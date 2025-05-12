import pandas as pd
import argparse
from morfeusz2 import Morfeusz

def load_excel(file_path: str) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.
    """
    return pd.read_excel(file_path)

def save_to_excel(df: pd.DataFrame, output_path: str) -> None:
    """
    Save the DataFrame to an Excel file without the index.
    """
    df.to_excel(output_path, index=False)

def initialize_morfeusz() -> Morfeusz:
    """
    Initialize and return the Morfeusz2 lemmatizer instance.
    """
    return Morfeusz()

def lemmatize_text(text: str, morfeusz: Morfeusz) -> str:
    """
    Lemmatize the provided text using Morfeusz2, preferring nouns if available.
    """
    words = str(text).split()
    lemmas = []
    for word in words:
        analyses = morfeusz.analyse(word)
        lemma = None
        for token in analyses:
            tag = token[2][2]
            base = token[2][1].split(":")[0]
            if "subst" in tag:
                lemma = base
                break
        if not lemma and analyses:
            lemma = analyses[0][2][1].split(":")[0]
        lemmas.append(lemma if lemma else word)
    return " ".join(lemmas)

def process_dataframe(input_path: str, output_path: str) -> None:
    """
    Load the input DataFrame, lemmatize the 'law_term' column,
    reorder columns, and save the result to the output file.
    """
    df = load_excel(input_path)
    morfeusz = initialize_morfeusz()
    df["law_term_lemma"] = df["law_term"].astype(str).apply(lambda text: lemmatize_text(text, morfeusz))

    """
    Reorder columns to place 'law_term_lemma' directly after 'law_term'.
    """
    cols = df.columns.tolist()
    cols.insert(cols.index("law_term") + 1, cols.pop(cols.index("law_term_lemma")))
    df = df[cols]

    save_to_excel(df, output_path)

if __name__ == "__main__":
    """
    Parse command-line arguments and execute the processing pipeline.
    """
    parser = argparse.ArgumentParser(description="Lemmatize law terms in an Excel file.")
    parser.add_argument("--input", required=True, help="Path to the input Excel file.")
    parser.add_argument("--output", required=True, help="Path to the output Excel file.")

    args = parser.parse_args()
    process_dataframe(args.input, args.output)
