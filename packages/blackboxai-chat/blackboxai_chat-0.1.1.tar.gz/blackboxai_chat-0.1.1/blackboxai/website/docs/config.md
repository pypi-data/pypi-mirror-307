---
nav_order: 55
has_children: true
description: Information on all of blackboxai's settings and how to use them.
---

# Configuration

blackboxai has many options which can be set with
command line switches.
Most options can also be set in an `.blackboxai.conf.yml` file
which can be placed in your home directory or at the root of
your git repo. 
Or by setting environment variables like `blackboxai_xxx`
either in your shell or a `.env` file.

Here are 4 equivalent ways of setting an option. 

With a command line switch:

```
$ blackboxai --dark-mode
```

Using a `.blackboxai.conf.yml` file:

```yaml
dark-mode: true
```

By setting an environment variable:

```
export blackboxai_DARK_MODE=true
```

Using an `.env` file:

```
blackboxai_DARK_MODE=true
```

{% include env-keys-tip.md %}

