Multilingual Deception Detection of GPT-generated Hotel Reviews
=================================================================================

This repository contains the dataset and code for our NAACL 2025 paper: 
[MAiDE-up: Multilingual Deception Detection of
AI-generated Hotel Reviews](https://aclanthology.org/2025.findings-naacl.88.pdf).

## Data

All data is available at [`all_data`](data/all_data.csv).
Source label **0 represents real hotel reviews** and label **1 represents fake/ LLM-generated hotel reviews**.

## Features

Topic Modeling features can be accessed interactively in [`topic_analysis`](topic_analysis)

## Models

### GPT-4 generation
All generation code is available at [LLM_generation](LLM_generation.py).

### Deception Detection models
XLM-Roberta, Random Forest and Naive Bayes models, together with interpretable features are available at [Deception Detection Models](Deception%20Detection%20Models.ipynb).

## Citation

```bibtex
@inproceedings{ignat-etal-2025-maide,
    title = "{MA}i{DE}-up: Multilingual Deception Detection of {AI}-generated Hotel Reviews",
    author = "Ignat, Oana  and
      Xu, Xiaomeng  and
      Mihalcea, Rada",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Findings of the Association for Computational Linguistics: NAACL 2025",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-naacl.88/",
    pages = "1636--1653",
    ISBN = "979-8-89176-195-7"
}
```
