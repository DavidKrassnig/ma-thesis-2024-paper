#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

lualatex --shell-escape "$SCRIPT_DIR/main.tex"
biber "$SCRIPT_DIR/main"
lualatex --shell-escape "$SCRIPT_DIR/main.tex"
