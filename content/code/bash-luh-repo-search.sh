#!/usr/bin/env bash
MAINFOLDERPATH = ./data/
cd $MAINFOLDERPATH
clear && for FOLDER in */; do 
	cd $FOLDER; 
	echo "$FOLDER"
	for FILE in *.pdf; do 
		pdftotext "$FILE" - | grep -iE "github|gitlab|reposi|open source|source code|quellcode|code|data.uni-hannover.de|25835|zenodo|availability"
	done; 
	echo "-----------------------"
	cd ..
done