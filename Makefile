CONFIG=data/book.yml
DESTINATION=builds
FLAGS=--safe-mode=safe --attribute=allow-uri-read
INPUT=builds/main_book.adoc
OUTPUT=$(DESTINATION)/recipe-book
TEMPERATURE_SYSTEM=imperial
ASCIIDOCTOR := bundle exec asciidoctor
ASCIIDOCTOR-PDF := bundle exec asciidoctor-pdf
export PATH := bin:$(PATH)

.PHONY: all
all: asciidoc docbook html pdf epub

.PHONY: asciidoc
asciidoc:
	generate.py --configfile=$(CONFIG) --temperature=$(TEMPERATURE_SYSTEM) --builddir=$(DESTINATION)

.PHONY: docbook
docbook: asciidoc
	$(ASCIIDOCTOR) --backend=docbook $(FLAGS) $(INPUT) --out-file=$(OUTPUT).xml

.PHONY: pdf
pdf: asciidoc
	$(ASCIIDOCTOR-PDF) ${FLAGS} $(INPUT) --out-file=$(OUTPUT).pdf

.PHONY: html
html:	asciidoc
	$(ASCIIDOCTOR) --backend=html5 $(FLAGS) $(INPUT) --out-file=$(OUTPUT).html

.PHONY: epub
epub:	docbook
	pandoc --from docbook --to epub $(OUTPUT).xml -o $(OUTPUT).epub

.PHONY: clean
clean:
	rm -rf $(DESTINATION)
