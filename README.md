# PDF to Markdown Converter

A Python CLI tool that converts PDFs to nicely formatted markdown files with two modes:
- **Standalone**: Direct extraction using PyMuPDF
- **AI**: Enhanced formatting using Google Gemini 2.5 Flash API

## Installation

### Using uv (recommended)
```bash
uv tool install git+https://github.com/yourusername/pdf2md.git
```

Or install from local directory:
```bash
uv tool install /path/to/pdf2md
```

### Using pip
```bash
pip install -r requirements.txt
```

### Development install
```bash
pip install -e .
```

## Usage

### Basic usage (standalone mode)
```bash
python pdf2md.py document.pdf
```

Outputs: `document.md` in the same directory.

### AI-powered formatting
```bash
python pdf2md.py document.pdf --mode ai
```

Requires `GEMINI_API_KEY` environment variable to be set:
```bash
export GEMINI_API_KEY="your-api-key-here"
python pdf2md.py document.pdf --mode ai
```

Or pass it directly:
```bash
python pdf2md.py document.pdf --mode ai --api-key "your-api-key-here"
```

### Batch processing (directory)
```bash
python pdf2md.py /path/to/pdf/folder
python pdf2md.py /path/to/pdf/folder --mode ai
```

Processes all PDFs recursively, maintains directory structure.

### Specify output file
```bash
python pdf2md.py document.pdf --output my_output.md
```

## Options

- `--mode {standalone,ai}` - Conversion mode (default: standalone)
- `--output PATH` - Output file path (auto-generated if not provided)
- `--api-key KEY` - Gemini API key (overrides env variable)

## API Key Configuration

The tool looks for API key in this order:
1. `--api-key` command-line argument
2. `GEMINI_API_KEY` environment variable
3. Hardcoded value in `pdf2md.py` (if set)

## Requirements

- Python 3.8+
- PyMuPDF (pymupdf) - PDF extraction
- google-genai - Gemini API (optional, only for AI mode)
- python-dotenv - Environment variable management (optional)

## API Integration

This tool uses the modern **Google GenAI SDK** (`google-genai`) instead of the deprecated `google-generativeai`.

### Key Features:
- Uses `genai.Client()` for initialization
- Supports Gemini 2.5 Flash model
- Proper error handling with `genai.errors.APIError`
- Streaming support for large responses
- Automatic environment variable configuration

### API Key Setup
```bash
# Option 1: Environment variable (recommended)
export GEMINI_API_KEY="your-api-key"

# Option 2: Pass via CLI
pdf2md document.pdf --mode ai --api-key "your-api-key"

# Option 3: Hardcode in pdf2md.py (not recommended for production)
# Edit the HARDCODED_API_KEY variable in pdf2md.py
```

