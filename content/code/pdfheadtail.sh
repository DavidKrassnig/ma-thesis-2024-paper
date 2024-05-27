#!/usr/bin/env bash
for FOLDER in */; do 
    for FILE in "$FOLDER"*.pdf; do 
        pdftotext "$FILE" - | echo -e "$FILE\n $(head -n 20) $(tail -n 20)" | less; 
    done
done