#!/bin/bash
set -e

echo "== AI-FG public build start =="

python3 scripts/validate-content.py
python3 scripts/build-index.py
python3 scripts/build-pages.py
python3 scripts/build-llms.py
python3 scripts/build-sitemap.py
python3 scripts/build-readme.py

echo "== AI-FG public build done =="
