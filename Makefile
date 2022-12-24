# Variables
BIBTEX:=bibtex
BIB_DEFS:=tex/strings.bib
BIB_FILE:=tex/nwit.bib
DATA:=_data/authors.yml _data/categories.yml _includes/bibliography.html tex/nwit.pdf
JEKYLL:=bundle exec jekyll
LATEX:=pdflatex
POSTS:=$(wildcard _posts/*/*.html) $(wildcard _posts/*/*.md)
TEX_SHRAPNEL=tex/nwit.aux tex/nwit.bbl tex/nwit.blg tex/nwit.log

# By default, show available commands
.DEFAULT: commands

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
.PHONY: build
build: ${DATA}
	${JEKYLL} build

## serve: build site and run server
.PHONY: serve
serve: ${DATA}
	${JEKYLL} serve

## data: rebuild data files and bibliography
.PHONY: data
data: ${DATA}

_includes/bibliography.html: bin/bib_to_html.py ${BIB_FILE} ${BIB_DEFS}
	@python bin/bib_to_html.py --bib ${BIB_FILE} --strings ${BIB_DEFS} > $@

_data/authors.yml: bin/authors.py ${BIB_FILE} ${BIB_DEFS} tex/unreviewed.txt
	@mkdir -p _data
	@python bin/authors.py --bib ${BIB_FILE} --strings ${BIB_DEFS} --unreviewed tex/unreviewed.txt > $@

_data/categories.yml: bin/categories.py $(POSTS)
	@mkdir -p _data
	@python bin/categories.py --prefix _posts $(POSTS) > $@

tex/nwit.pdf: ${BIB_FILE} ${BIB_DEF} tex/nwit.tex tex/settings.tex tex/abstract.bst
	@rm -f ${TEX_SHRAPNEL}
	@cd tex \
	&& ${LATEX} nwit \
	&& ${BIBTEX} nwit \
	&& ${LATEX} nwit \
	&& ${LATEX} nwit

## pdf: make the PDF version of the bibliography
.PHONY: pdf
pdf: tex/nwit.pdf

## sterile: clean up everything for a complete rebuild
.PHONY: sterile
sterile: clean
	@rm -f ${DATA}

## clean: clean up temporary files
.PHONY: clean
clean:
	@rm -rf _site
	@find . -name '*~' -print | xargs rm -f
	@rm -f ${TEX_SHRAPNEL}

## settings: show settings
.PHONY: settings
settings:
	@echo "BIBTEX =" ${BIBTEX}
	@echo "BIB_FILE =" ${BIB_FILE}
	@echo "BIB_DEFS =" ${BIB_DEFS}
	@echo "DATA =" ${DATA}
	@echo "JEKYLL =" ${JEKYLL}
	@echo "LATEX =" ${LATEX}
	@echo "POSTS =" ${POSTS}
	@echo "TEX_SHRAPNEL =" ${TEX_SHRAPNEL}
