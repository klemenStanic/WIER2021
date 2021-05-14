# Programming assignment 3 - Inverted index and querying

This repository contains the solutions for the third programming assignment of 
the Master's course Web extraction and retrieval at the University of Ljubljana.

## Contents:
- report: `report-indexing.pdf`
- input data: `data/`
- implementation: `implementation-indexing/`
- outputs of both the basic and sqlite searches: `results/`
- inverted index sqlite db: `implementation-indexing/inverted-index.db`

## How to run:
`pip install -r requierements.txt`

`cd implementation-indexing`

`python run-basic-search.py SEARCH_PARAM`

or

`python run-sqlite-search.py SEARCH_PARAM`

If your search query consists of multiple words, use quotations marks around it e.g. `"Sistem SPOT"`.

In order to run the indexing process, uncomment lines 47 and 48 in the file `implemetation-indexing/run-sqlite-search.py`.


