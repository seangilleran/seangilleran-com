#!/bin/bash

rm content/.html/*

for filename in content/*.md; do
    pandoc -o /tmp/content.html "$filename" --ascii &&
    tidy -config tidy.conf /tmp/content.html > content/.html/$(basename "${filename%.*}").html
    sed '/\.\.\./q' "$filename" > content/.html/$(basename "${filename%.*}").yaml &&
    rm /tmp/content.html
done
