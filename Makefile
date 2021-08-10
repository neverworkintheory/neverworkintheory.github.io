JEKYLL=bundle exec jekyll
SITE=./_site

AUTHORS_BIN=./bin/authors.py
BIB2HTML_BIN=./bin/bib2html.py
LATEX_BIN=pdflatex
BIBTEX_BIN=bibtex

AUTHORS_HTML=authors/index.html
BIB_HTML=bib/index.html
TODO_HTML=todo/index.html
SUPPORT_HTML=${AUTHORS_HTML} ${BIB_HTML} ${TODO_HTML}

PDF=tex/nwit.pdf

BIB_BIB=./tex/bib.bib
TODO_BIB=./tex/todo.bib
ALL_BIB=${BIB_BIB} ${TODO_BIB}

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
build: ${SUPPORT_HTML} ${PDF}
	${JEKYLL} build

## serve: build site and run server
serve: ${SUPPORT_HTML}
	${JEKYLL} serve

# ---

## authors: cross-reference authors and bibliography entries
authors: ${AUTHORS_HTML} ${AUTHORS_BIN}
	@mkdir -p authors
	@echo "---" > ${AUTHORS_HTML}
	@echo "layout: page" >> ${AUTHORS_HTML}
	@echo "title: Authors" >> ${AUTHORS_HTML}
	@echo "---" >> ${AUTHORS_HTML}
	${AUTHORS_BIN} --input ${BIB_BIB} >> ${AUTHORS_HTML}

## pdf: re-create PDF version of bibliography
pdf: ${PDF}

## bib: re-create HTML bibliography of reviewed articles
bib: ${BIB_HTML}

## todo: re-create HTML bibliography of upcoming articles
todo: ${TODO_HTML}

## ----

## categories: list files by category
categories:
	@bin/categories.py _posts/*/*.html

## check: check integrity of bibliography
check:
	@bin/check.py --inputs ${BIB_BIB} ${TODO_BIB}

## entry: convert single entry (KEY=NameYear) to HTML
entry:
	@cat ${ALL_BIB} | ${BIB2HTML_BIN} --action bib2md --only ${KEY}

## used: check which papers have been used or not
used:
	@bin/used.py --inputs ${BIB_BIB} --pagedir _posts

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

${BIB_HTML}: ${BIB_BIB} ${BIB2HTML_BIN}
	@make TITLE="Bibliography" SLUG=bib bib2html > $@

${TODO_HTML}: ${TODO_BIB} ${BIB2HTML_BIN}
	@make TITLE="To Do" SLUG=todo bib2html > $@

${PDF}: ${BIB_BIB} ${TODO_BIB} tex/nwit.tex tex/abstract.bst
	@cd tex \
	&& rm -f nwit.aux nwit.bbl \
	&& ${LATEX_BIN} nwit \
	&& ${BIBTEX_BIN} nwit \
	&& ${LATEX_BIN} nwit \
	&& ${LATEX_BIN} nwit

bib2html:
	@mkdir -p ${SLUG}
	@echo "---"
	@echo "layout: page"
	@echo "title: ${TITLE}"
	@echo "---"
	@echo '<p><a href="../tex/${SLUG}.bib">BibTeX</a></p>'
	@cat ./tex/${SLUG}.bib | ${BIB2HTML_BIN} --action bib2md
