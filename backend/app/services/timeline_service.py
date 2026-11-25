import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import CommitHistory, Submission

logger = logging.getLogger(__name__)


class TimelineService:
    """
    Analyze development timelines and commit patterns.
    Does not require Git repository access - works with stored commit history.
    """

    @staticmethod
    def analyze_submission_timeline(submission: Submission, db: Session) -> Dict[str, Any]:
        """Analyze the development timeline for a single submission."""
        
        # Get commit history
        commits = db.query(CommitHistory).filter(
            CommitHistory.submission_id == submission.id
        ).order_by(CommitHistory.timestamp).all()
        
        if not commits:
            return {
                "submission_id": submission.id,
                "has_history": False,
                "commits": [],
                "commit_count": 0,
                "analysis": "No commit history available for this submission."
            }
        
        # Analyze timeline
        commits_data = []
        total_additions = 0
        total_deletions = 0
        
        for commit in commits:
            commits_data.append({
                "hash": commit.commit_hash,
                "author": commit.author,
                "message": commit.message,
                "timestamp": commit.timestamp.isoformat(),
                "additions": commit.additions,
                "deletions": commit.deletions
            })
            total_additions += commit.additions
            total_deletions += commit.deletions
        
        # Calculate timeline statistics
        first_commit = commits[0].timestamp
        last_commit = commits[-1].timestamp
        timeline_span = (last_commit - first_commit).total_seconds() / 86400  # Convert to days
        
        # Analyze commit frequency
        commit_intervals = []
        for i in range(1, len(commits)):
            interval = (commits[i].timestamp - commits[i-1].timestamp).total_seconds() / 3600  # In hours
            commit_intervals.append(interval)
        
        avg_interval_hours = sum(commit_intervals) / len(commit_intervals) if commit_intervals else 0
        
        # Identify large commits (potential concerns or expected patterns)
        large_commits = []
        for commit in commits:
            total_changes = commit.additions + commit.deletions
            if total_changes > 100:  # Large commit threshold
                large_commits.append({
                    "hash": commit.commit_hash,
                    "message": commit.message,
                    "timestamp": commit.timestamp.isoformat(),
                    "total_changes": total_changes,
                    "additions": commit.additions,
                    "deletions": commit.deletions
                })
        
        # Assess incremental development
        is_incremental = TimelineService._assess_incremental_development(
            commits,
            total_additions,
            timeline_span
        )
        
        # Identify unusual patterns
        unusual_patterns = TimelineService._identify_unusual_patterns(
            commits,
            commit_intervals,
            large_commits
        )
        
        return {
            "submission_id": submission.id,
            "has_history": True,
            "commits": commits_data,
            "commit_count": len(commits),
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "timeline_span_days": round(timeline_span, 2),
            "first_commit": first_commit.isoformat(),
            "last_commit": last_commit.isoformat(),
            "average_interval_hours": round(avg_interval_hours, 2),
            "large_commits": large_commits,
            "incremental_development": is_incremental,
            "unusual_patterns": unusual_patterns,
            "analysis": TimelineService._generate_timeline_analysis(
                len(commits),
                timeline_span,
                is_incremental,
                unusual_patterns,
                total_additions
            )
        }

    @staticmethod
    def _assess_incremental_development(
        commits: List,
        total_additions: int,
        timeline_span: float
    ) -> bool:
        """Assess if development appears incremental."""
        
        # If there are many commits over time, likely incremental
        if len(commits) >= 5 and timeline_span > 1:
            return True
        
        # If additions are spread across commits, likely incremental
        avg_additions_per_commit = total_additions / len(commits) if commits else 0
        
        # Check if most commits are relatively small (< 50 lines)
        small_commits = sum(1 for c in commits if (c.additions + c.deletions) < 50)
        small_commit_ratio = small_commits / len(commits) if commits else 0
        
        if small_commit_ratio > 0.6:
            return True
        
        return False

    @staticmethod
    def _identify_unusual_patterns(
        commits: List,
        commit_intervals: List[float],
        large_commits: List
    ) -> List[str]:
        """Identify potentially unusual or suspicious patterns."""
        
        patterns = []
        
        # Pattern 1: All work done in single commit
        if len(commits) == 1:
            patterns.append("All code added in a single commit - no incremental development")
        
        # Pattern 2: Very large initial commit
        if commits and (commits[0].additions + commits[0].deletions) > 500:
            patterns.append("Very large initial commit suggests bulk code addition")
        
        # Pattern 3: Commits very close together (within minutes)
        rapid_commits = [i for i in commit_intervals if i < 1]  # Within 1 hour
        if len(rapid_commits) > len(commit_intervals) * 0.5:
            patterns.append("Unusually rapid commits (many within hours) may suggest batching")
        
        # Pattern 4: Long gaps between commits
        long_gaps = [i for i in commit_intervals if i > 48]  # Longer than 2 days
        if long_gaps:
            patterns.append(f"Extended gaps in development ({len(long_gaps)} gaps > 48 hours)")
        
        # Pattern 5: Many large commits
        if len(large_commits) > len(commits) * 0.6:
            patterns.append("Most commits are large - suggests batching rather than incremental development")
        
        # Pattern 6: Work only during certain hours (would need timezone analysis)
        # For now, we note it as a potential pattern
        if commits and len(commits) > 3:
            # Check if commits have unusual timezone patterns
            hours = [c.timestamp.hour for c in commits]
            if len(set(hours)) == 1:
                patterns.append(f"All commits at same hour ({hours[0]:02d}:00) - may indicate batching")
        
        return patterns

    @staticmethod
    def _generate_timeline_analysis(
        commit_count: int,
        timeline_span: float,
        is_incremental: bool,
        unusual_patterns: List[str],
        total_additions: int
    ) -> str:
        """Generate human-readable timeline analysis."""
        
        analysis = f"Timeline analysis: {commit_count} commits over {timeline_span:.1f} days.\n"
        
        if timeline_span == 0:
            analysis += "All commits made on the same day.\n"
        else:
            avg_per_day = commit_count / timeline_span if timeline_span > 0 else 0
            analysis += f"Average: {avg_per_day:.1f} commits per day.\n"
        
        if is_incremental:
            analysis += "Development appears incremental with regular commits.\n"
        else:
            analysis += "Development does not show clear incremental pattern.\n"
        
        analysis += f"Total code additions: {total_additions} lines.\n"
        
        if unusual_patterns:
            analysis += "\nUnusual patterns detected:\n"
            for pattern in unusual_patterns:
                analysis += f"  • {pattern}\n"
            analysis += "\nThese patterns may warrant further investigation.\n"
        else:
            analysis += "No highly unusual patterns detected in commit history.\n"
        
        return analysis

    @staticmethod
    def compare_timelines(
        submission1_timeline: Dict[str, Any],
        submission2_timeline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare timelines between two submissions."""
        
        # Get the actual submission from timeline data
        submission1_id = submission1_timeline.get("submission_id")
        submission2_id = submission2_timeline.get("submission_id")
        
        # Check for suspicious temporal relationships
        suspicious_temporal = []
        
        if (submission1_timeline.get("has_history") and 
            submission2_timeline.get("has_history")):
            
            # Check if one submission's timeline is suspiciously similar to the other's
            commits1 = submission1_timeline.get("commits", [])
            commits2 = submission2_timeline.get("commits", [])
            
            if commits1 and commits2:
                # Check if commits are at same times
                times1 = set(c["timestamp"] for c in commits1)
                times2 = set(c["timestamp"] for c in commits2)
                
                common_times = len(times1 & times2)
                if common_times > len(commits1) * 0.3:
                    suspicious_temporal.append(
                        f"Both submissions have commits at {common_times} common timestamps"
                    )
                
                # Check if one is a subset of the other's timeline
                if submission1_timeline.get("total_additions") > submission2_timeline.get("total_additions") * 0.8:
                    if submission2_timeline.get("total_additions") > submission1_timeline.get("total_additions") * 0.8:
                        suspicious_temporal.append("Similar amounts of code added in similar timeframes")
        
        return {
            "submission1_id": submission1_id,
            "submission2_id": submission2_id,
            "timeline1": submission1_timeline,
            "timeline2": submission2_timeline,
            "suspicious_temporal_patterns": suspicious_temporal,
            "both_incremental": (
                submission1_timeline.get("incremental_development", False) and
                submission2_timeline.get("incremental_development", False)
            ),
            "summary": f"Submissions have {len(suspicious_temporal)} suspicious temporal patterns in common."
        }
