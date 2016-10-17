#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$DIR:$PYTHONPATH"
cd $DIR
python image_annotator/app.py
