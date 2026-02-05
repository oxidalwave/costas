#!/usr/bin/bash
if [[ "$1" == "-i" ]]; then
    shift
    .venv/bin/pip install .
fi

.venv/bin/python main.py
