#!/usr/bin/env bash
# Convert markdown to pdf

pandoc -s -o DFBA_models_in_SBML.pdf DFBA_models_in_SBML.md --variable urlcolor=cyan
echo "MD --> PDF: DFBA_models_in_SBML.pdf"
