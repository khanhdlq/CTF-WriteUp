#!/bin/sh

socat tcp-listen:9991,fork,reuseaddr exec:./chall 2>/dev/null