DESTINATION=builds
FLAGS=--safe-mode=safe --attribute=allow-uri-read
INPUT=builds/book/index.adoc
OUTPUT=$(DESTINATION)/recipe-book
TEMPERATURE_SYSTEM=imperial
# Some distros like OpenSUSE add gem executables to PATH differently so resolve gem executables through rubygems instead
ASCIIDOCTOR := $(shell ruby -r 'rubygems' -e 'puts Gem.bin_path("asciidoctor", "asciidoctor")')
ASCIIDOCTOR-PDF := $(shell ruby -r 'rubygems' -e 'puts Gem.bin_path("asciidoctor-pdf", "asciidoctor-pdf")')
export PATH := src/bin:$(PATH)

all: asciidoc docbook html pdf epub

asciidoc:
	build.py --temperature=$(TEMPERATURE_SYSTEM) src $(DESTINATION)

docbook: asciidoc
	$(ASCIIDOCTOR) --backend=docbook $(FLAGS) $(INPUT) --out-file=$(OUTPUT).xml

pdf:	asciidoc
	$(ASCIIDOCTOR-PDF) ${FLAGS} $(INPUT) --out-file=$(OUTPUT).pdf

html:	asciidoc
	$(ASCIIDOCTOR) --backend=html5 $(FLAGS) $(INPUT) --out-file=$(OUTPUT).html

epub:	docbook
	pandoc --from docbook --to epub $(OUTPUT).xml -o $(OUTPUT).epub

clean:
	rm -rf $(DESTINATION)
