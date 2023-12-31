#! /bin/bash

files="./input/*"
for filepath in $files; do
  echo $filepath
  . make-vp.sh $filepath
done