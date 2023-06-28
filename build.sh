#!/bin/bash
rm -r ./eggs
rm -r ./build
rm -r ./dist
sh ./make_icons.sh
poetry run python setup.py py2app