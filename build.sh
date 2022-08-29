#!/bin/bash

pyinstaller -F awesomepywp.py
cp ./dist/awesomepywp ~/.local/bin
