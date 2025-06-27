#!/bin/bash
cd "$(dirname "$0")"
pip install -r requirements.txt
cd src
python main.py