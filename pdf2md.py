#!/usr/bin/env python3
"""
pdf2md - Convert PDFs to Markdown
Supports standalone extraction or AI-powered formatting via Gemini API
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional
import fitz  # pymupdf

# try to import google genai SDK, optional for standalone mode
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# hardcoded API key fallback (nie pytaj czemu xD)
HARDCODED_API_KEY = ""


def clear_buffer():
    """clear terminal output"""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner(text):
    """draw a small banner"""
    print(f"\n{'=' * 50}")
    print(f"  {text}")
    print(f"{'=' * 50}\n")


def get_api_key(provided_key: Optional[str] = None) -> Optional[str]:
    """get API key from various sources"""
    # priority: provided > env var > hardcoded
    if provided_key:
        return provided_key
    
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        return env_key
    
    if HARDCODED_API_KEY:
        return HARDCODED_API_KEY
    
    return None


def extract_pdf_text(pdf_path: str) -> str:
    """
    extract text from PDF using pymupdf
    preserves some basic structure (pages, headings)
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = []
        
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                full_text.append(f"## Page {page_num}\n")
                full_text.append(text)
                full_text.append("\n")
        
        doc.close()
        return "\n".join(full_text)
    
    except Exception as e:
        print(f"ERROR: nie mogę otworzyć {pdf_path}: {e}")
        return ""


def format_with_gemini(text: str, api_key: str) -> str:
    """
    send extracted text to Gemini for AI formatting
    uses gemini-2.5-flash model with the new Google GenAI SDK
    """
    if not GEMINI_AVAILABLE:
        print("ERROR: google-genai not installed, use --mode standalone")
        return text
    
    try:
        # create client with API key
        client = genai.Client(api_key=api_key)
        
        prompt = f"""Convert the following raw PDF text into well-formatted markdown.
Rules:
- Use appropriate heading levels
- Format lists properly
- Preserve code blocks if present
- Add proper spacing
- Make it readable and well-structured

Raw text:
{text}"""
        
        # generate content using new SDK
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    
    except Exception as e:
        print(f"ERROR: Gemini formatting failed: {e}")
        return text


def save_markdown(content: str, output_path: str) -> bool:
    """save markdown content to file"""
    try:
        # create parent directories if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    except Exception as e:
        print(f"ERROR: nie mogę zapisać {output_path}: {e}")
        return False


def process_single_file(
    input_path: str,
    output_path: Optional[str],
    mode: str,
    api_key: Optional[str] = None
) -> bool:
    """
    process a single PDF file
    """
    print(f"Processing: {input_path}")
    
    # extract text
    wynik = extract_pdf_text(input_path)
    if not wynik:
        print("Extraction failed, skipping...")
        return False
    
    # format based on mode
    if mode == 'ai':
        if not api_key:
            print("ERROR: AI mode requires API key (set GEMINI_API_KEY or use --api-key)")
            return False
        
        print("Formatting with Gemini...")
        wynik = format_with_gemini(wynik, api_key)
    
    # determine output path
    if not output_path:
        pdf_stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{pdf_stem}.md")
    
    # save
    if save_markdown(wynik, output_path):
        print(f"✓ Saved: {output_path}\n")
        return True
    
    return False


def process_directory(
    dir_path: str,
    mode: str,
    api_key: Optional[str] = None
) -> int:
    """
    process all PDFs in directory recursively
    returns number of successfully converted files
    """
    print_banner(f"Processing directory: {dir_path}")
    
    pdf_files = list(Path(dir_path).rglob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found.")
        return 0
    
    print(f"Found {len(pdf_files)} PDF files\n")
    
    success_count = 0
    for pdf_file in pdf_files:
        # output in same directory, same name but .md
        output_file = pdf_file.with_suffix('.md')
        
        if process_single_file(str(pdf_file), str(output_file), mode, api_key):
            success_count += 1
    
    print(f"\nDone! Successfully converted {success_count}/{len(pdf_files)} files")
    return success_count


def parse_args():
    """build CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="Convert PDFs to markdown (standalone or AI-powered)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf2md.py document.pdf
  python pdf2md.py document.pdf --mode ai
  python pdf2md.py /path/to/pdfs --output result.md
  python pdf2md.py docs/ --mode ai --api-key YOUR_KEY
        """
    )
    
    parser.add_argument(
        'input',
        help='PDF file or directory containing PDFs'
    )
    
    parser.add_argument(
        '--mode',
        choices=['standalone', 'ai'],
        default='standalone',
        help='Conversion mode (default: standalone)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (auto-generated if not provided)'
    )
    
    parser.add_argument(
        '--api-key',
        help='Gemini API key (overrides GEMINI_API_KEY env var)'
    )
    
    return parser.parse_args()


def main():
    """main entry point"""
    args = parse_args()
    
    input_path = args.input
    
    # check if input exists
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found")
        sys.exit(1)
    
    # get API key if needed
    api_key = None
    if args.mode == 'ai':
        api_key = get_api_key(args.api_key)
        if not api_key:
            print("ERROR: AI mode requires API key")
            print("Set GEMINI_API_KEY env var or use --api-key flag")
            sys.exit(1)
    
    print_banner("PDF to Markdown Converter")
    print(f"Mode: {args.mode}")
    print(f"Input: {input_path}\n")
    
    # process
    if os.path.isfile(input_path):
        # single file
        success = process_single_file(input_path, args.output, args.mode, api_key)
        sys.exit(0 if success else 1)
    
    elif os.path.isdir(input_path):
        # directory
        if args.output:
            print("WARNING: --output ignored for directory processing")
        
        process_directory(input_path, args.mode, api_key)
        sys.exit(0)
    
    else:
        print(f"ERROR: {input_path} is neither file nor directory")
        sys.exit(1)


if __name__ == '__main__':
    main()

