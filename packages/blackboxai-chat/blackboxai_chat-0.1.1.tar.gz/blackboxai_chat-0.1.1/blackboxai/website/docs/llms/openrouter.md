---
parent: Connecting to LLMs
nav_order: 500
---

# OpenRouter

blackboxai can connect to [models provided by OpenRouter](https://openrouter.ai/models?o=top-weekly):
You'll need an [OpenRouter API key](https://openrouter.ai/keys).

```
python -m pip install -U blackboxai-chat

export OPENROUTER_API_KEY=<key> # Mac/Linux
setx   OPENROUTER_API_KEY <key> # Windows, restart shell after setx

# Or any other open router model
blackboxai --model openrouter/<provider>/<model>

# List models available from OpenRouter
blackboxai --list-models openrouter/
```

In particular, many blackboxai users access Sonnet via OpenRouter:

```
python -m pip install -U blackboxai-chat

export OPENROUTER_API_KEY=<key> # Mac/Linux
setx   OPENROUTER_API_KEY <key> # Windows, restart shell after setx

blackboxai --model openrouter/anthropic/claude-3.5-sonnet
```


{: .tip }
If you get errors, check your
[OpenRouter privacy settings](https://openrouter.ai/settings/privacy).
Be sure to "enable providers that may train on inputs"
to allow use of all models.



