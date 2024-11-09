---
parent: More info
nav_order: 400
description: You can script blackboxai via the command line or python.
---

# Scripting blackboxai

You can script blackboxai via the command line or python.

## Command line

blackboxai takes a `--message` argument, where you can give it a natural language instruction.
It will do that one thing, apply the edits to the files and then exit.
So you could do:

```bash
blackboxai --message "make a script that prints hello" hello.js
```

Or you can write simple shell scripts to apply the same instruction to many files:

```bash
for FILE in *.py ; do
    blackboxai --message "add descriptive docstrings to all the functions" $FILE
done
```

Use `blackboxai --help` to see all the 
[command line options](/docs/config/options.html),
but these are useful for scripting:

```
--stream, --no-stream
                      Enable/disable streaming responses (default: True) [env var:
                      blackboxai_STREAM]
--message COMMAND, --msg COMMAND, -m COMMAND
                      Specify a single message to send GPT, process reply then exit
                      (disables chat mode) [env var: blackboxai_MESSAGE]
--message-file MESSAGE_FILE, -f MESSAGE_FILE
                      Specify a file containing the message to send GPT, process reply,
                      then exit (disables chat mode) [env var: blackboxai_MESSAGE_FILE]
--yes                 Always say yes to every confirmation [env var: blackboxai_YES]
--auto-commits, --no-auto-commits
                      Enable/disable auto commit of GPT changes (default: True) [env var:
                      blackboxai_AUTO_COMMITS]
--dirty-commits, --no-dirty-commits
                      Enable/disable commits when repo is found dirty (default: True) [env
                      var: blackboxai_DIRTY_COMMITS]
--dry-run, --no-dry-run
                      Perform a dry run without modifying files (default: False) [env var:
                      blackboxai_DRY_RUN]
--commit              Commit all pending changes with a suitable commit message, then exit
                      [env var: blackboxai_COMMIT]
```


## Python

You can also script blackboxai from python:

```python
from blackboxai.coders import Coder
from blackboxai.models import Model

# This is a list of files to add to the chat
fnames = ["greeting.py"]

model = Model("gpt-4-turbo")

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames)

# This will execute one instruction on those files and then return
coder.run("make a script that prints hello world")

# Send another instruction
coder.run("make it say goodbye")

# You can run in-chat "/" commands too
coder.run("/tokens")

```

See the
[Coder.create() and Coder.__init__() methods](https://github.com/blackboxai-AI/blackboxai/blob/main/blackboxai/coders/base_coder.py)
for all the supported arguments.

It can also be helpful to set the equivalent of `--yes` by doing this:

```
from blackboxai.io import InputOutput
io = InputOutput(yes=True)
# ...
coder = Coder.create(model=model, fnames=fnames, io=io)
```

