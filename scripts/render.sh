#!/bin/bash

rm content/.html/*.html
rm content/.html/*.yaml
for filename in content/*.md; do
    pandoc -o "/tmp/~render.html" "$filename" -f markdown+autolink_bare_uris --ascii &&
    tidy -config scripts/tidy.conf "/tmp/~render.html" > content/.html/$(basename "${filename%.*}").html &&
    rm "/tmp/~render.html" &&
    sed '/\.\.\./q' "$filename" > content/.html/$(basename "${filename%.*}").yaml
done

rm wwwroot/files/cv.docx
pandoc -o wwwroot/files/cv.docx content/_cv.md
