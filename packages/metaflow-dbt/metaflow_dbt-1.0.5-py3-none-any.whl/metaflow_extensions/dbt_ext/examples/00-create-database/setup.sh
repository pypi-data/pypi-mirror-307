#!/bin/bash

if [[ ! -f "config.py" ]];then
    cp example.config.py config.py
    echo "Created 'config.py'. Remember to edit the placeholder values."
fi