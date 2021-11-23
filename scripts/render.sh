#!/bin/bash

rm content/.html/*

for filename in content/*.md; do
    pandoc -o /tmp/content.html "$filename" -f markdown+autolink_bare_uris --ascii &&
    tidy -config scripts/tidy.conf /tmp/content.html > content/.html/$(basename "${filename%.*}").html &&
    sed '/\.\.\./q' "$filename" > content/.html/$(basename "${filename%.*}").yaml &&
    rm /tmp/content.html
done

rm wwwroot/files/cv.docx
pandoc -o wwwroot/files/cv.docx content/_cv.md
