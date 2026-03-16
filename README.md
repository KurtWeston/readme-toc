# readme-toc

Auto-generate and update table of contents for README.md files by parsing markdown headers

## Features

- Parse markdown files and extract headers (h1-h6) with proper nesting
- Generate GitHub-compatible anchor links from header text (lowercase, spaces to hyphens, special chars removed)
- Create hierarchical table of contents with proper indentation
- Detect existing TOC markers (<!-- toc --> and <!-- tocstop -->) and update in-place
- Insert new TOC at specified location if markers don't exist
- Support configurable depth levels (e.g., only h1-h3)
- Handle duplicate headers by appending numbered suffixes to anchors
- Preserve existing markdown formatting outside TOC section
- CLI flags: --depth (max heading level), --marker (custom TOC markers), --dry-run (preview only)
- Exit with error code if file doesn't exist or isn't valid markdown
- Support reading from stdin and writing to stdout for pipeline usage

## How to Use

Use this project when you need to:

- Quickly solve problems related to readme-toc
- Integrate python functionality into your workflow
- Learn how python handles common patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/readme-toc.git
cd readme-toc

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
