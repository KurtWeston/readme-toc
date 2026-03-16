"""TOC insertion and update functionality."""
import re
from typing import Optional, Tuple


def find_toc_markers(content: str, start_marker: str, end_marker: str) -> Optional[Tuple[int, int]]:
    """Find TOC marker positions in content."""
    lines = content.split('\n')
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if start_marker in line and start_idx is None:
            start_idx = i
        elif end_marker in line and start_idx is not None:
            end_idx = i
            break
    
    if start_idx is not None and end_idx is not None:
        return (start_idx, end_idx)
    return None


def insert_toc(content: str, toc: str, start_marker: str, end_marker: str) -> str:
    """Insert or update TOC in content."""
    markers = find_toc_markers(content, start_marker, end_marker)
    lines = content.split('\n')
    
    if markers:
        start_idx, end_idx = markers
        new_lines = lines[:start_idx + 1] + ['', toc, ''] + lines[end_idx:]
        return '\n'.join(new_lines)
    else:
        toc_block = f"{start_marker}\n\n{toc}\n\n{end_marker}"
        return toc_block + '\n\n' + content


def remove_toc_section(content: str) -> str:
    """Remove content between TOC markers for parsing."""
    markers = find_toc_markers(content, '<!-- toc -->', '<!-- tocstop -->')
    if not markers:
        return content
    
    lines = content.split('\n')
    start_idx, end_idx = markers
    filtered_lines = lines[:start_idx] + lines[end_idx + 1:]
    return '\n'.join(filtered_lines)
