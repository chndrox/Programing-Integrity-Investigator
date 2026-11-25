import logging
import time
from typing import Dict, Any
from app.services.groq_service import get_groq_service

logger = logging.getLogger(__name__)


class CaseWriter:
    """
    AGENT 4: CASE WRITER
    
    Synthesizes findings from all three agents into a comprehensive,
    neutral, evidence-based investigation report.
    
    Responsibilities:
    - Include evidence supporting and opposing the plagiarism suspicion
    - Preserve disagreements between agents
    - Identify uncertainties and evidence gaps
    - Explain investigation limitations
    - Provide neutral summary for instructor review
    - Never generate automatic guilty or innocent verdict
    """

    def __init__(self):
        self.groq = get_groq_service()

    async def generate_report(
        self,
        similarity_findings: Dict[str, Any],
        timeline_findings: Dict[str, Any],
        exculpatory_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive case report synthesizing all agent findings.
        
        Returns structured report with:
        - Executive summary
        - Detailed findings from each agent
        - Conflicting opinions preserved
        - Evidence gaps identified
        - Recommendations for instructor review
        """
        
        start_time = time.time()
        
        try:
            # Extract key findings from each agent
            extracted_findings = self._extract_findings(
                similarity_findings,
                timeline_findings,
                exculpatory_findings
            )
            
            # Use Groq to synthesize into report
            groq_report = await self._synthesize_with_groq(extracted_findings)
            
            # Build comprehensive report structure
            report = self._build_report_structure(
                extracted_findings,
                groq_report,
                similarity_findings,
                timeline_findings,
                exculpatory_findings
            )
            
            execution_time = time.time() - start_time
            
            return {
                "agent_type": "case_writer",
                "status": "completed",
                "report": report,
                "execution_time": execution_time,
                "metadata": {
                    "total_agents_reporting": 3,
                    "conflicting_opinions": len(self._identify_conflicts(
                        similarity_findings,
                        timeline_findings,
                        exculpatory_findings
                    )),
                    "evidence_completeness": self._assess_evidence_completeness(
                        extracted_findings
                    )
                }
            }
        
        except Exception as e:
            logger.error(f"Case Writer error: {str(e)}", exc_info=True)
            return {
                "agent_type": "case_writer",
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def _extract_findings(
        self,
        similarity: Dict[str, Any],
        timeline: Dict[str, Any],
        exculpatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract key findings from each agent."""
        
        return {
            "similarity_summary": {
                "status": similarity.get("status"),
                "comparisons": len(similarity.get("comparisons", [])),
                "highest_similarity": max(
                    (c["similarity_metrics"]["weighted_similarity"] 
                     for c in similarity.get("comparisons", [])),
                    default=0
                ),
                "average_similarity": sum(
                    c["similarity_metrics"]["weighted_similarity"]
                    for c in similarity.get("comparisons", [])
                ) / len(similarity.get("comparisons", [])) if similarity.get("comparisons") else 0,
                "summary": similarity.get("summary", "")
            },
            "timeline_summary": {
                "status": timeline.get("status"),
                "submissions_analyzed": timeline.get("submission_count", 0),
                "with_commit_history": sum(
                    1 for tl in timeline.get("individual_timelines", [])
                    if tl.get("has_history", False)
                ),
                "incremental_development_count": sum(
                    1 for tl in timeline.get("individual_timelines", [])
                    if tl.get("incremental_development", False)
                ),
                "summary": timeline.get("summary", "")
            },
            "exculpatory_summary": {
                "status": exculpatory.get("status"),
                "plagiarism_probability": exculpatory.get("defense_case", {}).get(
                    "probability_analysis", {}
                ).get("plagiarism_probability", 50),
                "defense_arguments": len(
                    exculpatory.get("defense_case", {}).get("defense_arguments", [])
                ),
                "supporting_evidence": len(
                    exculpatory.get("defense_case", {}).get("supporting_evidence", [])
                ),
                "summary": exculpatory.get("summary", "")
            }
        }

    async def _synthesize_with_groq(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Use Groq to synthesize findings into coherent report."""
        
        try:
            prompt = f"""Synthesize these investigation findings into a comprehensive case report:

SIMILARITY ANALYSIS:
- Status: {findings['similarity_summary']['status']}
- Comparisons: {findings['similarity_summary']['comparisons']}
- Highest similarity: {findings['similarity_summary']['highest_similarity']:.1f}%
- Average similarity: {findings['similarity_summary']['average_similarity']:.1f}%
- Summary: {findings['similarity_summary']['summary']}

TIMELINE ANALYSIS:
- Status: {findings['timeline_summary']['status']}
- Submissions with history: {findings['timeline_summary']['with_commit_history']}/{findings['timeline_summary']['submissions_analyzed']}
- Incremental development: {findings['timeline_summary']['incremental_development_count']}
- Summary: {findings['timeline_summary']['summary']}

EXCULPATORY ANALYSIS:
- Plagiarism probability: {findings['exculpatory_summary']['plagiarism_probability']}%
- Defense arguments: {findings['exculpatory_summary']['defense_arguments']}
- Supporting evidence: {findings['exculpatory_summary']['supporting_evidence']}
- Summary: {findings['exculpatory_summary']['summary']}

Create a balanced case report in JSON format with:
- executive_summary (neutral overview of investigation)
- key_evidence_supporting_plagiarism (list of concerning findings)
- key_evidence_supporting_innocence (list of exonerating findings)
- uncertainty_areas (where evidence is unclear or conflicting)
- evidence_gaps (what information is missing)
- confidence_statement (how confident should we be in findings)
- next_steps_for_instructor (recommended actions)
- important_limitations (what this analysis cannot determine)
"""
            
            system_prompt = """You are a neutral case report writer synthesizing a plagiarism investigation.
Your job is to present ALL evidence fairly - both supporting and opposing plagiarism suspicion.
Never reach a verdict. Present evidence for the instructor to decide.
Identify where agents disagree and preserve those disagreements."""
            
            report = await self.groq.analyze_text(prompt, system_prompt, json_mode=True)
            return report
        
        except Exception as e:
            logger.warning(f"Groq report synthesis failed: {str(e)}")
            return {
                "error": "Groq synthesis unavailable",
                "executive_summary": "Report synthesis unavailable"
            }

    def _build_report_structure(
        self,
        extracted: Dict[str, Any],
        groq_report: Dict[str, Any],
        similarity: Dict[str, Any],
        timeline: Dict[str, Any],
        exculpatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build comprehensive report structure."""
        
        conflicts = self._identify_conflicts(similarity, timeline, exculpatory)
        
        return {
            "case_metadata": {
                "investigation_type": "code_plagiarism",
                "agents_involved": ["similarity_analyst", "timeline_analyst", "exculpatory_reviewer"],
                "report_generated_by": "case_writer"
            },
            "executive_summary": groq_report.get(
                "executive_summary",
                "Investigation completed. See detailed findings below."
            ),
            "findings": {
                "similarity_findings": {
                    "highest_similarity": extracted["similarity_summary"]["highest_similarity"],
                    "average_similarity": extracted["similarity_summary"]["average_similarity"],
                    "comparisons_performed": extracted["similarity_summary"]["comparisons"],
                    "detailed_findings": similarity.get("comparisons", []),
                    "agent_summary": similarity.get("summary", ""),
                    "limitations": similarity.get("comparisons", [{}])[0].get("limitations", [])
                    if similarity.get("comparisons") else []
                },
                "timeline_findings": {
                    "submissions_analyzed": extracted["timeline_summary"]["submissions_analyzed"],
                    "with_commit_history": extracted["timeline_summary"]["with_commit_history"],
                    "incremental_development": extracted["timeline_summary"]["incremental_development_count"],
                    "detailed_findings": timeline.get("individual_timelines", []),
                    "temporal_comparisons": timeline.get("timeline_comparisons", []),
                    "agent_summary": timeline.get("summary", ""),
                    "limitations": timeline.get("limitations", [])
                },
                "exculpatory_findings": {
                    "plagiarism_probability": extracted["exculpatory_summary"]["plagiarism_probability"],
                    "independence_probability": 100 - extracted["exculpatory_summary"]["plagiarism_probability"],
                    "defense_case": exculpatory.get("defense_case", {}),
                    "agent_summary": exculpatory.get("summary", ""),
                    "contradictions_identified": exculpatory.get("contradictions_found", [])
                }
            },
            "evidence_synthesis": {
                "supporting_plagiarism": groq_report.get("key_evidence_supporting_plagiarism", []),
                "supporting_innocence": groq_report.get("key_evidence_supporting_innocence", []),
                "conflicting_agent_opinions": conflicts,
                "uncertainty_areas": groq_report.get("uncertainty_areas", []),
                "evidence_gaps": groq_report.get("evidence_gaps", [])
            },
            "confidence_and_limitations": {
                "overall_confidence": groq_report.get("confidence_statement", "Cannot assess"),
                "investigation_limitations": groq_report.get("important_limitations", []),
                "recommendation": groq_report.get("next_steps_for_instructor", "Review evidence carefully")
            },
            "instructor_guidance": {
                "important_note": "This report presents evidence for your review. The investigator has not reached a verdict.",
                "what_this_shows": "Potential concerns that warrant review",
                "what_this_does_not_show": "Definitive proof of plagiarism or innocence",
                "recommended_actions": [
                    "Review all evidence presented",
                    "Consider student explanations",
                    "Interview students if necessary",
                    "Consult assignment rubric and teaching materials",
                    "Compare with student's past work",
                    "Make final determination based on institutional policy"
                ]
            }
        }

    def _identify_conflicts(
        self,
        similarity: Dict[str, Any],
        timeline: Dict[str, Any],
        exculpatory: Dict[str, Any]
    ) -> list:
        """Identify where agents have conflicting opinions."""
        
        conflicts = []
        
        # Conflict 1: High similarity but exculpatory review suggests innocence
        avg_similarity = similarity.get("comparisons", [{}])[0].get("similarity_metrics", {}).get("weighted_similarity", 0) if similarity.get("comparisons") else 0
        plagiarism_prob = exculpatory.get("defense_case", {}).get("probability_analysis", {}).get("plagiarism_probability", 50)
        
        if avg_similarity > 60 and plagiarism_prob < 40:
            conflicts.append({
                "agents_in_conflict": ["similarity_analyst", "exculpatory_reviewer"],
                "similarity_view": f"High similarity ({avg_similarity:.1f}%) suggests potential plagiarism",
                "exculpatory_view": f"Low plagiarism probability ({plagiarism_prob}%) suggests innocence",
                "resolution": "Similarity alone does not prove plagiarism. Timeline and development process context is crucial."
            })
        
        # Conflict 2: Timeline shows incremental development vs high similarity
        with_history = timeline.get("individual_timelines", [])
        incremental_count = sum(1 for tl in with_history if tl.get("incremental_development", False))
        
        if incremental_count > 0 and avg_similarity > 60:
            conflicts.append({
                "agents_in_conflict": ["similarity_analyst", "timeline_analyst"],
                "similarity_view": f"High code similarity ({avg_similarity:.1f}%) is concerning",
                "timeline_view": f"Incremental development patterns ({incremental_count} submissions) suggest independent work",
                "resolution": "Independent work can still produce similar code. Both high similarity AND incremental development may coexist."
            })
        
        return conflicts

    def _assess_evidence_completeness(self, extracted: Dict[str, Any]) -> str:
        """Assess how complete the evidence is."""
        
        completeness = 0
        
        # Similarity evidence: 0-25 points
        if extracted["similarity_summary"]["comparisons"] > 0:
            completeness += 25
        
        # Timeline evidence: 0-25 points
        if extracted["timeline_summary"]["with_commit_history"] > 0:
            completeness += 25
        
        # Exculpatory evidence: 0-25 points
        if extracted["exculpatory_summary"]["defense_arguments"] > 0:
            completeness += 25
        
        # Agent diversity: 0-25 points
        completeness += 25  # Always have all 4 agents
        
        if completeness > 75:
            return "complete"
        elif completeness > 50:
            return "partial"
        else:
            return "incomplete"
