#!/usr/bin/env python3
"""
Convert SVG files to PDF for LaTeX inclusion
Uses reportlab or falls back to subprocess with Inkscape/cairosvg
"""

import os
import subprocess
import sys

def convert_with_inkscape(svg_path, pdf_path):
    """Convert SVG to PDF using Inkscape"""
    try:
        # Try new Inkscape syntax (1.0+)
        result = subprocess.run(['inkscape', '--export-type=pdf', f'--export-filename={pdf_path}', svg_path], 
                              check=True, capture_output=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try old Inkscape syntax (<1.0)
            subprocess.run(['inkscape', '--export-pdf', pdf_path, svg_path], 
                          check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def convert_with_cairosvg(svg_path, pdf_path):
    """Convert SVG to PDF using cairosvg"""
    try:
        import cairosvg
        cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
        return True
    except (ImportError, Exception):
        return False

def convert_svg_to_pdf(svg_path):
    """Convert SVG to PDF using available tool"""
    pdf_path = svg_path.replace('.svg', '.pdf')
    
    if os.path.exists(pdf_path):
        print(f"PDF already exists: {pdf_path}")
        return True
    
    print(f"Converting {svg_path} -> {pdf_path}...")
    
    # Try Inkscape first
    if convert_with_inkscape(svg_path, pdf_path):
        print(f"  ✓ Converted with Inkscape")
        return True
    
    # Try cairosvg
    if convert_with_cairosvg(svg_path, pdf_path):
        print(f"  ✓ Converted with cairosvg")
        return True
    
    print(f"  ✗ Failed: No converter available")
    print(f"  Install Inkscape or cairosvg:")
    print(f"    - Inkscape: brew install inkscape")
    print(f"    - cairosvg: pip install cairosvg")
    return False

def main():
    figures_dir = "figures"
    if not os.path.exists(figures_dir):
        print(f"Error: {figures_dir} directory not found")
        return
    
    svg_files = [f for f in os.listdir(figures_dir) if f.endswith('.svg')]
    
    if not svg_files:
        print(f"No SVG files found in {figures_dir}")
        return
    
    print(f"Found {len(svg_files)} SVG files")
    print()
    
    success_count = 0
    for svg_file in sorted(svg_files):
        svg_path = os.path.join(figures_dir, svg_file)
        if convert_svg_to_pdf(svg_path):
            success_count += 1
    
    print()
    print(f"Converted {success_count}/{len(svg_files)} files")
    
    if success_count < len(svg_files):
        print("\nNote: Some files could not be converted.")
        print("For LaTeX compilation, you can:")
        print("1. Install Inkscape: brew install inkscape")
        print("2. Install cairosvg: pip install cairosvg")
        print("3. Or manually convert SVGs to PDF using online tools")

if __name__ == "__main__":
    main()

