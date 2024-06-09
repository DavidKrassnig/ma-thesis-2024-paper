#!/usr/bin/env bash
for FOLDER in * /; do 
  for FILE in "$FOLDER" *.pdf; do
    echo "$FILE";
    pdftotext "$FILE" - | grep -iE -C 5 --color=auto "forschungsdat|primärdat|sekundärdat|FDM|research data|praxis";
    echo "-----------------";
  done
done