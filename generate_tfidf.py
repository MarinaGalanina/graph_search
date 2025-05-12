import pandas as pd
import argparse
from ast import literal_eval
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

def load_excel(file_path: str) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.
    """
    return pd.read_excel(file_path)

def build_document_term_map(df: pd.DataFrame) -> dict:
    """
    Build a mapping of document IDs to lists of legal terms.
    """
    doc_terms = defaultdict(list)
    for _, row in df.iterrows():
        term = row['law_term_lemma']
        try:
            nodes = literal_eval(row['related_nodes'])
            for node_id in nodes:
                doc_terms[node_id].append(term)
        except (ValueError, SyntaxError):
            continue
    return doc_terms

def compute_tfidf(documents: list) -> tuple:
    """
    Compute the TF-IDF matrix for a list of documents.
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    return X, vectorizer

def save_to_excel(matrix, doc_ids, feature_names, output_path: str) -> None:
    """
    Save the TF-IDF matrix to an Excel file.
    """
    tfidf_df = pd.DataFrame(matrix.toarray(), index=doc_ids, columns=feature_names)
    tfidf_df.to_excel(output_path, engine='openpyxl')

def main(input_path: str, output_path: str) -> None:
    """
    Load data, compute TF-IDF, and save the result to an Excel file.
    """
    df = load_excel(input_path)
    doc_terms = build_document_term_map(df)
    documents = [' '.join(terms) for terms in doc_terms.values()]
    doc_ids = list(doc_terms.keys())
    matrix, vectorizer = compute_tfidf(documents)
    save_to_excel(matrix, doc_ids, vectorizer.get_feature_names_out(), output_path)
    print(f"TF-IDF matrix saved to '{output_path}'")

if __name__ == "__main__":
    """
    Parse command-line arguments and execute the TF-IDF pipeline.
    """
    parser = argparse.ArgumentParser(description="Generate TF-IDF matrix from legal terms in an Excel file.")
    parser.add_argument("--input", required=True, help="Path to the input Excel file.")
    parser.add_argument("--output", required=True, help="Path to the output Excel file.")

    args = parser.parse_args()
    main(args.input, args.output)
