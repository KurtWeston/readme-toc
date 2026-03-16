"""CLI interface for readme-toc."""
import argparse
import sys
from pathlib import Path
from . import __version__
from .parser import parse_headers, assign_anchors, generate_toc
from .updater import insert_toc, remove_toc_section


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Auto-generate table of contents for README.md files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', nargs='?', help='Markdown file to process (or use stdin)')
    parser.add_argument('--depth', type=int, default=6, help='Maximum heading level (1-6)')
    parser.add_argument('--start-marker', default='<!-- toc -->', help='TOC start marker')
    parser.add_argument('--end-marker', default='<!-- tocstop -->', help='TOC end marker')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        if args.file:
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"Error: File '{args.file}' not found", file=sys.stderr)
                return 1
            content = file_path.read_text(encoding='utf-8')
        else:
            content = sys.stdin.read()
        
        if not content.strip():
            print("Error: Empty input", file=sys.stderr)
            return 1
        
        clean_content = remove_toc_section(content)
        headers = parse_headers(clean_content, args.depth)
        
        if not headers:
            print("Warning: No headers found", file=sys.stderr)
            return 0
        
        assign_anchors(headers)
        toc = generate_toc(headers)
        updated_content = insert_toc(content, toc, args.start_marker, args.end_marker)
        
        if args.dry_run:
            print(updated_content)
        elif args.file:
            file_path.write_text(updated_content, encoding='utf-8')
            print(f"TOC updated in {args.file}")
        else:
            print(updated_content)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
