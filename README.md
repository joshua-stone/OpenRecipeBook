# OpenRecipeBook

## Building

### Fedora/Silverblue

```
    $ toolbox create --container openrecipebook
    $ toolbox enter --container openrecipebook
    $ sudo dnf --assumeyes install asciidoctor-pdf make pandoc
    $ make
    $ exit
    $ xdg-open builds/recipe-book.pdf
```

## Contributing a recipe

Anyone is welcome to contribute a recipe that they've perfected over time and have wanted to share with others! Please note that some guidelines should be followed for a consistent reading experience:

- Additions should be derived from src/templates. Recipes follow a specific structure that're seen in traditional recipe books, and should be written as if they're going to be printed onto paper.
- Equipment should be explicitely listed, and any equipment should link to the equipment section in src/sections/equipment. This lets aspiring home chefs quickly understand what they'd need to get started
- New equipment should be anything contributors have personally used and would recommend and/or are well-reviewed by reputable sources
- Measurements should use mass whenever possible. Due to differences and inconsistencies in measuring systems, measuring by volume can lead to an otherwise good recipe having poor results.
- Measurements using whole units, e.g., "1 tomato", are acceptable as they're often intuitive to read. Listing mass alongside for accuracy is recommended as well
- Mentioning brands is helpful since there tends to be deviation in taste, texture, etc.
