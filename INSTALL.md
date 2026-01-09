# Installation

## Prerequisites

- [Bun](https://bun.sh) (for building from source or running the script directly)

## Global Installation

The easiest way to install is using the provided installation script:

```bash
./install.sh
```

Alternatively, you can do it manually:

1. Clone the repository:
...
```bash
bun install -g .
```
   ```bash
   git clone https://github.com/pc-style/pdf2md-cli.git
   cd pdf2md-cli
   ```

2. Install dependencies:
   ```bash
   bun install
   ```

3. Build the binary:
   ```bash
   bun run build
   ```
   This will create a standalone `pdf2md` executable in the `bin/` directory.

4. (Optional) Move to your PATH:
   ```bash
   mv bin/pdf2md /usr/local/bin/
   ```

## Usage

### Configuration (AI Mode)

To use the AI-powered formatting (Gemini), you need an API Key.

```bash
pdf2md config --key YOUR_GEMINI_API_KEY
```

### Convert a PDF

**Standalone Mode (Fast, extract text only):**
```bash
./pdf2md input.pdf
```

**AI Mode (Smart formatting):**
```bash
./pdf2md input.pdf --mode ai
```

### Bulk Conversion

Process an entire directory of PDFs:

```bash
./pdf2md ./documents/ --mode ai
```

### Help

```bash
./pdf2md --help
```