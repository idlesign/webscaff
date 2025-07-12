#!/usr/bin/env bash

# install makeapp from sources for local development
cd ../
# venv will be in current directory and in ~/.local/share/uv/tools/webscaff/
uv tool install --force -e .
uv sync
