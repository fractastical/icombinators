#!/bin/bash
# Convert SVG figures to PDF for LaTeX inclusion
# Requires Inkscape or cairosvg

FIGURES_DIR="figures"
OUTPUT_DIR="figures"

echo "Converting SVG figures to PDF..."

# Check for Inkscape
if command -v inkscape &> /dev/null; then
    echo "Using Inkscape..."
    for svg in "$FIGURES_DIR"/*.svg; do
        if [ -f "$svg" ]; then
            pdf="${svg%.svg}.pdf"
            inkscape --export-pdf="$pdf" "$svg" 2>/dev/null
            echo "Converted: $(basename $svg) -> $(basename $pdf)"
        fi
    done
# Check for cairosvg
elif command -v cairosvg &> /dev/null; then
    echo "Using cairosvg..."
    for svg in "$FIGURES_DIR"/*.svg; do
        if [ -f "$svg" ]; then
            pdf="${svg%.svg}.pdf"
            cairosvg "$svg" -o "$pdf"
            echo "Converted: $(basename $svg) -> $(basename $pdf)"
        fi
    done
else
    echo "Error: Neither Inkscape nor cairosvg found."
    echo "Install one of:"
    echo "  - Inkscape: brew install inkscape (macOS) or apt-get install inkscape (Linux)"
    echo "  - cairosvg: pip install cairosvg"
    exit 1
fi

echo "Done! PDF files created in $OUTPUT_DIR/"

