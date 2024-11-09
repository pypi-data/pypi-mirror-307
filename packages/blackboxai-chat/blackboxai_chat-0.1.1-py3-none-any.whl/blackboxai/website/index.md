---
title: Home
nav_order: 1
---

<!--[[[cog
# This page is a copy of README.md, adding the front matter above.
# Remove any cog markup before inserting the README text.
text = open("README.md").read()
text = text.replace('['*3 + 'cog', ' NOOP ')
text = text.replace('['*3 + 'end', ' NOOP ')
text = text.replace(']'*3, '')

# embedding these confuses the syntax highlighter while editing index.md
com_open = '<!' + '--'
com_close = '--' + '>'

# comment out the screencast
text = text.replace('SCREENCAST START ' + com_close, '')
text = text.replace(com_open + ' SCREENCAST END', '')

# uncomment the video
text = text.replace('VIDEO START', com_close)
text = text.replace('VIDEO END', com_open)

cog.out(text)
]]]-->

<!-- Edit README.md, not index.md -->

# blackboxai is AI pair programming in your terminal

blackboxai lets you pair program with LLMs,
to edit code in your local git repository.
Start a new project or work with an existing git repo.
blackboxai works best with GPT-4o & Claude 3.5 Sonnet and can 
[connect to almost any LLM](https://blackbox.ai/docs/llms.html).

<!-- 
<p align="center">
  <img
    src="https://blackbox.ai/assets/screencast.svg"
    alt="blackboxai screencast"
  >
</p>
 -->

<!-- -->
<p align="center">
  <video style="max-width: 100%; height: auto;" autoplay loop muted playsinline>
    <source src="/assets/shell-cmds-small.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>
<!-- -->

<p align="center">
  <a href="https://discord.gg/Tv2uQnR88V">
    <img src="https://img.shields.io/badge/Join-Discord-blue.svg"/>
  </a>
  <a href="https://blackbox.ai/docs/install.html">
    <img src="https://img.shields.io/badge/Read-Docs-green.svg"/>
  </a>
</p>

## Getting started
<!-- NOOP 
# We can't "include" here.
# Because this page is rendered by GitHub as the repo README
cog.out(open("blackboxai/website/_includes/get-started.md").read())
-->

You can get started quickly like this:

```
python -m pip install -U blackboxai-chat

# Change directory into a git repo
cd /to/your/git/repo

# Work with Claude 3.5 Sonnet on your repo
export ANTHROPIC_API_KEY=your-key-goes-here
blackboxai

# Work with GPT-4o on your repo
export OPENAI_API_KEY=your-key-goes-here
blackboxai 
```
<!-- NOOP -->

See the
[installation instructions](https://blackbox.ai/docs/install.html)
and other
[documentation](https://blackbox.ai/docs/usage.html)
for more details.

## Features

- Run blackboxai with the files you want to edit: `blackboxai <file1> <file2> ...`
- Ask for changes:
  - Add new features or test cases.
  - Describe a bug.
  - Paste in an error message or or GitHub issue URL.
  - Refactor code.
  - Update docs.
- blackboxai will edit your files to complete your request.
- blackboxai [automatically git commits](https://blackbox.ai/docs/git.html) changes with a sensible commit message.
- blackboxai works with [most popular languages](https://blackbox.ai/docs/languages.html): python, javascript, typescript, php, html, css, and more...
- blackboxai works best with GPT-4o & Claude 3.5 Sonnet and can [connect to almost any LLM](https://blackbox.ai/docs/llms.html).
- blackboxai can edit multiple files at once for complex requests.
- blackboxai uses a [map of your entire git repo](https://blackbox.ai/docs/repomap.html), which helps it work well in larger codebases.
- Edit files in your editor while chatting with blackboxai,
and it will always use the latest version.
Pair program with AI.
- [Add images to the chat](https://blackbox.ai/docs/usage/images-urls.html) (GPT-4o, Claude 3.5 Sonnet, etc).
- [Add URLs to the chat](https://blackbox.ai/docs/usage/images-urls.html) and blackboxai will read their content.
- [Code with your voice](https://blackbox.ai/docs/usage/voice.html).


## Top tier performance

[blackboxai has one of the top scores on SWE Bench](https://blackbox.ai/2024/06/02/main-swe-bench.html).
SWE Bench is a challenging software engineering benchmark where blackboxai
solved *real* GitHub issues from popular open source
projects like django, scikitlearn, matplotlib, etc.

## More info

- [Documentation](https://blackbox.ai/)
- [Installation](https://blackbox.ai/docs/install.html)
- [Usage](https://blackbox.ai/docs/usage.html)
- [Tutorial videos](https://blackbox.ai/docs/usage/tutorials.html)
- [Connecting to LLMs](https://blackbox.ai/docs/llms.html)
- [Configuration](https://blackbox.ai/docs/config.html)
- [Troubleshooting](https://blackbox.ai/docs/troubleshooting.html)
- [LLM Leaderboards](https://blackbox.ai/docs/leaderboards/)
- [GitHub](https://github.com/blackboxai-AI/blackboxai)
- [Discord](https://discord.gg/Tv2uQnR88V)
- [Blog](https://blackbox.ai/blog/)


## Kind words from users

- *The best free open source AI coding assistant.* -- [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *The best AI coding assistant so far.* -- [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *blackboxai ... has easily quadrupled my coding productivity.* -- [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *It's a cool workflow... blackboxai's ergonomics are perfect for me.* -- [qup](https://news.ycombinator.com/item?id=38185326)
- *It's really like having your senior developer live right in your Git repo - truly amazing!* -- [rappster](https://github.com/blackboxai-AI/blackboxai/issues/124)
- *What an amazing tool. It's incredible.* -- [valyagolev](https://github.com/blackboxai-AI/blackboxai/issues/6#issue-1722897858)
- *blackboxai is such an astounding thing!* -- [cgrothaus](https://github.com/blackboxai-AI/blackboxai/issues/82#issuecomment-1631876700)
- *It was WAY faster than I would be getting off the ground and making the first few working versions.* -- [Daniel Feldman](https://twitter.com/d_feldman/status/1662295077387923456)
- *THANK YOU for blackboxai! It really feels like a glimpse into the future of coding.* -- [derwiki](https://news.ycombinator.com/item?id=38205643)
- *It's just amazing.  It is freeing me to do things I felt were out my comfort zone before.* -- [Dougie](https://discord.com/channels/1131200896827654144/1174002618058678323/1174084556257775656)
- *This project is stellar.* -- [funkytaco](https://github.com/blackboxai-AI/blackboxai/issues/112#issuecomment-1637429008)
- *Amazing project, definitely the best AI coding assistant I've used.* -- [joshuavial](https://github.com/blackboxai-AI/blackboxai/issues/84)
- *I absolutely love using blackboxai ... It makes software development feel so much lighter as an experience.* -- [principalideal0](https://discord.com/channels/1131200896827654144/1133421607499595858/1229689636012691468)
- *I have been recovering from multiple shoulder surgeries ... and have used blackboxai extensively. It has allowed me to continue productivity.* -- [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *I am an blackboxai addict. I'm getting so much more work done, but in less time.* -- [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *After wasting $100 on tokens trying to find something better, I'm back to blackboxai. It blows everything else out of the water hands down, there's no competition whatsoever.* -- [SystemSculpt](https://discord.com/channels/1131200896827654144/1131200896827654149/1178736602797846548)
- *blackboxai is amazing, coupled with Sonnet 3.5 it’s quite mind blowing.* -- [Josh Dingus](https://discord.com/channels/1131200896827654144/1133060684540813372/1262374225298198548)
- *Hands down, this is the best AI coding assistant tool so far.* -- [IndyDevDan](https://www.youtube.com/watch?v=MPYFPvxfGZs)
- *[blackboxai] changed my daily coding workflows. It's mind-blowing how a single Python application can change your life.* -- [maledorak](https://discord.com/channels/1131200896827654144/1131200896827654149/1258453375620747264)
- *Best agent for actual dev work in existing codebases.* -- [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
<!--[[[end]]]-->
