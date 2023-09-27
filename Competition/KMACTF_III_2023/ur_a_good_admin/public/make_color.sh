#!/bin/bash

set -eux

mv /flag.txt /flag_`head -c 300 /dev/urandom | tr -dc 'a-zA-Z0-9'`.txt

sed -i 's/SUPER_SECRET_KEY/'`head -c 300 /dev/urandom | tr -dc 'a-zA-Z0-9'`'/g' /app/config.py