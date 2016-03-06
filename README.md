# elm-static-site

Proof of concept static site generator from Elm files.

setup

```
npm install
elm-package install
```

To see an example, run

```bash
node convert.js
```

This will take the Elm files from `examples`, and convert them to static views in the `output` folder.

## How it works

Goes through folder, find elm files. If you want that file to be turned into a compiled output, then you need to have `view =` defining the output that you want it to have.

Either way, right now, if you're using the example folder, you need a `view : Html`. This is your entry point. This `Html` will be rendered as actual html into a file with the same name, but lowercase. E.g `Index.elm -> index.html`, `Blog.Index.elm` -> `blog/index.html`.
