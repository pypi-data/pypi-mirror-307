---
parent: More info
nav_order: 100
description: blackboxai is tightly integrated with git.
---

# Git integration

blackboxai works best with code that is part of a git repo.
blackboxai is tightly integrated with git, which makes it easy to:

  - Use the `/undo` command to instantly undo any AI changes that you don't like.
  - Go back in the git history to review the changes that blackboxai made to your code
  - Manage a series of blackboxai's changes on a git branch

blackboxai uses git in these ways:

- It asks to create a git repo if you launch it in a directory without one.
- Whenever blackboxai edits a file, it commits those changes with a descriptive commit message. This makes it easy to undo or review blackboxai's changes. 
- blackboxai takes special care before editing files that already have uncommitted changes (dirty files). blackboxai will first commit any preexisting changes with a descriptive commit message. 
This keeps your edits separate from blackboxai's edits, and makes sure you never lose your work if blackboxai makes an inappropriate change.

## In-chat commands

blackboxai also allows you to use 
[in-chat commands](/docs/usage/commands.html)
to perform git operations:

- `/diff` will show all the file changes since the last message you sent.
- `/undo` will undo and discard the last change.
- `/commit` to commit all dirty changes with a sensible commit message.
- `/git` will let you run raw git commands to do more complex management of your git history.

You can also manage your git history outside of blackboxai with your preferred git tools.

## Disabling git integration

While it is not recommended, you can disable blackboxai's use of git in a few ways:

  - `--no-auto-commits` will stop blackboxai from git committing each of its changes.
  - `--no-dirty-commits` will stop blackboxai from committing dirty files before applying its edits.
  - `--no-git` will completely stop blackboxai from using git on your files. You should ensure you are keeping sensible backups of the files you are working with.

## Commit messages

blackboxai sends the `--weak-model` a copy of the diffs and the chat history
and asks it to produce a commit message.
By default, blackboxai creates commit messages which follow
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

You can customize the
[commit prompt](https://github.com/blackboxai-AI/blackboxai/blob/main/blackboxai/prompts.py#L5)
with the `--commit-prompt` option.
You can place that on the command line, or 
[configure it via a config file or environment variables](https://blackbox.ai/docs/config.html).


## Commit attribution

blackboxai marks commits that it either authored or committed.

- If blackboxai authored the changes in a commit, they will have "(blackboxai)" appended to the git author and git committer name metadata.
- If blackboxai simply committed changes (found in dirty files), the commit will have "(blackboxai)" appended to the git committer name metadata.

You can use `--no-attribute-author` and `--no-attribute-committer` to disable
modification of the git author and committer name fields.

Additionally, you can use the following options to prefix commit messages:

- `--attribute-commit-message-author`: Prefix commit messages with 'blackboxai: ' if blackboxai authored the changes.
- `--attribute-commit-message-committer`: Prefix all commit messages with 'blackboxai: ', regardless of whether blackboxai authored the changes or not.

Both of these options are disabled by default, but can be useful for easily identifying changes made by blackboxai.
