---
title: blackboxai in your browser
highlight_image: /assets/browser.jpg
parent: Usage
nav_order: 800
description: blackboxai can run in your browser, not just on the command line.
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# blackboxai in your browser

<div class="video-container">
  <video controls loop poster="/assets/browser.jpg">
    <source src="/assets/blackboxai-browser-social.mp4" type="video/mp4">
    <a href="/assets/blackboxai-browser-social.mp4">blackboxai browser UI demo video</a>
  </video>
</div>

<style>
.video-container {
  position: relative;
  padding-bottom: 101.89%; /* 1080 / 1060 = 1.0189 */
  height: 0;
  overflow: hidden;
}

.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>

Use blackboxai's new experimental browser UI to collaborate with LLMs
to edit code in your local git repo.
blackboxai will directly edit the code in your local source files,
and [git commit the changes](https://blackbox.ai/docs/git.html)
with sensible commit messages.
You can start a new project or work with an existing git repo.
blackboxai works well with GPT 3.5, GPT-4, GPT-4 Turbo with Vision,
and Claude 3 Opus.
It also supports [connecting to almost any LLM](https://blackbox.ai/docs/llms.html).

Use the `--browser` switch to launch the browser version of blackboxai:

```
python -m pip install -U blackboxai-chat

export OPENAI_API_KEY=<key> # Mac/Linux
setx   OPENAI_API_KEY <key> # Windows, restart shell after setx

blackboxai --browser
```
