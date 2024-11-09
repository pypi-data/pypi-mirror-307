---
title: blackboxai has written 7% of its own code
excerpt: blackboxai has written 7% of its own code, via 600+ commits that inserted 4.8K and deleted 1.5K lines of code.
highlight_image: /assets/self-assembly.jpg
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# blackboxai has written 7% of its own code

[![self assembly](/assets/self-assembly.jpg)](https://blackbox.ai/assets/self-assembly.jpg)

{: .note }
This article is quite out dated. For current statistics, see
[blackboxai's release history](/HISTORY.html).

The
[blackboxai git repo](https://github.com/blackboxai-AI/blackboxai)
currently contains about 4K commits and 14K lines of code.

blackboxai made 15% of the commits, inserting 4.8K and deleting 1.5K lines of code.

About 7% of the code now in the repo is attributable to an blackboxai commit
using `git blame`.
This number is probably a significant undercount, because periodic reformatting
by `black` is likely obscuring blackboxai's authorship of many lines.

Here's the breakdown of the code blackboxai wrote in the current code base
according to `git blame`.

| File | Lines | Percent |
|---|---:|---:|
|blackboxai/args.py| 6 of 449 | 1.3% |
|blackboxai/coders/base_coder.py| 37 of 1354 | 2.7% |
|blackboxai/coders/editblock_coder.py| 14 of 507 | 2.8% |
|blackboxai/coders/editblock_func_coder.py| 6 of 141 | 4.3% |
|blackboxai/coders/udiff_coder.py| 2 of 421 | 0.5% |
|blackboxai/coders/wholefile_coder.py| 5 of 146 | 3.4% |
|blackboxai/coders/wholefile_func_coder.py| 4 of 134 | 3.0% |
|blackboxai/commands.py| 67 of 703 | 9.5% |
|blackboxai/diffs.py| 15 of 129 | 11.6% |
|blackboxai/gui.py| 2 of 533 | 0.4% |
|blackboxai/history.py| 19 of 124 | 15.3% |
|blackboxai/io.py| 55 of 368 | 14.9% |
|blackboxai/linter.py| 30 of 240 | 12.5% |
|blackboxai/main.py| 30 of 466 | 6.4% |
|blackboxai/mdstream.py| 3 of 122 | 2.5% |
|blackboxai/models.py| 22 of 549 | 4.0% |
|blackboxai/repo.py| 19 of 266 | 7.1% |
|blackboxai/repomap.py| 17 of 518 | 3.3% |
|blackboxai/scrape.py| 12 of 199 | 6.0% |
|blackboxai/versioncheck.py| 10 of 37 | 27.0% |
|blackboxai/voice.py| 9 of 104 | 8.7% |
|benchmark/benchmark.py| 33 of 730 | 4.5% |
|benchmark/over_time.py| 32 of 60 | 53.3% |
|benchmark/swe_bench_lite.py| 40 of 71 | 56.3% |
|scripts/blame.py| 55 of 212 | 25.9% |
|scripts/versionbump.py| 96 of 123 | 78.0% |
|setup.py| 11 of 47 | 23.4% |
|tests/test_coder.py| 48 of 612 | 7.8% |
|tests/test_commands.py| 135 of 588 | 23.0% |
|tests/test_editblock.py| 23 of 403 | 5.7% |
|tests/test_io.py| 30 of 65 | 46.2% |
|tests/test_main.py| 13 of 239 | 5.4% |
|tests/test_models.py| 6 of 28 | 21.4% |
|tests/test_repo.py| 2 of 296 | 0.7% |
|tests/test_repomap.py| 70 of 217 | 32.3% |
|tests/test_udiff.py| 7 of 119 | 5.9% |
|tests/test_wholefile.py| 37 of 321 | 11.5% |
| **Total** | **1022 of 14219** | 7.2% |


