JEKYLL=bundle exec jekyll
SITE=./_site

ABSTRACT_BIN=./bin/abstracts.sh
AUTHORS_BIN=./bin/authors.py
BIB2YAML_BIN=./bin/bib2yaml.py
YAML2HTML_BIN=./bin/yaml2html.py
BIBTEX_BIN=bibtex
LATEX_BIN=pdflatex

NWIT_BIB=./tex/nwit.bib
TODO_BIB=./tex/todo.bib
ALL_BIB=${NWIT_BIB} ${TODO_BIB}

AUTHORS_HTML=authors/index.html
BIB_HTML=bib/index.html
TODO_HTML=todo/index.html
SUPPORT_HTML=${AUTHORS_HTML} ${BIB_HTML} ${TODO_HTML}

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
build: ${SUPPORT_HTML} ${PDF}
	${JEKYLL} build

## serve: build site and run server
serve: ${SUPPORT_HTML}
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

## ----

## abstract: get abstract from DOI (DOI=value)
abstract:
	@${ABSTRACT_BIN} ${DOI}

## entry: convert single entry (KEY=NameYear) to HTML
entry:
	@cat ${ALL_BIB} | ${BIB2YAML_BIN} --only ${KEY} | ${YAML2HTML_BIN}

## pick: select a random entry from the to-do list (YEAR=yyyy optional)
pick:
	@cat ${TODO_BIB} | bin/pick.py ${YEAR}

## show: show all entries from the to-do list (YEAR=yyyy optional)
show:
	@cat ${TODO_BIB} | bin/show.py ${YEAR}

## ----

## categories: list files by category
categories:
	@bin/categories.py _posts/*/*.html

## check: run all checks
check:
	@make check-bib
	@make check-used

## check-bib: check integrity of bibliography
check-bib:
	@bin/check-bib.py --inputs ${NWIT_BIB} ${TODO_BIB}

## check-used: check which papers have been used or not
check-used:
	@bin/check-used.py --pagedir _posts --used ${NWIT_BIB} --todo ${TODO_BIB}

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
	${AUTHORS_BIN} --input ${NWIT_BIB} >> ${AUTHORS_HTML}

${BIB_HTML}: ${NWIT_BIB} ${BIB2YAML_BIN} ${YAML2HTML_BIN}
	make TITLE="Bibliography" SLUG=nwit bib2yaml > $@

${TODO_HTML}: ${TODO_BIB} ${BIB2YAML_BIN}
	make TITLE="To Do" SLUG=todo bib2yaml > $@

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
	@echo '<p><a href="../tex/${SLUG}.bib">BibTeX</a></p>'
	@cat ./tex/${SLUG}.bib | ${BIB2YAML_BIN} | ${YAML2HTML_BIN}
