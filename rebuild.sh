#!/usr/bin/env sh

python3 -m sipy
rm -rf $STARBOARD_STATIC > /dev/null || true
cp -r static_out $STARBOARD_STATIC
