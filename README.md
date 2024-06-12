Multilingual Deception Detection of GPT-generated Hotel Reviews
=================================================================================

This repository contains the dataset and code for our paper.

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
