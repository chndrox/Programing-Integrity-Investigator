import logging
import time
import json
from typing import Dict, Any, List
from app.services.groq_service import get_groq_service

logger = logging.getLogger(__name__)


class ExculpatoryReviewer:
    """
    AGENT 3: EXCULPATORY REVIEWER
    
    Represents the student's defense perspective.
    
    Examines findings from other agents and searches for:
    - Evidence supporting independent development
    - Legitimate alternative explanations
    - Common programming patterns
    - Weaknesses in the evidence
    - Missing information
    - Questions requiring clarification
    
    This agent works independently and critically challenges assumptions.
    """

    def __init__(self):
        self.groq = get_groq_service()

    async def review(
        self,
        similarity_findings: Dict[str, Any],
        timeline_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Review findings from other agents and generate exculpatory evidence.
        
        Returns analysis focusing on:
        - Alternative explanations
        - Evidence of independent work
        - Common patterns that explain similarities
        - Missing evidence
        - Critical questions
        """
        
        start_time = time.time()
        
        try:
            # Prepare findings summary
            findings_summary = self._prepare_findings_summary(
                similarity_findings,
                timeline_findings
            )
            
            # Use Groq to generate detailed exculpatory analysis
            exculpatory_analysis = await self._generate_exculpatory_analysis(
                findings_summary
            )
            
            # Extract and structure key elements
            defense_case = self._build_defense_case(
                exculpatory_analysis,
                similarity_findings,
                timeline_findings
            )
            
            execution_time = time.time() - start_time
            
            return {
                "agent_type": "exculpatory_reviewer",
                "status": "completed",
                "defense_case": defense_case,
                "exculpatory_analysis": exculpatory_analysis,
                "contradictions_found": self._identify_contradictions(
                    similarity_findings,
                    exculpatory_analysis
                ),
                "execution_time": execution_time,
                "summary": self._generate_summary(defense_case)
            }
        
        except Exception as e:
            logger.error(f"Exculpatory Reviewer error: {str(e)}", exc_info=True)
            return {
                "agent_type": "exculpatory_reviewer",
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def _prepare_findings_summary(
        self,
        similarity_findings: Dict[str, Any],
        timeline_findings: Dict[str, Any]
    ) -> str:
        """Prepare a summary of findings to review."""
        
        summary = "FINDINGS TO REVIEW:\n\n"
        
        # Similarity findings
        summary += "SIMILARITY FINDINGS:\n"
        if "comparisons" in similarity_findings:
            for comp in similarity_findings.get("comparisons", []):
                similarity = comp.get("similarity_metrics", {}).get("weighted_similarity", 0)
                summary += f"- Submissions {comp.get('submission1_id')} vs {comp.get('submission2_id')}: {similarity:.1f}% similarity\n"
                matching_blocks = comp.get("total_matching_blocks", 0)
                summary += f"  Matching blocks: {matching_blocks}\n"
                unique1 = comp.get("unique_lines", {}).get("code1", 0)
                unique2 = comp.get("unique_lines", {}).get("code2", 0)
                summary += f"  Unique lines: Submission 1: {unique1}, Submission 2: {unique2}\n"
        
        # Timeline findings
        summary += "\nTIMELINE FINDINGS:\n"
        if "individual_timelines" in timeline_findings:
            for tl in timeline_findings.get("individual_timelines", []):
                summary += f"- Submission {tl.get('submission_id')}: {tl.get('commit_count', 0)} commits over {tl.get('timeline_span_days', 0):.1f} days\n"
                incremental = tl.get("incremental_development", False)
                summary += f"  Incremental development: {incremental}\n"
                patterns = tl.get("unusual_patterns", [])
                if patterns:
                    summary += f"  Unusual patterns: {', '.join(patterns[:2])}\n"
        
        return summary

    async def _generate_exculpatory_analysis(self, findings_summary: str) -> Dict[str, Any]:
        """Generate detailed exculpatory analysis using Groq."""
        
        try:
            prompt = f"""{findings_summary}

As the student's defense advocate, analyze these findings and provide:

1. ALTERNATIVE EXPLANATIONS: What legitimate reasons could explain these similarities?
2. COMMON PATTERNS: Which patterns are common in {len([x for x in findings_summary.split('\n') if 'Submission' in x])} submissions?
3. EVIDENCE OF INDEPENDENT WORK: What evidence suggests independent development?
4. WEAKNESSES IN ACCUSATION: What is missing or weak in the evidence?
5. MISSING INFORMATION: What additional evidence would help clear the student?
6. CRITICAL QUESTIONS: What questions should the instructor ask?
7. PROBABILITY ASSESSMENT: How likely is plagiarism vs. coincidence?

Format response as JSON with these exact keys:
- alternative_explanations
- common_patterns_found
- independent_work_evidence
- evidence_weaknesses
- missing_information
- critical_questions
- plagiarism_probability (percentage)
- student_perspective_summary
"""
            
            system_prompt = """You are an adversarial reviewer representing the student's defense. 
Your role is to find weaknesses in plagiarism accusations, alternative explanations, and evidence of independent work.
Be thorough in finding legitimate explanations for similarities. Challenge assumptions.
However, be honest - if the evidence is strong, acknowledge it."""
            
            analysis = await self.groq.analyze_text(prompt, system_prompt, json_mode=True)
            return analysis
        
        except Exception as e:
            logger.warning(f"Groq exculpatory analysis failed: {str(e)}")
            return {
                "error": "Groq analysis unavailable",
                "alternative_explanations": ["Analysis requires Groq service"],
                "student_perspective_summary": "Unable to generate detailed analysis"
            }

    def _build_defense_case(
        self,
        exculpatory_analysis: Dict[str, Any],
        similarity_findings: Dict[str, Any],
        timeline_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a structured defense case."""
        
        return {
            "defending_students": self._extract_students(similarity_findings),
            "charges": self._extract_charges(similarity_findings),
            "defense_arguments": exculpatory_analysis.get("alternative_explanations", []),
            "supporting_evidence": exculpatory_analysis.get("independent_work_evidence", []),
            "weakness_in_prosecution": exculpatory_analysis.get("evidence_weaknesses", []),
            "questions_for_court": exculpatory_analysis.get("critical_questions", []),
            "probability_analysis": {
                "plagiarism_probability": exculpatory_analysis.get("plagiarism_probability", 50),
                "independence_probability": 100 - exculpatory_analysis.get("plagiarism_probability", 50)
            },
            "prosecution_strategy": self._identify_prosecution_case(similarity_findings),
            "defense_recommendation": self._generate_defense_recommendation(
                exculpatory_analysis,
                similarity_findings
            )
        }

    def _extract_students(self, similarity_findings: Dict[str, Any]) -> List[str]:
        """Extract student names from findings."""
        students = set()
        for comp in similarity_findings.get("comparisons", []):
            students.add(comp.get("submission1_student", "Unknown"))
            students.add(comp.get("submission2_student", "Unknown"))
        return list(students)

    def _extract_charges(self, similarity_findings: Dict[str, Any]) -> List[str]:
        """Extract plagiarism charges from findings."""
        charges = []
        for comp in similarity_findings.get("comparisons", []):
            similarity = comp.get("similarity_metrics", {}).get("weighted_similarity", 0)
            if similarity > 50:
                charges.append(
                    f"Submission {comp.get('submission1_id')} copied from {comp.get('submission2_id')} "
                    f"({similarity:.1f}% similarity)"
                )
        return charges

    def _identify_prosecution_case(self, similarity_findings: Dict[str, Any]) -> str:
        """Summarize what the prosecution (plagiarism detector) is arguing."""
        
        case = "PROSECUTION CASE:\n"
        
        for comp in similarity_findings.get("comparisons", []):
            similarity = comp.get("similarity_metrics", {}).get("weighted_similarity", 0)
            if similarity > 50:
                matching_blocks = comp.get("total_matching_blocks", 0)
                case += f"\n- High similarity ({similarity:.1f}%) between submissions\n"
                case += f"  {matching_blocks} matching code blocks found\n"
        
        if case == "PROSECUTION CASE:\n":
            case += "No strong similarity evidence to prosecute"
        
        return case

    def _generate_defense_recommendation(
        self,
        exculpatory_analysis: Dict[str, Any],
        similarity_findings: Dict[str, Any]
    ) -> str:
        """Generate recommendation for the defense."""
        
        plagiarism_prob = exculpatory_analysis.get("plagiarism_probability", 50)
        
        if plagiarism_prob < 30:
            return "RECOMMENDATION: Request dismissal of charges. Strong evidence of independent work."
        elif plagiarism_prob < 60:
            return "RECOMMENDATION: Request further investigation. Evidence is mixed and inconclusive."
        else:
            return "RECOMMENDATION: Acknowledge similarities but request lenient consideration. Explain alternative explanations to instructor."

    def _identify_contradictions(
        self,
        similarity_findings: Dict[str, Any],
        exculpatory_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify contradictions between findings and defense."""
        
        contradictions = []
        
        # Check if similarity is high but timeline shows independent development
        for comp in similarity_findings.get("comparisons", []):
            similarity = comp.get("similarity_metrics", {}).get("weighted_similarity", 0)
            if similarity > 60:
                # This contradicts low plagiarism probability
                plagiarism_prob = exculpatory_analysis.get("plagiarism_probability", 50)
                if plagiarism_prob < 40:
                    contradictions.append(
                        f"High similarity ({similarity:.1f}%) contradicts low plagiarism probability ({plagiarism_prob}%)"
                    )
        
        return contradictions

    def _generate_summary(self, defense_case: Dict[str, Any]) -> str:
        """Generate summary of exculpatory review."""
        
        students = defense_case.get("defending_students", [])
        plagiarism_prob = defense_case.get("probability_analysis", {}).get("plagiarism_probability", 50)
        
        summary = f"Exculpatory review for {', '.join(students)}:\n"
        summary += f"Plagiarism probability: {plagiarism_prob}%\n"
        summary += f"Defense arguments: {len(defense_case.get('defense_arguments', []))}\n"
        summary += f"Supporting evidence: {len(defense_case.get('supporting_evidence', []))}\n"
        summary += f"Identified weaknesses: {len(defense_case.get('weakness_in_prosecution', []))}\n"
        
        if plagiarism_prob < 40:
            summary += "\nVERDICT: Evidence leans toward innocence. Further investigation needed to confirm."
        elif plagiarism_prob > 70:
            summary += "\nVERDICT: Evidence leans toward plagiarism. But alternative explanations possible."
        else:
            summary += "\nVERDICT: Mixed evidence. Requires instructor judgment and additional investigation."
        
        return summary
