# OpenRecipeBook

## Building

### Fedora/Silverblue

```
    $ toolbox create --container openrecipebook
    $ toolbox enter --container openrecipebook
    $ sudo dnf --assumeyes install make asciidoctor-pdf
    $ make
    $ exit
    $ xdg-open builds/recipe-book.pdf
```
