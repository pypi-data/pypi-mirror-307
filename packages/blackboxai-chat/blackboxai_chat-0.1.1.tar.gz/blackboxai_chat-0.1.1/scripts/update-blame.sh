#!/bin/bash

# exit when any command fails
set -e

./scripts/blame.py v0.1.0 --all --output blackboxai/website/_data/blame.yml
