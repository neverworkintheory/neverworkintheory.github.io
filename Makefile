INSTALL_DIR=$(HOME)/dev.third-bit.com
PAGES=index.html about.html blog.html cv.html
POSTS=$(wildcard _posts/*.html)
LAYOUTS=$(wildcard _layouts/*.html)
INCLUDES=$(wildcard _includes/*.html)

all : commands

## commands   : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## check      : build locally into _site directory for checking
check :
	make OUT=$(PWD)/_site build

## install    : build into installation directory for sharing
install :
	mkdir -p $(INSTALL_DIR)
	make OUT=$(INSTALL_DIR) build

## serve      : serve locally (builds files)
serve :
	jekyll serve

#-------------------------------------------------------------------------------

# build : compile site into $(OUT).
build : $(OUT)/feed.xml

$(OUT)/feed.xml : _config.yml feed.xml $(PAGES) $(LAYOUTS) $(INCLUDES) $(POSTS)
	jekyll build -d $(OUT)

clean :
	rm -rf _site $$(find . -name '*~' -print)
