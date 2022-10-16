#!/bin/sh

cd $1

for i in *.m4a;
do name=`echo "$i" | cut -d'.' -f1`
  echo "$name"
  ffmpeg -i "$i" "${name}.wav"
done
