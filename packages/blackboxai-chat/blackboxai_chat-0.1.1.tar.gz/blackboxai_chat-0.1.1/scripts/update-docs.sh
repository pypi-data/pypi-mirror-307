#!/bin/bash

# exit when any command fails
set -e

if [ -z "$1" ]; then
  ARG=-r
else
  ARG=$1
fi

if [ "$ARG" != "--check" ]; then
  tail -1000 ~/.blackboxai/analytics.jsonl > blackboxai/website/assets/sample-analytics.jsonl
fi

# README.md before index.md, because index.md uses cog to include README.md
cog $ARG \
    README.md \
    blackboxai/website/index.md \
    blackboxai/website/HISTORY.md \
    blackboxai/website/docs/usage/commands.md \
    blackboxai/website/docs/languages.md \
    blackboxai/website/docs/config/dotenv.md \
    blackboxai/website/docs/config/options.md \
    blackboxai/website/docs/config/blackboxai_conf.md \
    blackboxai/website/docs/config/adv-model-settings.md \
    blackboxai/website/docs/leaderboards/index.md \
    blackboxai/website/docs/llms/other.md \
    blackboxai/website/docs/more/infinite-output.md \
    blackboxai/website/docs/legal/privacy.md
