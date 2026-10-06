#!/bin/sh
# Build the shareable zip from exactly what is committed: dist/hermes-jev-skills-<version>.zip
set -eu
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests
python3 scripts/check_release.py
version=$(python3 -c "import re;print(re.search(r'\"(.+?)\"', open('jevkit/__init__.py').read().split('__version__')[1]).group(1))")
mkdir -p dist
out="dist/hermes-jev-skills-$version.zip"
rm -f "$out"
git archive --format=zip --prefix="hermes-jev-skills/" -o "$out" HEAD
echo "$out"
