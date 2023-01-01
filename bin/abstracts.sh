#!/usr/bin/env bash

curl -s https://api.semanticscholar.org/v1/paper/${1} | jq .abstract
