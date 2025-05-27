import sys
import requests
from bs4 import BeautifulSoup


def fetch_page(word):
    """
    Fetch the HTML content of the synonym page for the given word.

    Parameters:
        word (str): The word to look up.

    Returns:
        str: HTML content of the page.

    Raises:
        requests.HTTPError: If the HTTP request fails.
    """
    url = f"https://synonim.net/synonim/{word}"
    response = requests.get(url, timeout=10)

    # Raise an exception for HTTP errors (e.g., 404, 500)
    response.raise_for_status()
    return response.text


def extract_synonyms(html):
    """
    Parse the HTML content and extract a list of synonyms.

    Parameters:
        html (str): Raw HTML of the synonym page.

    Returns:
        list[str]: A list of extracted synonyms.
    """
    soup = BeautifulSoup(html, "html.parser")
    synonym_elements = soup.select("div#main ul li a")

    # Extract and return the text content of each <a> element
    return [el.get_text(strip=True) for el in synonym_elements]


def get_synonyms(word):
    """
    Get synonyms for a given word by fetching and parsing the page.

    Parameters:
        word (str): The word to look up.

    Returns:
        list[str]: List of synonyms, or an empty list if none found.
    """
    try:
        html = fetch_page(word)
        synonyms = extract_synonyms(html)
        return synonyms
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching synonyms: {http_err}")
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    return []


def main():
    """
    Main function to parse CLI arguments and print synonyms.
    """
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <word>")
        sys.exit(1)

    word = sys.argv[1]
    synonyms = get_synonyms(word)

    if synonyms:
        print(f"Synonyms for '{word}':")
        print(", ".join(synonyms))
    else:
        print(f"No synonyms found for '{word}' or an error occurred.")


if __name__ == "__main__":
    main()
