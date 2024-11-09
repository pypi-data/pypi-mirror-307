---
parent: Troubleshooting
nav_order: 28
---

# blackboxai not found

In some environments the `blackboxai` command may not be available
on your shell path.
This can occur because of permissions/security settings in your OS,
and often happens to Windows users.

You may see an error message like this:

> blackboxai: The term 'blackboxai' is not recognized as a name of a cmdlet, function, script file, or executable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

Below is the most fail safe way to install and run blackboxai in these situations:

```
python -m pip install -U blackboxai-chat
python -m blackboxai
```


{% include venv-pipx.md %}
