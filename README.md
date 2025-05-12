# Legal Term Processing Pipeline

This repository contains scripts for:
1. **Lemmatizing legal terms** using Morfeusz2.
2. **Generating a TF-IDF matrix** from legal terms mapped to document IDs.
3. **Searching the TF-IDF matrix** (via `tfidf_search').

## Table of Contents

1. [Project Structure](#project-structure)
2. [Workflow Overview](#workflow-overview)
2. [Pipeline Diagram](#pipeline-diagram)
4. [Installation](#installation)
5. [License](#license)


## Project Structure

```text
├── lemmatize_law_terms.py                # Lemmatization script
├── generate_tfidf.py                     # TF-IDF matrix generator
├── requirements.txt                      # Project dependencies
└── README.md      
```

## Workflow Overview

1. **Lemmatization**
   - **Input:** original Excel file with legal terms in the law_term column and linked document IDs in the related_nodes column
   - **Output:** new Excel file with an added law_term_lemma column next to law_term
   - **Run:**
     ```bash
     python lemmatize_law_terms.py --input input_file.xlsx --output output_file.xlsx
     ```

2. **TF-IDF Matrix Generation**
   - **Input:** produced in the previous step (or without previous step)
   - **Output:** Excel file containing the TF-IDF matrix
   - Run:
     ```bash
     python generate_tfidf.py --input input_file.xlsx --output output_file.xlsx
     ```

3. **TF-IDF Search**
   - Load **tfidf_matrix_lemma.xlsx**(Excel file containing the TF-IDF matrix), receive a user query, and return the most relevant document IDs based on TF-IDF ranking


---

## Pipeline Diagram

```plaintext
+---------------------+
| counts_df.xlsx      |
| (law terms + links) |
+---------+-----------+
          |
          v
+-------------------------------+
| lemmatize_law_terms.py         |
| Output: counts_df_lemmatized.xlsx |
+-------------------------------+
          |
          v
+-------------------------------+
| generate_tfidf.py              |
| Output: tfidf_matrix_lemma.xlsx|
+-------------------------------+
          |
          v
+-------------------------------+
| tfidf_search.py (external)     |
| Input: tfidf_matrix_lemma.xlsx |
| Search functionality          |
+-------------------------------+

## Installation

1. Clone the repository:

```bash
https://github.com/MarinaGalanina/graph_search.git
cd graph_search
```
2. (Recommended) Create a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## License

This project is under the MIT License