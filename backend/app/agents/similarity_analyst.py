import logging
import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Submission, AgentResult
from app.services.similarity_service import SimilarityService
from app.services.groq_service import get_groq_service

logger = logging.getLogger(__name__)


class SimilarityAnalyst:
    """
    AGENT 1: SIMILARITY ANALYST
    
    Analyzes source code similarity between submissions using:
    - Deterministic token-based comparison
    - AST analysis
    - Line-by-line comparison
    - Function/variable name overlap
    
    Uses Groq for interpretation and analysis explanation.
    """

    def __init__(self, db: Session):
        self.db = db
        self.groq = get_groq_service()

    async def analyze(self, submissions: List[Submission]) -> Dict[str, Any]:
        """
        Analyze code similarity between multiple submissions.
        
        Returns comprehensive similarity analysis with:
        - Similarity percentages
        - Matching code blocks
        - Confidence levels
        - Limitations
        """
        
        start_time = time.time()
        
        try:
            if len(submissions) < 2:
                return {
                    "error": "At least 2 submissions required for comparison",
                    "execution_time": time.time() - start_time
                }
            
            # Analyze all pairs
            similarity_results = []
            
            for i in range(len(submissions)):
                for j in range(i + 1, len(submissions)):
                    submission1 = submissions[i]
                    submission2 = submissions[j]
                    
                    # Get source code
                    if not submission1.source_code or not submission2.source_code:
                        logger.warning(f"Missing source code for submissions {submission1.id} or {submission2.id}")
                        continue
                    
                    # Perform deterministic analysis
                    comparison = SimilarityService.comprehensive_comparison(
                        submission1.source_code,
                        submission2.source_code
                    )
                    
                    # Enhance with Groq analysis of the patterns
                    groq_analysis = await self._analyze_patterns_with_groq(
                        comparison,
                        submission1,
                        submission2
                    )
                    
                    result = {
                        "submission1_id": submission1.id,
                        "submission1_student": submission1.student.name,
                        "submission2_id": submission2.id,
                        "submission2_student": submission2.student.name,
                        "similarity_metrics": {
                            "weighted_similarity": comparison["similarity_percentage"],
                            "token_similarity": comparison["token_similarity"],
                            "ast_similarity": comparison["ast_similarity"],
                            "line_similarity": comparison["line_similarity"],
                            "name_overlap": comparison["name_overlap"]
                        },
                        "matching_blocks": comparison["matching_blocks"],
                        "total_matching_blocks": comparison["total_matching_blocks"],
                        "matching_lines": comparison["matching_lines"],
                        "unique_lines": {
                            "code1": comparison["unique_lines_code1"],
                            "code2": comparison["unique_lines_code2"]
                        },
                        "confidence_level": comparison["confidence_level"],
                        "deterministic_analysis": comparison["analysis"],
                        "groq_insights": groq_analysis,
                        "limitations": [
                            "Analysis based on static code comparison",
                            "Does not access full repository history",
                            "May flag legitimate code as similar (common patterns)",
                            "Language-specific analysis limited to Python"
                        ]
                    }
                    
                    similarity_results.append(result)
            
            execution_time = time.time() - start_time
            
            return {
                "agent_type": "similarity_analyst",
                "status": "completed",
                "submission_count": len(submissions),
                "comparison_count": len(similarity_results),
                "comparisons": similarity_results,
                "execution_time": execution_time,
                "summary": self._generate_summary(similarity_results)
            }
        
        except Exception as e:
            logger.error(f"Similarity Analyst error: {str(e)}", exc_info=True)
            return {
                "agent_type": "similarity_analyst",
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    async def _analyze_patterns_with_groq(
        self,
        comparison: Dict[str, Any],
        submission1: Submission,
        submission2: Submission
    ) -> Dict[str, Any]:
        """Use Groq to provide insights into the detected patterns."""
        
        try:
            # Prepare comparison summary for Groq
            blocks_summary = "\n".join([
                f"Block {i+1}: {block['size']} matching lines at {block['file1_start']}-{block['file1_end']}"
                for i, block in enumerate(comparison["matching_blocks"][:5])
            ])
            
            if not blocks_summary:
                blocks_summary = "No significant matching blocks (< 3 lines)"
            
            prompt = f"""Analyze these code similarity findings:

Similarity Metrics:
- Overall Similarity: {comparison['similarity_percentage']:.1f}%
- Token Similarity: {comparison['token_similarity']:.1f}%
- AST Similarity: {comparison['ast_similarity']:.1f}%
- Line Similarity: {comparison['line_similarity']:.1f}%
- Name Overlap: {comparison['name_overlap']:.1f}%

Matching Code Blocks Found:
{blocks_summary}

Total Code Lines:
- File 1: {comparison['total_lines_code1']} lines
- File 2: {comparison['total_lines_code2']} lines

Matching Lines: {comparison['matching_lines']}
Unique to File 1: {comparison['unique_lines_code1']}
Unique to File 2: {comparison['unique_lines_code2']}

Provide insights in JSON format with:
- pattern_explanation (what these similarities likely represent)
- legitimacy_assessment (how likely these are from independent development)
- concern_level (low, medium, high)
- further_investigation_needed (true/false)
"""
            
            system_prompt = """You are an expert code plagiarism analyst. Interpret code similarity metrics 
and determine whether patterns suggest plagiarism or legitimate independent development with common patterns.
Provide balanced analysis. High similarity alone does not prove plagiarism."""
            
            analysis = await self.groq.analyze_text(prompt, system_prompt)
            return analysis
        
        except Exception as e:
            logger.warning(f"Groq analysis failed: {str(e)}")
            return {
                "error": "Groq analysis unavailable",
                "pattern_explanation": "Deterministic analysis only - consult Groq service for pattern insights"
            }

    def _generate_summary(self, results: List[Dict[str, Any]]) -> str:
        """Generate a summary of similarity analysis."""
        
        if not results:
            return "No submissions to compare."
        
        avg_similarity = sum(r["similarity_metrics"]["weighted_similarity"] for r in results) / len(results)
        
        high_similarity = sum(1 for r in results if r["similarity_metrics"]["weighted_similarity"] > 70)
        medium_similarity = sum(1 for r in results if 40 <= r["similarity_metrics"]["weighted_similarity"] <= 70)
        low_similarity = sum(1 for r in results if r["similarity_metrics"]["weighted_similarity"] < 40)
        
        summary = f"""Analyzed {len(results)} submission pair(s).
        
Average Similarity: {avg_similarity:.1f}%

Breakdown:
- High similarity (>70%): {high_similarity}
- Medium similarity (40-70%): {medium_similarity}
- Low similarity (<40%): {low_similarity}

Note: Similarity percentages alone do not indicate plagiarism. 
Timeline, development patterns, and code comments must also be considered."""
        
        return summary
