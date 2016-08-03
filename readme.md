MiSS-Project
===============


## Project Introduction
This project addresses the problem of how to derive identities of persons and social structures from large sets of genealogical data available as text and photographs with incomplete information. In order to do so we want to investigate and deploy a combination of techniques from data mining, machine learning and human computation. The project goals are (a) a semantically enriched and cleaned version of the current database of the BHIC; (b) the development of advanced search tools to support historical research; and (c) providing automatic tools for supporting large scale prosopographical research.

## Contributions
* Using information retrieval framework for identity matching.
* Using the concept of fingerprints for each 
* Easy-to-use Manual Labeling Tool
* Relationship-oriented visualization of family trees

## Packages Required
* Apache Solr™ 5.2.1 
* Django Web Framework
* MySQL
* Twitter Bootsrap
* d3js

## Publications

* B. Ranjbar-Sahraei, J. Efremova, H. Rahmani, T. Calders, K. Tuyls and G. Weiss, "HiDER: Query-Driven Entity Resolution for Historical Data", In Proceedings of the European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases (ECML PKDD 2015), Porto, Portugal, 2015.
* H. Rahmani, B. Ranjbar-Sahraei, G. Weiss and K. Tuyls, "Entity Resolution in Disjoint Graphs: an Application on Genealogical Data", Journal of Intelligent Data Analysis (in press).
* J. Efremova, B. Ranjbar-Sahraei, F. Oliehoek, T. Calders and K. Tuyls, "An Interactive, Web-based Tool for Genealogical Entity Resolution", In Proceedings of the 25th Benelux Conference on Artificial Intelligence (BNAIC), Delft, Netherlands, 2013.



## Details
* the `Modules` folder contains the basic modules needed to run HiDER.
** `basic_modules/basic.py` connects to the MySQL database, runs queries, compares references, wraps data in form of nice format objects and compares vectors.
** `basic_modules/myOrm` is an object-relational mapping to convert MySQL relational data to appropriate objects.
* The `NERD` folder deals with natural language processing. 
* `NERD/dict_based_nerd.py` contains most of the dictionary-based name and relationship extraction files.
