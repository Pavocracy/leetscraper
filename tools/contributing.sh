#!/usr/bin/env bash
# This is a helper script to automate the process of preparing for a pull reuqest
# Each flag will run a specific python module required to conform to coding standards
# Run this script from the root leetscraper directory and pass desired flags

while getopts "iadmp" flag; do
  case "${flag}" in
    i)
        echo "Installing pip requirments"
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt ;;
    a)
        echo "Running autopep8"
        python3 -m autopep8 -i -r src/ ;;
    d)
        echo "Running docformatter"
        python3 -m docformatter -i -r src/ ;;
    m)
        echo "Running mypy"
        python3 -m mypy src/ ;;
    p)
        echo "Running pylint"
        python3 -m pylint src/ ;;
  esac
done
