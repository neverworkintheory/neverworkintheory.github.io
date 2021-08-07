JEKYLL=bundle exec jekyll
SITE=./_site

AUTHORS=./bin/authors.py
BIB2HTML=./bin/bib2html.py

CROSSREF_HTML=authors/index.html
REVIEWED_HTML=reviewed/index.html
TODO_HTML=todo/index.html
SUPPORT_HTML=${REVIEWED_HTML} ${TODO_HTML} ${CROSSREF_HTML}

REVIEWED_BIB=bib/reviewed.bib
TODO_BIB=bib/todo.bib

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
build: ${SUPPORT_HTML}
	${JEKYLL} build

## serve: build site and run server
serve: ${SUPPORT_HTML}
	${JEKYLL} serve

# ---

## crossref: cross-reference authors and bibliography entries
crossref:
	@mkdir -p authors
	@echo "---" > ${CROSSREF_HTML}
	@echo "layout: page" >> ${CROSSREF_HTML}
	@echo "title: Authors" >> ${CROSSREF_HTML}
	@echo "---" >> ${CROSSREF_HTML}
	${AUTHORS} --input ${REVIEWED_BIB} >> ${CROSSREF_HTML}

## reviewed: re-create HTML bibliography of reviewed articles
reviewed: ${REVIEWED_HTML}

## todo: re-create HTML bibliography of upcoming articles
todo: ${TODO_HTML}

## ----

## categories: list files by category
categories:
	bin/categories.py _posts/*/*.html

## check: check integrity of bibliography
check:
	bin/check.py --input ${REVIEWED_BIB}

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;

## sterile: clean up and erase generated site
sterile:
	@make clean
	@rm -rf ${SITE}

# --------

${REVIEWED_HTML}: ${REVIEWED_BIB} ${BIB2HTML}
	@make TITLE="Reviewed" SLUG=reviewed bib2html > $@

${TODO_HTML}: ${TODO_BIB} ${BIB2HTML}
	@make TITLE="To Do" SLUG=todo bib2html > $@

bib2html:
	@mkdir -p ${SLUG}
	@echo "---"
	@echo "layout: page"
	@echo "title: ${TITLE}"
	@echo "---"
	@echo '<p><a href="../bib/${SLUG}.bib">BibTeX</a></p>'
	@cat bib/${SLUG}.bib | ${BIB2HTML} bib2md
