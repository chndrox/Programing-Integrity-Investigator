import logging
import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Submission
from app.services.timeline_service import TimelineService
from app.services.groq_service import get_groq_service

logger = logging.getLogger(__name__)


class TimelineAnalyst:
    """
    AGENT 2: TIMELINE ANALYST
    
    Analyzes commit history and development timelines using:
    - Commit frequency analysis
    - Incremental development assessment
    - Unusual pattern detection
    - Timeline comparison between submissions
    
    Uses Groq for interpretation of timeline patterns.
    """

    def __init__(self, db: Session):
        self.db = db
        self.groq = get_groq_service()

    async def analyze(self, submissions: List[Submission]) -> Dict[str, Any]:
        """
        Analyze development timelines for submissions.
        
        Returns:
        - Commit history analysis
        - Development patterns
        - Suspicious temporal patterns
        - Timeline comparisons
        """
        
        start_time = time.time()
        
        try:
            # Analyze individual timelines
            timeline_analyses = []
            
            for submission in submissions:
                timeline = TimelineService.analyze_submission_timeline(submission, self.db)
                timeline_analyses.append(timeline)
            
            # Compare timelines if multiple submissions
            timeline_comparisons = []
            if len(timeline_analyses) >= 2:
                for i in range(len(timeline_analyses)):
                    for j in range(i + 1, len(timeline_analyses)):
                        comparison = TimelineService.compare_timelines(
                            timeline_analyses[i],
                            timeline_analyses[j]
                        )
                        timeline_comparisons.append(comparison)
            
            # Enhance with Groq analysis
            groq_analysis = await self._analyze_patterns_with_groq(
                timeline_analyses,
                timeline_comparisons
            )
            
            execution_time = time.time() - start_time
            
            return {
                "agent_type": "timeline_analyst",
                "status": "completed",
                "submission_count": len(submissions),
                "individual_timelines": timeline_analyses,
                "timeline_comparisons": timeline_comparisons,
                "groq_insights": groq_analysis,
                "execution_time": execution_time,
                "summary": self._generate_summary(timeline_analyses, timeline_comparisons),
                "limitations": [
                    "Analysis depends on available commit history",
                    "Missing commit history does not indicate plagiarism",
                    "Development patterns vary by individual and project type",
                    "Requires accurate commit timestamps (may be manipulated)",
                    "Cannot detect copy-paste within single session"
                ]
            }
        
        except Exception as e:
            logger.error(f"Timeline Analyst error: {str(e)}", exc_info=True)
            return {
                "agent_type": "timeline_analyst",
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    async def _analyze_patterns_with_groq(
        self,
        timelines: List[Dict[str, Any]],
        comparisons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Use Groq to analyze timeline patterns."""
        
        try:
            # Prepare timeline summary for analysis
            timeline_summary = ""
            for i, tl in enumerate(timelines):
                timeline_summary += f"\nSubmission {i+1}:\n"
                timeline_summary += f"  - Commits: {tl.get('commit_count', 0)}\n"
                timeline_summary += f"  - Span: {tl.get('timeline_span_days', 0):.1f} days\n"
                timeline_summary += f"  - Total additions: {tl.get('total_additions', 0)}\n"
                timeline_summary += f"  - Incremental: {tl.get('incremental_development', False)}\n"
                if tl.get("unusual_patterns"):
                    timeline_summary += f"  - Patterns: {', '.join(tl.get('unusual_patterns', []))}\n"
            
            prompt = f"""Analyze these development timeline patterns for suspicious indicators:

{timeline_summary}

Consider:
1. Is development pattern typical for the assignment type?
2. Are there signs of work done in bulk vs. incremental?
3. Do timeline patterns match between submissions (suspicious)?
4. Are unusual patterns explainable or concerning?

Provide analysis in JSON format with:
- development_pattern_assessment (typical, irregular, suspicious)
- incremental_development_evidence (strong, moderate, weak)
- temporal_anomalies (list of concerning patterns)
- timeline_consistency (consistent across submissions, inconsistent, varies)
- red_flags (list of items needing investigation)
- innocence_indicators (evidence supporting independent work)
- confidence_level (high, medium, low)
- analyst_notes
"""
            
            system_prompt = """You are a development timeline analyst specializing in detecting plagiarism through 
commit patterns. Analyze development timelines critically but fairly. Missing history or unusual patterns don't 
automatically indicate plagiarism - consider alternative explanations."""
            
            analysis = await self.groq.analyze_text(prompt, system_prompt)
            return analysis
        
        except Exception as e:
            logger.warning(f"Groq timeline analysis failed: {str(e)}")
            return {
                "error": "Groq analysis unavailable",
                "analysis": "Deterministic timeline analysis completed. Consult Groq service for pattern interpretation."
            }

    def _generate_summary(
        self,
        timelines: List[Dict[str, Any]],
        comparisons: List[Dict[str, Any]]
    ) -> str:
        """Generate a summary of timeline analysis."""
        
        if not timelines:
            return "No timelines to analyze."
        
        # Count submissions with history
        with_history = sum(1 for tl in timelines if tl.get("has_history", False))
        
        # Identify unusual patterns
        all_patterns = []
        for tl in timelines:
            all_patterns.extend(tl.get("unusual_patterns", []))
        
        # Count incremental development
        incremental_count = sum(1 for tl in timelines if tl.get("incremental_development", False))
        
        summary = f"""Timeline analysis completed for {len(timelines)} submission(s).

Submissions with commit history: {with_history}
Submissions with incremental development: {incremental_count}
Total unusual patterns detected: {len(all_patterns)}
Submission pair comparisons: {len(comparisons)}"""
        
        if comparisons:
            suspicious_pairs = sum(1 for c in comparisons if c.get("suspicious_temporal_patterns"))
            summary += f"\n\nTemporal patterns found suspicious: {suspicious_pairs}"
        
        summary += """\n\nNote: Missing commit history does not indicate plagiarism. 
The analysis evaluates available evidence only."""
        
        return summary
