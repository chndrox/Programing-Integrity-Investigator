import logging
import asyncio
import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Investigation, Submission, AgentResult, AgentType
from app.database import settings
from app.agents.similarity_analyst import SimilarityAnalyst
from app.agents.timeline_analyst import TimelineAnalyst
from app.agents.exculpatory_reviewer import ExculpatoryReviewer
from app.agents.case_writer import CaseWriter

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Central coordinator for multi-agent investigation workflow.
    
    Orchestration flow:
    1. Retrieve investigation and submissions
    2. Execute Similarity Analyst
    3. Execute Timeline Analyst (can run concurrently with Similarity)
    4. Execute Exculpatory Reviewer (uses Similarity and Timeline results)
    5. Execute Case Writer (synthesizes all findings)
    6. Store complete investigation results
    
    Concurrency is controlled by configurable limit to avoid overwhelming Groq API.
    """

    def __init__(self, db: Session):
        self.db = db
        self.concurrency_limit = settings.agent_concurrency_limit
        self.timeout_seconds = settings.agent_timeout_seconds
        
        # Initialize agents
        self.similarity_analyst = SimilarityAnalyst(db)
        self.timeline_analyst = TimelineAnalyst(db)
        self.exculpatory_reviewer = ExculpatoryReviewer()
        self.case_writer = CaseWriter()

    async def orchestrate_investigation(
        self,
        investigation_id: int
    ) -> Dict[str, Any]:
        """
        Execute complete investigation workflow for an investigation.
        
        Returns:
        - All agent results
        - Investigation status
        - Final case report
        """
        
        investigation_start_time = time.time()
        
        try:
            # Retrieve investigation and submissions
            investigation = self.db.query(Investigation).filter(
                Investigation.id == investigation_id
            ).first()
            
            if not investigation:
                raise ValueError(f"Investigation {investigation_id} not found")
            
            submissions = investigation.submissions
            
            if len(submissions) < 2:
                raise ValueError("Investigation requires at least 2 submissions")
            
            # Update investigation status
            investigation.status = "in_progress"
            investigation.started_at = asyncio.get_event_loop().time()
            self.db.commit()
            
            logger.info(f"Starting investigation {investigation_id} with {len(submissions)} submissions")
            
            # Phase 1: Execute parallel agents (Similarity and Timeline)
            logger.info("Phase 1: Executing parallel agents (Similarity Analyst, Timeline Analyst)")
            
            similarity_result, timeline_result = await asyncio.gather(
                self._execute_agent(
                    "similarity_analyst",
                    self.similarity_analyst.analyze(submissions),
                    investigation_id
                ),
                self._execute_agent(
                    "timeline_analyst",
                    self.timeline_analyst.analyze(submissions),
                    investigation_id
                ),
                return_exceptions=True
            )
            
            # Handle any exceptions
            if isinstance(similarity_result, Exception):
                logger.error(f"Similarity Analyst failed: {similarity_result}")
                similarity_result = {
                    "agent_type": "similarity_analyst",
                    "status": "failed",
                    "error": str(similarity_result)
                }
            
            if isinstance(timeline_result, Exception):
                logger.error(f"Timeline Analyst failed: {timeline_result}")
                timeline_result = {
                    "agent_type": "timeline_analyst",
                    "status": "failed",
                    "error": str(timeline_result)
                }
            
            # Phase 2: Execute Exculpatory Reviewer (uses Phase 1 results)
            logger.info("Phase 2: Executing Exculpatory Reviewer")
            
            exculpatory_result = await self._execute_agent(
                "exculpatory_reviewer",
                self.exculpatory_reviewer.review(
                    similarity_result,
                    timeline_result
                ),
                investigation_id
            )
            
            if isinstance(exculpatory_result, Exception):
                logger.error(f"Exculpatory Reviewer failed: {exculpatory_result}")
                exculpatory_result = {
                    "agent_type": "exculpatory_reviewer",
                    "status": "failed",
                    "error": str(exculpatory_result)
                }
            
            # Phase 3: Execute Case Writer (uses all previous results)
            logger.info("Phase 3: Executing Case Writer")
            
            case_writer_result = await self._execute_agent(
                "case_writer",
                self.case_writer.generate_report(
                    similarity_result,
                    timeline_result,
                    exculpatory_result
                ),
                investigation_id
            )
            
            if isinstance(case_writer_result, Exception):
                logger.error(f"Case Writer failed: {case_writer_result}")
                case_writer_result = {
                    "agent_type": "case_writer",
                    "status": "failed",
                    "error": str(case_writer_result)
                }
            
            # Store results in database
            agent_results = [
                similarity_result,
                timeline_result,
                exculpatory_result,
                case_writer_result
            ]
            
            for result in agent_results:
                agent_result = AgentResult(
                    investigation_id=investigation_id,
                    agent_type=result.get("agent_type", "unknown"),
                    status=result.get("status", "failed"),
                    result=result,
                    error=result.get("error"),
                    execution_time=result.get("execution_time")
                )
                self.db.add(agent_result)
            
            # Update investigation status
            investigation.status = "completed"
            investigation.completed_at = asyncio.get_event_loop().time()
            self.db.commit()
            
            total_execution_time = time.time() - investigation_start_time
            
            logger.info(f"Investigation {investigation_id} completed in {total_execution_time:.2f}s")
            
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "total_execution_time": total_execution_time,
                "agent_results": {
                    "similarity_analyst": similarity_result,
                    "timeline_analyst": timeline_result,
                    "exculpatory_reviewer": exculpatory_result,
                    "case_writer": case_writer_result
                }
            }
        
        except Exception as e:
            logger.error(f"Investigation orchestration failed: {str(e)}", exc_info=True)
            
            # Update investigation status
            investigation.status = "failed"
            investigation.error_message = str(e)
            self.db.commit()
            
            return {
                "investigation_id": investigation_id,
                "status": "failed",
                "error": str(e),
                "total_execution_time": time.time() - investigation_start_time
            }

    async def _execute_agent(
        self,
        agent_name: str,
        agent_coro,
        investigation_id: int
    ) -> Dict[str, Any]:
        """
        Execute a single agent with timeout handling.
        """
        
        try:
            # Wrap in timeout
            result = await asyncio.wait_for(
                agent_coro,
                timeout=self.timeout_seconds
            )
            
            logger.info(f"{agent_name} completed successfully")
            return result
        
        except asyncio.TimeoutError:
            logger.error(f"{agent_name} timed out after {self.timeout_seconds}s")
            return {
                "agent_type": agent_name,
                "status": "failed",
                "error": f"Agent execution timed out after {self.timeout_seconds} seconds"
            }
        
        except Exception as e:
            logger.error(f"{agent_name} failed: {str(e)}")
            return {
                "agent_type": agent_name,
                "status": "failed",
                "error": str(e)
            }
