#!/bin/bash
chal="${CHAL:-ehc-pwn-earn-much-money}"
docker rm -f "$chal"
docker build --tag="$chal" .
docker run -p 1337:1337 --rm --name="${chal}" "${chal}"