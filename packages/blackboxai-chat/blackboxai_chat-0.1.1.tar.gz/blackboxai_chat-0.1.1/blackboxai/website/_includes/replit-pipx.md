To use blackboxai with pipx on replit, you can run these commands in the replit shell:

```
pip install pipx
pipx run blackboxai-chat ...normal blackboxai args...
```

If you install blackboxai with pipx on replit and try and run it as just `blackboxai` it will crash with a missing `libstdc++.so.6` library.

