import pandas as pd
import argparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import morfeusz2


def load_tfidf_matrix(filepath: str) -> pd.DataFrame:
    """
    Load TF-IDF matrix from an Excel file.
    The first column should contain document IDs, and the first row should contain terms.
    """
    try:
        df = pd.read_excel(filepath, index_col=0)
        print(f"Pomyślnie wczytano macierz TF-IDF o wymiarach {df.shape}.")
        return df
    except Exception as e:
        raise FileNotFoundError(f"Nie udało się wczytać macierzy TF-IDF: {e}")


def lemmatize_polish(text: str) -> list:
    """
    Lemmatize the given Polish text using Morfeusz2.
    """
    morfeusz = morfeusz2.Morfeusz()
    analysis = morfeusz.analyse(text)
    lemmas = [interpretation[2][1] for interpretation in analysis]
    return lemmas


def extract_terms_from_prompt(prompt: str, available_terms: list) -> list:
    """
    Extract valid TF-IDF terms from a natural language prompt after lemmatization.
    """
    lemmatized_words = lemmatize_polish(prompt.lower())
    valid_terms = [lemma for lemma in lemmatized_words if lemma in available_terms]

    if not valid_terms:
        print("Żadne słowo z podanego zapytania nie znajduje się w macierzy.")
    else:
        print(f"Zidentyfikowane słowa kluczowe: {valid_terms}")

    return valid_terms


def compute_similarity(df: pd.DataFrame, query_terms: list) -> pd.Series:
    """
    Compute cosine similarity between the user query and all documents in the TF-IDF matrix.
    """
    query_vector = np.zeros((1, df.shape[1]))
    for term in query_terms:
        if term in df.columns:
            query_vector[0, df.columns.get_loc(term)] = 1.0

    doc_vectors = df.values
    similarity_scores = cosine_similarity(query_vector, doc_vectors).flatten()
    return pd.Series(similarity_scores, index=df.index).sort_values(ascending=False)


def save_results(results: pd.Series, output_path: str) -> None:
    """
    Save the similarity results to an Excel file.
    """
    results.to_excel(output_path)
    print(f"Wyniki zapisano do pliku '{output_path}'.")


def parse_arguments():
    """
    Parse command-line arguments for the TF-IDF query tool.
    """
    parser = argparse.ArgumentParser(description="Przeszukaj graf TF-IDF na podstawie pytania.")
    parser.add_argument("prompt", type=str, help="Naturalne pytanie użytkownika, np. 'Jakie leki wymagają rejestracji?'")
    return parser.parse_args()


def main():
    """
    Main execution function for running the TF-IDF graph search tool with natural language query support.
    """
    args = parse_arguments()
    input_filepath = "tfidf_matrix_lemma.xlsx"
    output_filepath = "wyniki_zapytania.xlsx"

    df = load_tfidf_matrix(input_filepath)
    query_terms = extract_terms_from_prompt(args.prompt, df.columns.tolist())
    if not query_terms:
        return

    results = compute_similarity(df, query_terms)
    print("\nNajlepiej pasujące dokumenty:\n")
    print(results.head(10))

    save_results(results, output_filepath)


if __name__ == "__main__":
    main()
