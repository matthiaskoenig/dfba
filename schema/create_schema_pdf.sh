#!/usr/bin/env bash
################################################
# Convert markdown to pdf using pandoc
################################################
# requirements:
#  sudo apt-get install pandoc
#
# usage:
#  ./create_schema_pdf.sh
################################################

echo "create pdf from markdown"
pandoc -s -o DFBA_models_in_SBML.pdf DFBA_models_in_SBML.md --variable urlcolor=cyan
echo "MD --> PDF: DFBA_models_in_SBML.pdf"

echo "copy to supplement"
cp DFBA_models_in_SBML.pdf ../docs/manuscript/supplement/S1_DFBA_models_in_SBML.pdf
