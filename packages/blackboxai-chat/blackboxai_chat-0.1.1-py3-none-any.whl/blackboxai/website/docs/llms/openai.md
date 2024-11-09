---
parent: Connecting to LLMs
nav_order: 100
---

# OpenAI

To work with OpenAI's models, you need to provide your
[OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
either in the `OPENAI_API_KEY` environment variable or
via the `--openai-api-key` command line switch.

blackboxai has some built in shortcuts for the most popular OpenAI models and
has been tested and benchmarked to work well with them:

```
python -m pip install -U blackboxai-chat

export OPENAI_API_KEY=<key> # Mac/Linux
setx   OPENAI_API_KEY <key> # Windows, restart shell after setx

# blackboxai uses gpt-4o by default (or use --4o)
blackboxai

# GPT-4o
blackboxai --4o

# GPT-3.5 Turbo
blackboxai --35-turbo

# o1-mini
blackboxai --model o1-mini

# o1-preview
blackboxai --model o1-preview

# List models available from OpenAI
blackboxai --list-models openai/
```

You can use `blackboxai --model <model-name>` to use any other OpenAI model.
For example, if you want to use a specific version of GPT-4 Turbo
you could do `blackboxai --model gpt-4-0125-preview`.
