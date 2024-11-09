---
parent: Troubleshooting
nav_order: 28
---

# Dependency versions

blackboxai expects to be installed via `pip` or `pipx`, which will install
correct versions of all of its required dependencies.

If you've been linked to this doc from a GitHub issue, 
or if blackboxai is reporting `ImportErrors`
it is likely that your
blackboxai install is using incorrect dependencies.

## Install with pipx

If you are having dependency problems you should consider
[installing blackboxai using pipx](/docs/install/pipx.html).
This will ensure that blackboxai is installed in its own python environment,
with the correct set of dependencies.

Try re-installing cleanly:

```
pipx uninstall blackboxai-chat
pipx install blackboxai-chat
```

## Package managers like Homebrew, AUR, ports

Package managers often install blackboxai with the wrong dependencies, leading
to import errors and other problems.

The recommended way to 
install blackboxai is with 
[pip](/docs/install/install.html).
Be sure to use the `--upgrade-strategy only-if-needed` switch so that the correct
versions of dependencies will be installed.

```
python -m pip install -U --upgrade-strategy only-if-needed blackboxai-chat
```

A very safe way is to
[install blackboxai using pipx](/docs/install/pipx.html),
which will ensure it is installed in a stand alone virtual environment.

## Dependency versions matter

blackboxai pins its dependencies and is tested to work with those specific versions.
If you are installing blackboxai with pip (rather than pipx),
you should be careful about upgrading or downgrading the python packages that
blackboxai uses.

In particular, be careful with the packages with pinned versions 
noted at the end of
[blackboxai's requirements.in file](https://github.com/blackboxai-AI/blackboxai/blob/main/requirements/requirements.in).
These versions are pinned because blackboxai is known not to work with the
latest versions of these libraries.

Also be wary of upgrading `litellm`, as it changes versions frequently
and sometimes introduces bugs or backwards incompatible changes.

## Replit

You can `pip install -U blackboxai-chat` on replit.

Or you can install blackboxai with
pipx as follows:

{% include replit-pipx.md %}
