"""
SIMILARITY-MCP SERVER

Provides tools for code similarity analysis and cohort baseline calculations.
Implements local mock mode if external MCP servers unavailable.
"""

import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import Submission
from app.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)


class SimilarityMCP:
    """Mock implementation of similarity MCP server."""

    def __init__(self, db: Session):
        self.db = db

    async def compare_submissions(
        self,
        submission_id_1: int,
        submission_id_2: int
    ) -> Dict[str, Any]:
        """
        Compare two submissions for code similarity.
        
        Tool: similarity-mcp.compare_submissions
        Parameters:
        - submission_id_1: int
        - submission_id_2: int
        
        Returns: Detailed similarity analysis
        """
        
        try:
            submission1 = self.db.query(Submission).filter(
                Submission.id == submission_id_1
            ).first()
            
            submission2 = self.db.query(Submission).filter(
                Submission.id == submission_id_2
            ).first()
            
            if not submission1 or not submission2:
                return {
                    "status": "error",
                    "message": "One or both submissions not found"
                }
            
            if not submission1.source_code or not submission2.source_code:
                return {
                    "status": "error",
                    "message": "Source code not available for one or both submissions"
                }
            
            # Perform comparison
            comparison = SimilarityService.comprehensive_comparison(
                submission1.source_code,
                submission2.source_code
            )
            
            return {
                "status": "success",
                "submission_1": {
                    "id": submission1.id,
                    "student": submission1.student.name
                },
                "submission_2": {
                    "id": submission2.id,
                    "student": submission2.student.name
                },
                "analysis": comparison
            }
        
        except Exception as e:
            logger.error(f"Error comparing submissions: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def get_cohort_baseline(self, assignment_id: int) -> Dict[str, Any]:
        """
        Calculate cohort baseline similarity statistics.
        Useful for determining whether a similarity percentage is unusual.
        
        Tool: similarity-mcp.get_cohort_baseline
        Parameters:
        - assignment_id: int
        
        Returns: Baseline statistics for the assignment cohort
        """
        
        try:
            # Get all submissions for this assignment
            submissions = self.db.query(Submission).filter(
                Submission.assignment_id == assignment_id
            ).all()
            
            if len(submissions) < 2:
                return {
                    "status": "error",
                    "message": "Insufficient submissions for baseline calculation"
                }
            
            # Calculate pairwise similarities
            similarities = []
            
            for i in range(len(submissions)):
                for j in range(i + 1, len(submissions)):
                    if submissions[i].source_code and submissions[j].source_code:
                        comparison = SimilarityService.comprehensive_comparison(
                            submissions[i].source_code,
                            submissions[j].source_code
                        )
                        similarities.append(comparison["similarity_percentage"])
            
            if not similarities:
                return {
                    "status": "error",
                    "message": "Could not calculate similarities"
                }
            
            # Calculate statistics
            similarities_sorted = sorted(similarities)
            mean_similarity = sum(similarities) / len(similarities)
            median_similarity = similarities_sorted[len(similarities) // 2]
            min_similarity = min(similarities)
            max_similarity = max(similarities)
            
            # Calculate percentiles
            p25_idx = len(similarities) // 4
            p75_idx = 3 * len(similarities) // 4
            p25 = similarities_sorted[p25_idx]
            p75 = similarities_sorted[p75_idx]
            
            return {
                "status": "success",
                "assignment_id": assignment_id,
                "total_submissions": len(submissions),
                "total_comparisons": len(similarities),
                "statistics": {
                    "mean_similarity": round(mean_similarity, 2),
                    "median_similarity": round(median_similarity, 2),
                    "min_similarity": round(min_similarity, 2),
                    "max_similarity": round(max_similarity, 2),
                    "std_dev": self._calculate_std_dev(similarities),
                    "p25": round(p25, 2),
                    "p75": round(p75, 2)
                },
                "interpretation": self._interpret_baseline(mean_similarity, max_similarity)
            }
        
        except Exception as e:
            logger.error(f"Error calculating cohort baseline: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def _calculate_std_dev(values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return (variance ** 0.5)

    @staticmethod
    def _interpret_baseline(mean_similarity: float, max_similarity: float) -> str:
        """Interpret baseline statistics."""
        
        if mean_similarity < 20:
            return "Low average similarity - assignments show diverse solutions"
        elif mean_similarity < 40:
            return "Moderate average similarity - typical for assignment cohort"
        elif mean_similarity < 60:
            return "Higher average similarity - check if assignments have natural similarities"
        else:
            return "Very high average similarity - possible systematic issue or related problems"

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools in this MCP server."""
        return [
            {
                "name": "compare_submissions",
                "description": "Compare two submissions for code similarity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "submission_id_1": {
                            "type": "integer",
                            "description": "ID of the first submission"
                        },
                        "submission_id_2": {
                            "type": "integer",
                            "description": "ID of the second submission"
                        }
                    },
                    "required": ["submission_id_1", "submission_id_2"]
                }
            },
            {
                "name": "get_cohort_baseline",
                "description": "Get baseline similarity statistics for an assignment cohort",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "assignment_id": {
                            "type": "integer",
                            "description": "ID of the assignment"
                        }
                    },
                    "required": ["assignment_id"]
                }
            }
        ]
