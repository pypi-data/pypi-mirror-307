---
parent: Connecting to LLMs
nav_order: 200
---

# Anthropic

To work with Anthropic's models, you need to provide your
[Anthropic API key](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
either in the `ANTHROPIC_API_KEY` environment variable or
via the `--anthropic-api-key` command line switch.

blackboxai has some built in shortcuts for the most popular Anthropic models and
has been tested and benchmarked to work well with them:

```
python -m pip install -U blackboxai-chat

export ANTHROPIC_API_KEY=<key> # Mac/Linux
setx   ANTHROPIC_API_KEY <key> # Windows, restart shell after setx

# blackboxai uses Claude 3.5 Sonnet by default (or use --sonnet)
blackboxai

# Claude 3 Opus
blackboxai --opus

# List models available from Anthropic
blackboxai --list-models anthropic/
```

{: .tip }
Anthropic has very low rate limits. 
You can access all the Anthropic models via
[OpenRouter](openrouter.md)
or [Google Vertex AI](vertex.md)
with more generous rate limits.

You can use `blackboxai --model <model-name>` to use any other Anthropic model.
For example, if you want to use a specific version of Opus
you could do `blackboxai --model claude-3-opus-20240229`.
