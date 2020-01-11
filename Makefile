DESTINATION=builds
FLAGS=--safe-mode=safe --attribute=allow-uri-read
INPUT=builds/book/index.adoc
OUTPUT=$(DESTINATION)/recipe-book
export PATH := src/bin:$(PATH)

all: asciidoc docbook html pdf epub

asciidoc:
	build.py src $(DESTINATION)
docbook: asciidoc
	asciidoctor --backend=docbook $(FLAGS) $(INPUT) --out-file=$(OUTPUT).xml

pdf:	asciidoc
	asciidoctor-pdf ${FLAGS} $(INPUT) --out-file=$(OUTPUT).pdf

html:	asciidoc
	asciidoctor --backend=html5 $(FLAGS) $(INPUT) --out-file=$(OUTPUT).html

epub:	docbook
	pandoc --from docbook --to epub $(OUTPUT).xml -o $(OUTPUT).epub

clean:
	rm -rf $(DESTINATION)
