# `concatsources`: Concatenate JavaScript or CSS files

A minimalistic Python script (with no dependencies) to concatenate `.js` or
`.css` files, and include the source map.

## Usage

To concatenate multiple `.js` files into one file:

    concatsources.py --output=out.js in1.js in2.js in3.js:

To also include the full source of the `.js` files in `out.js`:

    concatsources.py --source-map-include-sources --output=out.js in1.js in2.js in3.js
