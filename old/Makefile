JEKYLL=bundle exec jekyll
SITE=./_site

ABSTRACT_BIN=./bin/abstracts.sh
AUTHORS_BIN=./bin/authors.py
BIB2YAML_BIN=./bin/bib2yaml.py
YAML2HTML_BIN=./bin/yaml2html.py
YEARS_BIN=./bin/years.py
BIBTEX_BIN=bibtex
LATEX_BIN=pdflatex

STRINGS_BIB=./tex/strings.bib
NWIT_BIB=./tex/nwit.bib
TODO_BIB=./tex/todo.bib
ALL_BIB=${STRINGS_BIB} ${NWIT_BIB} ${TODO_BIB}
UNREVIEWED_TXT=./tex/unreviewed.txt

STRINGS_OPTION=--strings ./tex/strings.bib

AUTHORS_HTML=authors/index.html
BIB_HTML=bib/index.html
TODO_HTML=todo/index.html
YEARS_SVG=files/years-histogram.svg
SUPPORT_FILES=${AUTHORS_HTML} ${BIB_HTML} ${TODO_HTML} ${YEARS_SVG}

PDF=tex/nwit.pdf

CONFIG=_config.yml
INCLUDES=$(wildcard _includes/*.html)
LAYOUTS=$(wildcard _layouts/*.html)
POSTS=$(wildcard _posts/*/*.md)
PAGES=\
	atom.xml\
	index.html\
	about/index.html\
	bycategory/index.html\
	bydate/index.html\
	contributing/index.html
STYLES=$(wildcard _sass/*/*.scss) $(wildcard css/*.css) $(wildcard css/*.scss)

.DEFAULT: commands

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
build: ${SUPPORT_FILES} ${PDF}
	${JEKYLL} build

## serve: build site and run server
serve: ${SUPPORT_FILES}
	${JEKYLL} serve

# ---

## authors: cross-reference authors and bibliography entries
authors: ${AUTHORS_HTML}

## pdf: re-create PDF version of bibliography
pdf: ${PDF}

## bib: re-create HTML bibliography of reviewed articles
bib: ${BIB_HTML}

## todo: re-create HTML bibliography of upcoming articles
todo: ${TODO_HTML}

## years: regenerate plot of publication years of reviewed articles
years: ${YEARS_SVG}

## ----

## abstract: get abstract from DOI (DOI=value)
abstract:
	@${ABSTRACT_BIN} ${DOI}

## entry: convert single entry (KEY=NameYear) to HTML
entry:
	@cat ${STRINGS_BIB} ${NWIT_BIB} ${TODO_BIB} | bin/entry.py ${KEY} _template.html

## pick: select a random entry from the to-do list (YEAR=yyyy optional)
pick:
	bin/list.py ${STRINGS_OPTION} --input ${TODO_BIB} --random --year ${YEAR}

## show: show all entries from the to-do list in chronological order (YEAR=yyyy optional)
show:
	bin/list.py ${STRINGS_OPTION} --input ${TODO_BIB} --year ${YEAR}

## ----

## categories: list files by category
categories:
	@bin/categories.py _posts/*/*.html

## check: run all checks
check:
	@make check-ascii
	@make check-bib
	@make check-dates
	@make check-used

## check-ascii: check that all .bib files are 7-bit ASCII
check-ascii:
	@bin/check-ascii.py --inputs ${NWIT_BIB} ${TODO_BIB}


## check-bib: check integrity of bibliography
check-bib:
	@bin/check-bib.py ${STRINGS_OPTION} --inputs ${NWIT_BIB} ${TODO_BIB}

## check-dates: make sure the dates in posts line up with filenames
check-dates:
	@bin/check-dates.py --root _posts

## check-pdf: check that PDFs exist (use PDFDIR=<path>)
check-pdf:
	@bin/check-pdf.py ${STRINGS_OPTION} --inputs ${NWIT_BIB} ${TODO_BIB} --pdfdir ${PDFDIR}

## check-used: check which papers have been used or not
check-used:
	@bin/check-used.py --pagedir _posts ${STRINGS_OPTION} --used ${NWIT_BIB} --unreviewed ${UNREVIEWED_TXT}

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -name '*.aux' -exec rm {} \;
	@find . -name '*.bbl' -exec rm {} \;
	@find . -name '*.blg' -exec rm {} \;
	@find . -name '*.log' -exec rm {} \;

## sterile: clean up and erase generated site
sterile:
	@make clean
	@rm -rf ${SITE}

# --------

${AUTHORS_HTML}: ${AUTHORS_BIN} ${NWIT_BIB}
	@mkdir -p authors
	@echo "---" > ${AUTHORS_HTML}
	@echo "layout: page" >> ${AUTHORS_HTML}
	@echo "title: Authors" >> ${AUTHORS_HTML}
	@echo "---" >> ${AUTHORS_HTML}
	@cat ${STRINGS_BIB} ${NWIT_BIB} | ${AUTHORS_BIN} ${UNREVIEWED_TXT} >> ${AUTHORS_HTML}

${BIB_HTML}: ${STRINGS_BIB} ${NWIT_BIB} ${BIB2YAML_BIN} ${YAML2HTML_BIN}
	make TITLE="Bibliography" SLUG=nwit bib2yaml > $@

${TODO_HTML}: ${STRINGS_BIB} ${TODO_BIB} ${BIB2YAML_BIN} ${YAML2HTML_BIN}
	make TITLE="To Do" SLUG=todo bib2yaml > $@

${YEARS_SVG}: ${NWIT_BIB} ${YEARS_BIN}
	${YEARS_BIN} ${STRINGS_OPTION} --input ${NWIT_BIB} --output $@

${PDF}: ${NWIT_BIB} ${TODO_BIB} tex/nwit.tex tex/settings.tex tex/abstract.bst
	@cd tex \
	&& rm -f nwit.aux nwit.bbl \
	&& ${LATEX_BIN} nwit \
	&& ${BIBTEX_BIN} nwit \
	&& ${LATEX_BIN} nwit \
	&& ${LATEX_BIN} nwit

bib2yaml:
	@mkdir -p ${SLUG}
	@echo "---"
	@echo "layout: page"
	@echo "title: ${TITLE}"
	@echo "---"
	@echo '<p><a href="../tex/${SLUG}.bib">BibTeX</a> | <a href="../tex/${SLUG}.pdf">PDF</a></p>'
	@cat ./tex/${SLUG}.bib | ${BIB2YAML_BIN} ${STRINGS_OPTION} | ${YAML2HTML_BIN}
