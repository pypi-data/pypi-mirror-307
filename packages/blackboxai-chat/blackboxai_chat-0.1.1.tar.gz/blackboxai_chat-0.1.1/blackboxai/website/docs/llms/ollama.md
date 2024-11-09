---
parent: Connecting to LLMs
nav_order: 500
---

# Ollama

blackboxai can connect to local Ollama models.

```
# Pull the model
ollama pull <model>

# Start your ollama server
ollama serve

# In another terminal window...
python -m pip install -U blackboxai-chat

export OLLAMA_API_BASE=http://127.0.0.1:11434 # Mac/Linux
setx   OLLAMA_API_BASE http://127.0.0.1:11434 # Windows, restart shell after setx

blackboxai --model ollama/<model>
```

In particular, `llama3:70b` works well with blackboxai:


```
ollama pull llama3:70b
ollama serve

# In another terminal window...
export OLLAMA_API_BASE=http://127.0.0.1:11434 # Mac/Linux
setx   OLLAMA_API_BASE http://127.0.0.1:11434 # Windows, restart shell after setx

blackboxai --model ollama/llama3:70b 
```

See the [model warnings](warnings.html)
section for information on warnings which will occur
when working with models that blackboxai is not familiar with.

