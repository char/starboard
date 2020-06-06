#!/usr/bin/env sh

if [ ! -z "$STARBOARD_STATIC" ]
then
  python3 -m sipy
  rm -r $STARBOARD_STATIC/*
  cp -r static_out/. $STARBOARD_STATIC
fi
