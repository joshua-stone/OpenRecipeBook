DESTINATION=builds
FLAGS=--safe-mode=safe --attribute=allow-uri-read --destination-dir=$(DESTINATION) 
INPUT=src/index.adoc

all: docbook html pdf

docbook:
	mkdir -p $(DESTINATION)
	asciidoctor --backend=docbook $(FLAGS) $(INPUT)

pdf:
	mkdir -p $(DESTINATION)
	asciidoctor-pdf ${FLAGS} $(INPUT)

html:
	mkdir -p $(DESTINATION)
	asciidoctor --backend=html5 $(FLAGS) $(INPUT)

clean:
	rm -rf $(DESTINATION)
