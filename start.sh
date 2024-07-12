#!/bin/bash

# Check if the virtual enviroment exist
if [ -d "env" ]; then
  source env/bin/activate
fi

# Start EXEUbot.py using Python
python3 EXEUbot.py
