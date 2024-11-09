---
parent: More info
nav_order: 200
description: blackboxai supports pretty much all popular coding languages.
---
# Supported languages

blackboxai should work well with most popular coding languages.
This is because top LLMs are fluent in most mainstream languages,
and familiar with popular libraries, packages and frameworks.

blackboxai has specific support for linting many languages.
By default, blackboxai runs the built in linter any time a file is edited.
If it finds syntax errors, blackboxai will offer to fix them for you.
This helps catch small code issues and quickly fix them.

blackboxai also does code analysis to help
the LLM navigate larger code bases by producing
a [repository map](https://blackbox.ai/docs/repomap.html).
blackboxai can currently produce repository maps for many popular
mainstream languages, listed below.


## How to add support for another language

blackboxai should work quite well for other languages, even those
without repo map or linter support.
You should really try coding with blackboxai before
assuming it needs better support for your language.

That said, if blackboxai already has support for linting your language,
then it should be possible to add repo map support.
To build a repo map, blackboxai needs the `tags.scm` file
from the given language's tree-sitter grammar.
If you can find and share that file in a 
[GitHub issue](https://github.com/blackboxai-AI/blackboxai/issues),
then it may be possible to add repo map support.

If blackboxai doesn't support linting, it will be complicated to
add linting and repo map support.
That is because blackboxai relies on 
[py-tree-sitter-languages](https://github.com/grantjenks/py-tree-sitter-languages)
to provide pre-packaged versions of tree-sitter
parsers for many languages.

blackboxai needs to be easy for users to install in many environments,
and it is probably too complex to add dependencies on
additional individual tree-sitter parsers.


<!--[[[cog
from blackboxai.repomap import get_supported_languages_md
cog.out(get_supported_languages_md())
]]]-->

| Language | File extension | Repo map | Linter |
|:--------:|:--------------:|:--------:|:------:|
| bash                 | .bash                |          |   ✓    |
| c                    | .c                   |    ✓     |   ✓    |
| c_sharp              | .cs                  |    ✓     |   ✓    |
| commonlisp           | .cl                  |          |   ✓    |
| cpp                  | .cc                  |    ✓     |   ✓    |
| cpp                  | .cpp                 |    ✓     |   ✓    |
| css                  | .css                 |          |   ✓    |
| dockerfile           | .dockerfile          |          |   ✓    |
| dot                  | .dot                 |          |   ✓    |
| elisp                | .el                  |    ✓     |   ✓    |
| elixir               | .ex                  |    ✓     |   ✓    |
| elm                  | .elm                 |    ✓     |   ✓    |
| embedded_template    | .et                  |          |   ✓    |
| erlang               | .erl                 |          |   ✓    |
| go                   | .go                  |    ✓     |   ✓    |
| gomod                | .gomod               |          |   ✓    |
| hack                 | .hack                |          |   ✓    |
| haskell              | .hs                  |          |   ✓    |
| hcl                  | .hcl                 |          |   ✓    |
| html                 | .html                |          |   ✓    |
| java                 | .java                |    ✓     |   ✓    |
| javascript           | .js                  |    ✓     |   ✓    |
| javascript           | .mjs                 |    ✓     |   ✓    |
| jsdoc                | .jsdoc               |          |   ✓    |
| json                 | .json                |          |   ✓    |
| julia                | .jl                  |          |   ✓    |
| kotlin               | .kt                  |          |   ✓    |
| lua                  | .lua                 |          |   ✓    |
| make                 | .mk                  |          |   ✓    |
| objc                 | .m                   |          |   ✓    |
| ocaml                | .ml                  |    ✓     |   ✓    |
| perl                 | .pl                  |          |   ✓    |
| php                  | .php                 |    ✓     |   ✓    |
| python               | .py                  |    ✓     |   ✓    |
| ql                   | .ql                  |    ✓     |   ✓    |
| r                    | .R                   |          |   ✓    |
| r                    | .r                   |          |   ✓    |
| regex                | .regex               |          |   ✓    |
| rst                  | .rst                 |          |   ✓    |
| ruby                 | .rb                  |    ✓     |   ✓    |
| rust                 | .rs                  |    ✓     |   ✓    |
| scala                | .scala               |          |   ✓    |
| sql                  | .sql                 |          |   ✓    |
| sqlite               | .sqlite              |          |   ✓    |
| toml                 | .toml                |          |   ✓    |
| tsq                  | .tsq                 |          |   ✓    |
| typescript           | .ts                  |    ✓     |   ✓    |
| typescript           | .tsx                 |    ✓     |   ✓    |
| yaml                 | .yaml                |          |   ✓    |

<!--[[[end]]]-->


