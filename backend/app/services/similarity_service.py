import ast
import logging
from typing import List, Dict, Tuple, Any
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)


class SimilarityService:
    """
    Deterministic code similarity analysis without relying on LLM.
    Uses token-based, AST-based, and line-based comparison.
    """

    @staticmethod
    def tokenize_code(code: str) -> List[str]:
        """Convert code to tokens for comparison."""
        # Remove comments and strings, then tokenize
        tokens = []
        lines = code.split('\n')
        
        for line in lines:
            # Remove comments
            if '#' in line:
                line = line[:line.index('#')]
            
            # Simple tokenization: split on whitespace and common delimiters
            line_tokens = re.findall(r'\w+|[{}()\[\],;:]|[+\-*/%=<>!&|]', line)
            tokens.extend(line_tokens)
        
        return tokens

    @staticmethod
    def calculate_token_similarity(code1: str, code2: str) -> Tuple[float, List[str]]:
        """Calculate similarity based on token matching."""
        tokens1 = SimilarityService.tokenize_code(code1)
        tokens2 = SimilarityService.tokenize_code(code2)
        
        if not tokens1 or not tokens2:
            return 0.0, []
        
        # Use SequenceMatcher to find matching blocks
        matcher = SequenceMatcher(None, tokens1, tokens2)
        matching_blocks = matcher.get_matching_blocks()
        
        # Calculate similarity
        matching_tokens = sum(block.size for block in matching_blocks)
        total_tokens = max(len(tokens1), len(tokens2))
        similarity = (matching_tokens / total_tokens) * 100 if total_tokens > 0 else 0
        
        # Extract matching token sequences
        matching_sequences = []
        for block in matching_blocks:
            if block.size > 2:  # Only include sequences of 3+ tokens
                seq = ' '.join(tokens1[block.a:block.a + block.size])
                if len(seq) > 10:  # Only include meaningful sequences
                    matching_sequences.append(seq)
        
        return similarity, matching_sequences

    @staticmethod
    def get_ast_nodes(code: str) -> List[str]:
        """Extract AST node types from code."""
        try:
            tree = ast.parse(code)
            nodes = []
            
            for node in ast.walk(tree):
                node_type = node.__class__.__name__
                nodes.append(node_type)
            
            return nodes
        except SyntaxError:
            return []

    @staticmethod
    def calculate_ast_similarity(code1: str, code2: str) -> float:
        """Calculate similarity based on AST structure."""
        nodes1 = SimilarityService.get_ast_nodes(code1)
        nodes2 = SimilarityService.get_ast_nodes(code2)
        
        if not nodes1 or not nodes2:
            return 0.0
        
        matcher = SequenceMatcher(None, nodes1, nodes2)
        matching_blocks = matcher.get_matching_blocks()
        matching_nodes = sum(block.size for block in matching_blocks)
        total_nodes = max(len(nodes1), len(nodes2))
        
        similarity = (matching_nodes / total_nodes) * 100 if total_nodes > 0 else 0
        return similarity

    @staticmethod
    def calculate_line_similarity(code1: str, code2: str) -> Tuple[float, List[Tuple[int, int]]]:
        """Calculate line-by-line similarity."""
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        # Normalize lines (remove whitespace)
        norm_lines1 = [line.strip() for line in lines1 if line.strip()]
        norm_lines2 = [line.strip() for line in lines2 if line.strip()]
        
        matcher = SequenceMatcher(None, norm_lines1, norm_lines2)
        matching_blocks = matcher.get_matching_blocks()
        
        matching_lines = sum(block.size for block in matching_blocks)
        total_lines = max(len(norm_lines1), len(norm_lines2))
        similarity = (matching_lines / total_lines) * 100 if total_lines > 0 else 0
        
        # Get matching line indices
        matching_indices = []
        for block in matching_blocks:
            for i in range(block.size):
                matching_indices.append((block.a + i, block.b + i))
        
        return similarity, matching_indices

    @staticmethod
    def find_matching_blocks(code1: str, code2: str) -> List[Dict[str, Any]]:
        """Find matching code blocks between two files."""
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        norm_lines1 = [line.strip() for line in lines1 if line.strip()]
        norm_lines2 = [line.strip() for line in lines2 if line.strip()]
        
        matcher = SequenceMatcher(None, norm_lines1, norm_lines2)
        matching_blocks = matcher.get_matching_blocks()
        
        blocks = []
        for block in matching_blocks:
            if block.size >= 3:  # Only blocks with 3+ lines
                blocks.append({
                    "file1_start": block.a,
                    "file1_end": block.a + block.size,
                    "file2_start": block.b,
                    "file2_end": block.b + block.size,
                    "size": block.size,
                    "lines": norm_lines1[block.a:block.a + block.size]
                })
        
        return blocks

    @staticmethod
    def extract_function_names(code: str) -> List[str]:
        """Extract function and variable names from code."""
        try:
            tree = ast.parse(code)
            names = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    names.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    names.append(node.name)
                elif isinstance(node, ast.Name):
                    names.append(node.id)
            
            return list(set(names))  # Remove duplicates
        except SyntaxError:
            return []

    @staticmethod
    def calculate_name_overlap(code1: str, code2: str) -> float:
        """Calculate how many names are shared between files."""
        names1 = set(SimilarityService.extract_function_names(code1))
        names2 = set(SimilarityService.extract_function_names(code2))
        
        if not names1 or not names2:
            return 0.0
        
        overlap = len(names1 & names2)
        total = len(names1 | names2)
        
        return (overlap / total) * 100 if total > 0 else 0

    @staticmethod
    def comprehensive_comparison(code1: str, code2: str) -> Dict[str, Any]:
        """
        Perform comprehensive code comparison using multiple metrics.
        Returns a combined analysis without relying on LLM.
        """
        # Calculate different similarity metrics
        token_sim, token_matches = SimilarityService.calculate_token_similarity(code1, code2)
        ast_sim = SimilarityService.calculate_ast_similarity(code1, code2)
        line_sim, matching_indices = SimilarityService.calculate_line_similarity(code1, code2)
        name_overlap = SimilarityService.calculate_name_overlap(code1, code2)
        
        # Get matching blocks
        matching_blocks = SimilarityService.find_matching_blocks(code1, code2)
        
        # Calculate weighted average similarity
        weighted_similarity = (token_sim * 0.3 + ast_sim * 0.2 + line_sim * 0.4 + name_overlap * 0.1)
        
        # Determine confidence level
        if weighted_similarity > 70:
            confidence = "high"
        elif weighted_similarity > 40:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Count unique and matching code
        lines1 = [l.strip() for l in code1.split('\n') if l.strip()]
        lines2 = [l.strip() for l in code2.split('\n') if l.strip()]
        matching_line_count = len(matching_indices)
        unique_lines1 = len(lines1) - matching_line_count
        unique_lines2 = len(lines2) - matching_line_count
        
        return {
            "similarity_percentage": round(weighted_similarity, 2),
            "token_similarity": round(token_sim, 2),
            "ast_similarity": round(ast_sim, 2),
            "line_similarity": round(line_sim, 2),
            "name_overlap": round(name_overlap, 2),
            "confidence_level": confidence,
            "matching_blocks": matching_blocks[:10],  # Top 10 blocks
            "total_matching_blocks": len(matching_blocks),
            "matching_lines": matching_line_count,
            "unique_lines_code1": unique_lines1,
            "unique_lines_code2": unique_lines2,
            "total_lines_code1": len(lines1),
            "total_lines_code2": len(lines2),
            "analysis": self._generate_analysis(weighted_similarity, confidence, matching_blocks)
        }

    @staticmethod
    def _generate_analysis(similarity: float, confidence: str, blocks: List[Dict]) -> str:
        """Generate human-readable analysis."""
        analysis = f"Code similarity analysis shows {similarity:.1f}% weighted similarity with {confidence} confidence.\n"
        
        if blocks:
            analysis += f"Found {len(blocks)} significant matching code blocks.\n"
            analysis += "Common patterns may include standard programming idioms, shared libraries, or similar problem-solving approaches.\n"
        else:
            analysis += "No significant matching code blocks found.\n"
        
        if similarity < 30:
            analysis += "Low similarity suggests independent development."
        elif similarity < 70:
            analysis += "Moderate similarity could result from common patterns or shared resources. Further investigation recommended."
        else:
            analysis += "High similarity warrants detailed investigation of development processes and timelines."
        
        return analysis
