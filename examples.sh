#!/usr/bin/env bash

for f in examples/*; do
  for f1 in $f/before_file_hash/*; do
    BEFORE_FILE=$f1
  done
  for f1 in $f/after_file_hash/*; do
    AFTER_FILE=$f1
  done
  for f1 in $f/target_file_hash/*; do
    if [[ $f1 != *.patched.c ]]; then
      TARGET_FILE=$f1
    fi
  done

#  python -m backporter $BEFORE_FILE $AFTER_FILE $TARGET_FILE > $TARGET_FILE.patched.c
#  diff $TARGET_FILE $TARGET_FILE.patched
  python3 -m backporter $BEFORE_FILE $AFTER_FILE $TARGET_FILE > $TARGET_FILE.patched.c 2>>examples.log
done
