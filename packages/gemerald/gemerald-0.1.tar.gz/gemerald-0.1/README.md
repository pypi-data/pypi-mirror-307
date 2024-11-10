# Gemerald #

A markdown-based static site generator for HTTP and Gemini. Inspired by Hugo. Written in Python.

### Try it out ###

This repository provides an example project for you to play around.
You can try to build it with just a few commands

```bash
pip install gemerald
gemerald example
ls -la example-build
```
## Gemerald markdown ##

We use specific subset of markdown with some extensions. Here is features currently supported:

### Markdown features currently working ###

 - [X] Normal text
 - [X] Headings `#` - `######`
 - [X] Ordered lists
 - [X] Unordered lists
 - [X] Bold
 - [X] Italics
 - [X] Quotes
 - [ ] Nested lists
 - [X] Code snippets
 - [ ] Tables
 - [X] Inline code snippets
 - [X] Links
 - [ ] Images

### Markdown features that wont be supported ###

 - Inline links - All links must be placed on separate lines

### Extra markdown features ###

 - [X] Authors for quotes
 - [ ] Raw `.html` snippets
 - [ ] Raw `.gmi` snippets
 - [X] Metadata headers

### SSG features ###

 - [X] Templating
 - [X] Blog templating (one template for multiple files)
 - [X] Listings
 - [X] Auto copyright date
 - [ ] Images rescaling in build time
 - [ ] Image cache
 - [ ] Git integration for edit log

### Output formats ###

 - [X] Plaintext
 - [X] HTML
 - [X] Gemini markup
 - [ ] Markdown (Yes! Markdown from Markdown)
 - [ ] RSS feed
 - [ ] Atom feed

## Project Guide ##

### Compatibility ###

 - Python 3.12

### Basic directory structure ###

To start building your site you will need 3 directories:
 - templates
 - static
 - content

`static` directory will hold all your assets for the website.
This catalog will be copied to every output format under the path `/static`.
Please put your images there.

`content` directory contains all your markdown files.
These will be translated into output formats.
It can contain subfolders.
Subfolders will apear in output ass well.

`templates` is a directory that contains only other subdirectories.
All subdirectories must be named just like needed output formats.
As an example, if you need to produce HTML output, all your HTML templates will be placed under
`templates/html`.

### Config files ###

Each format's template directory must contain additional file named `config.yaml`.
This file contains all configuration for given format.
This is a list of mandatory keys that need to be present:

 - `enabled` (boolean) - Prevent output for given format by setting this to false.

### Templating ###

### Blog entires ###

## Who uses it? ##

 - [ ] wilmhit.pw (not yet)
 - [ ] hspoz.pl (If they will be willing to)
 - [ ] Your website
