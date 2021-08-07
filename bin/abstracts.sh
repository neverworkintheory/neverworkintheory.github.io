#!/usr/bin/env bash

while read doi
do
    echo $doi
    curl -s https://api.semanticscholar.org/v1/paper/${doi} | jq .abstract
    echo ""
done
