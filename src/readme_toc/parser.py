"""Markdown header parsing and TOC generation."""
import re
from typing import List, Tuple, Dict


class Header:
    def __init__(self, level: int, text: str, line_num: int):
        self.level = level
        self.text = text
        self.line_num = line_num
        self.anchor = ""


def parse_headers(content: str, max_depth: int = 6) -> List[Header]:
    """Extract headers from markdown content."""
    headers = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            if level <= max_depth:
                text = match.group(2).strip()
                headers.append(Header(level, text, i))
    
    return headers


def generate_anchor(text: str) -> str:
    """Generate GitHub-compatible anchor from header text."""
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'[\s_]+', '-', anchor)
    anchor = anchor.strip('-')
    return anchor


def assign_anchors(headers: List[Header]) -> None:
    """Assign unique anchors to headers, handling duplicates."""
    anchor_counts: Dict[str, int] = {}
    
    for header in headers:
        base_anchor = generate_anchor(header.text)
        
        if base_anchor not in anchor_counts:
            anchor_counts[base_anchor] = 0
            header.anchor = base_anchor
        else:
            anchor_counts[base_anchor] += 1
            header.anchor = f"{base_anchor}-{anchor_counts[base_anchor]}"


def generate_toc(headers: List[Header]) -> str:
    """Generate table of contents from headers."""
    if not headers:
        return ""
    
    min_level = min(h.level for h in headers)
    toc_lines = []
    
    for header in headers:
        indent = "  " * (header.level - min_level)
        toc_lines.append(f"{indent}- [{header.text}](#{header.anchor})")
    
    return "\n".join(toc_lines)
