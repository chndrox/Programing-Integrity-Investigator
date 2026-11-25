import json
import logging
from typing import Optional, Dict, Any
from groq import Groq
from app.database import settings
import asyncio

logger = logging.getLogger(__name__)


class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
        self.timeout = settings.agent_timeout_seconds

    async def analyze_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Call Groq API for text analysis.
        Returns the response as parsed JSON if json_mode is True.
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Run the API call in a timeout
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    self._make_request,
                    messages,
                    temperature
                ),
                timeout=self.timeout
            )
            
            return response
        
        except asyncio.TimeoutError:
            logger.error("Groq API request timed out")
            raise Exception("Groq API request timed out")
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise

    def _make_request(self, messages: list, temperature: float) -> Dict[str, Any]:
        """Synchronous wrapper for Groq API call."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=4096
        )
        
        content = response.choices[0].message.content
        
        # Try to parse as JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"text": content, "raw": content}

    async def analyze_code_similarity(self, code1: str, code2: str) -> Dict[str, Any]:
        """Analyze code similarity using Groq."""
        prompt = f"""Analyze the similarity between these two code snippets.
        
Code 1:
{code1}

Code 2:
{code2}

Provide analysis in JSON format with:
- similarity_percentage (0-100)
- similar_patterns (list of similar patterns found)
- key_differences (list of key differences)
- confidence_level (high, medium, low)
- analysis_notes
"""
        
        system_prompt = "You are an expert code similarity analyzer. Analyze code snippets carefully and provide detailed JSON responses."
        
        return await self.analyze_text(prompt, system_prompt)

    async def analyze_timeline_suspicious(
        self,
        timeline_data: str,
        code_volume: int,
        timeline_span: float
    ) -> Dict[str, Any]:
        """Analyze commit timeline for suspicious patterns."""
        prompt = f"""Analyze this commit timeline for suspicious patterns:

Timeline Data:
{timeline_data}

Total Code Added: {code_volume} lines
Timeline Span: {timeline_span} days

Provide analysis in JSON format with:
- suspicious_patterns (list of concerning patterns)
- incremental_development_evidence (how well does development appear incremental)
- timeline_consistency (consistent, irregular, suspicious)
- red_flags (list of any red flags)
- confidence_level (high, medium, low)
- analyst_notes
"""
        
        system_prompt = "You are an expert development timeline analyst. Analyze commit patterns and development progression."
        
        return await self.analyze_text(prompt, system_prompt)

    async def generate_exculpatory_analysis(
        self,
        similarity_findings: str,
        timeline_findings: str,
        code_analysis: str
    ) -> Dict[str, Any]:
        """Generate exculpatory evidence and alternative explanations."""
        prompt = f"""Review these investigation findings and provide exculpatory evidence and alternative explanations:

Similarity Findings:
{similarity_findings}

Timeline Findings:
{timeline_findings}

Code Analysis:
{code_analysis}

Provide analysis in JSON format with:
- potential_explanations (list of legitimate explanations for similarities)
- exculpatory_evidence (evidence supporting independent development)
- common_patterns_explanation (why these patterns might be common)
- missing_evidence (what evidence is missing for fair judgment)
- questions_for_instructor (list of clarifying questions)
- analyst_confidence (high, medium, low)
- student_defense_summary
"""
        
        system_prompt = "You are a critical analyst representing the student's perspective. Find legitimate explanations and evidence supporting independent work."
        
        return await self.analyze_text(prompt, system_prompt)

    async def generate_case_report(
        self,
        similarity_analysis: str,
        timeline_analysis: str,
        exculpatory_analysis: str,
        investigation_context: str
    ) -> Dict[str, Any]:
        """Generate a comprehensive case report."""
        prompt = f"""Based on these investigation findings, generate a comprehensive case report:

Investigation Context:
{investigation_context}

Similarity Analysis:
{similarity_analysis}

Timeline Analysis:
{timeline_analysis}

Exculpatory Analysis:
{exculpatory_analysis}

Generate a report in JSON format with:
- executive_summary (brief overview)
- key_findings (list of main findings)
- supporting_evidence (evidence suggesting plagiarism)
- contradictory_evidence (evidence against plagiarism)
- conflicting_opinions (where agents disagree)
- evidence_gaps (missing information)
- confidence_assessment (how confident should the instructor be)
- recommended_actions (what the instructor should do next)
- limitations (limitations of this analysis)
- case_summary (neutral summary for instructor review)
"""
        
        system_prompt = "You are a neutral case report writer. Synthesize all findings into a balanced, evidence-based report without making accusations."
        
        return await self.analyze_text(prompt, system_prompt)


# Singleton instance
_groq_service: Optional[GroqService] = None


def get_groq_service() -> GroqService:
    global _groq_service
    if _groq_service is None:
        _groq_service = GroqService()
    return _groq_service
