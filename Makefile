DESTINATION=builds
FLAGS=--safe-mode=safe --attribute=allow-uri-read
INPUT=src/index.adoc
OUT=$(DESTINATION)/recipe-book

all: docbook html pdf epub

docbook:
	asciidoctor --backend=docbook $(FLAGS) $(INPUT) --out-file=$(OUT).xml

pdf:
	asciidoctor-pdf ${FLAGS} $(INPUT) --out-file=$(OUT).pdf

html:
	asciidoctor --backend=html5 $(FLAGS) $(INPUT) --out-file=$(OUT).html

epub:	docbook
	pandoc --from docbook --to epub $(OUT).xml -o $(OUT).epub

clean:
	rm -rf $(DESTINATION)
