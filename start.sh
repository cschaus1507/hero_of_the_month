#!/bin/bash
if [ ! -f votes.json ]; then echo "[]" > votes.json; fi
python app.py
