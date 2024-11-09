---
parent: Connecting to LLMs
nav_order: 300
---

# Gemini

Google currently offers
[*free* API access to the Gemini 1.5 Pro model](https://ai.google.dev/pricing).
This is the most capable free model to use with blackboxai,
with code editing capability that's comparable to GPT-3.5.
You'll need a [Gemini API key](https://aistudio.google.com/app/u/2/apikey).

```
python -m pip install -U blackboxai-chat

export GEMINI_API_KEY=<key> # Mac/Linux
setx   GEMINI_API_KEY <key> # Windows, restart shell after setx

blackboxai --model gemini/gemini-1.5-pro-latest

# List models available from Gemini
blackboxai --list-models gemini/
```

