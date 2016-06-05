all : commands

## commands   : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## categories : show known categories
categories :
	@python bin/categories.py $(POSTS)

## check      : build locally into _site directory for checking
check :
	make OUT=$(PWD)/_site build

## serve      : serve locally (builds files)
serve :
	jekyll serve --config _config.yml,_config_dev.yml

## clean      : clean up
clean :
	rm -rf _site $$(find . -name '*~' -print)
