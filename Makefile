# Makefile for LaTeX document compilation

LATEX=pdflatex
BIBTEX=bibtex
MAIN=assessment

.PHONY: all clean view

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex
	@echo "PDF generated: $(MAIN).pdf"

clean:
	rm -f *.aux *.log *.out *.toc *.pdf

view: $(MAIN).pdf
	open $(MAIN).pdf

help:
	@echo "Available targets:"
	@echo "  all    - Compile PDF (default)"
	@echo "  clean  - Remove auxiliary files"
	@echo "  view   - Compile and open PDF"
	@echo "  help   - Show this help message"

