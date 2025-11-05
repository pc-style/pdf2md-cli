# Installation & Setup Guide

## Quick Start with `uv tool install`

The easiest way to install and use pdf2md:

```bash
# From local directory
uv tool install /Users/pcstyle/Documents/studia/podstawy_prog/kolos

# Or from git repository
uv tool install git+https://github.com/yourusername/pdf2md.git
```

After installation, the `pdf2md` command will be available globally:

```bash
pdf2md document.pdf
pdf2md document.pdf --mode ai
pdf2md /path/to/pdfs --mode ai --api-key "YOUR_KEY"
```

## Alternative: Direct Installation

### Using pip
```bash
cd /Users/pcstyle/Documents/studia/podstawy_prog/kolos
pip install -r requirements.txt
python pdf2md.py document.pdf
```

### Development installation
```bash
cd /Users/pcstyle/Documents/studia/podstawy_prog/kolos
pip install -e .
pdf2md document.pdf
```

## Configuration

### Set Gemini API Key

For AI mode, you need a Google Gemini API key. Get one from:
https://aistudio.google.com/app/apikeys

Then configure it:

```bash
# Option 1: Environment variable (recommended)
export GEMINI_API_KEY="your-api-key-here"
pdf2md document.pdf --mode ai

# Option 2: Pass as argument
pdf2md document.pdf --mode ai --api-key "your-api-key-here"

# Option 3: Edit pdf2md.py (not recommended)
# Open pdf2md.py and set:
# HARDCODED_API_KEY = "your-api-key-here"
```

## Project Structure

```
pdf2md/
├── pyproject.toml       # Project configuration (for uv and pip)
├── requirements.txt     # Dependencies list
├── pdf2md.py           # Main CLI tool
├── README.md           # User documentation
├── INSTALL.md          # This file
└── lab01/
    └── pp_lista01_2025_2026.pdf  # Example PDF
```

## What's Inside

### `pyproject.toml`
- Defines project metadata
- Specifies entry point: `pdf2md = "pdf2md:main"`
- Lists dependencies with version constraints
- Enables installation via `pip install .` or `uv tool install`

### `pdf2md.py`
- Single-file CLI tool with two modes:
  - **Standalone**: Extracts text using PyMuPDF
  - **AI**: Uses Gemini 2.5 Flash for formatting
- Features:
  - Batch processing (single file or directory recursion)
  - Multiple API key sources
  - Error handling and terminal feedback
  - Custom output paths

### `requirements.txt`
- For pip users who don't want to use uv
- Specifies minimum versions for dependencies

## Dependencies

- **pymupdf** (>=1.23.0) - Fast PDF text extraction
- **google-genai** (>=0.5.0) - Modern Gemini API client
- **python-dotenv** (>=1.0.0) - Environment variable management

## Troubleshooting

### "command not found: pdf2md"
Make sure you installed with `uv tool install` and not just `pip install -r requirements.txt`

### "ERROR: google-genai not installed"
Install the package:
```bash
pip install google-genai
# or with uv
uv tool install --with-editable .
```

### "ERROR: AI mode requires API key"
Set the `GEMINI_API_KEY` environment variable:
```bash
export GEMINI_API_KEY="your-key"
```

### API Rate Limits
If you hit rate limits, add delays between files or use standalone mode for batch processing.

## Running Tests

```bash
# Standalone mode (no API key needed)
pdf2md lab01/pp_lista01_2025_2026.pdf

# AI mode (requires API key)
export GEMINI_API_KEY="your-key"
pdf2md lab01/pp_lista01_2025_2026.pdf --mode ai

# Batch processing
pdf2md lab01/ --mode ai
```

