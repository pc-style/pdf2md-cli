# PDF to Markdown Converter (Bun Edition)

A blazing fast CLI tool that converts PDFs to nicely formatted markdown files. Rebuilt with [Bun](https://bun.sh) for speed and ease of use.

## Features

- **Blazing Fast**: Built on Bun.
- **AI-Powered**: Uses Google Gemini 3 Flash Preview for intelligent formatting.
- **Standalone Mode**: Quick raw text extraction.
- **Bulk Processing**: Convert entire directories recursively.
- **Configurable**: Persist your API key so you don't have to type it every time.

## Installation

### Prerequisites

- [Bun](https://bun.sh)

### Setup

1.  Clone the repo:
    ```bash
    git clone https://github.com/pc-style/pdf2md-cli.git
    cd pdf2md-cli
    ```
2.  Install dependencies:
    ```bash
    bun install
    ```
3.  Build the binary:
    ```bash
    bun run build
    ```

### Global Installation

To install the tool globally on your system:

```bash
bun install -g .
```

This will make the `pdf2md` command available anywhere.

## Usage

### 1. Configure API Key (One-time setup)

To use the AI features, set your Gemini API key:

```bash
./pdf2md config --key YOUR_API_KEY
```

To remove it later: `pdf2md config --delete`

### 2. Convert a PDF

**AI Mode (Recommended for formatting):**
```bash
./pdf2md document.pdf --mode ai
```

**Standalone Mode (Raw text only):**
```bash
./pdf2md document.pdf
```

### 3. Bulk Conversion

Convert all PDFs in a directory:

```bash
./pdf2md ./my-docs/ --mode ai
```

## License

MIT