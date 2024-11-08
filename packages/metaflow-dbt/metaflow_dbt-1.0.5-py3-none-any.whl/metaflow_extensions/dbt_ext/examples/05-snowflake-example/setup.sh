#!/bin/bash

if [[ ! -d "./jaffle_shop" ]];then
    git clone https://github.com/dbt-labs/jaffle_shop.git --depth 1
fi

if [[ ! -f "config.py" ]];then
    cp example.config.py config.py
    echo "Created 'config.py'. Remember to edit the placeholder values."
fi