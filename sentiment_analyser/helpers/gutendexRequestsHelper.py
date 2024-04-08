import urllib.request
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def getRequest(book_id):
    try:
        metadata_url = f"https://gutendex.com/books/{book_id}.json"
        with urllib.request.urlopen(metadata_url) as metadata_response:
            metadata = json.loads(metadata_response.read())
        
        content_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
        with urllib.request.urlopen(content_url) as content_response:
            book_content = content_response.read().decode('utf-8')

        return metadata, book_content
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to retrieve data for book ID {book_id}: {e}")
    except Exception as e:
        raise Exception(f"Failed to retrieve data for book ID {book_id}: {e}")

def get_books(num_books):
    try:
        books_url = f"https://gutendex.com/books?limit={num_books}"
        with urllib.request.urlopen(books_url) as books_response:
            books_data = json.loads(books_response.read())
        
        return books_data['results']
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to retrieve books: {e}")
    except Exception as e:
        raise Exception(f"Failed to retrieve books: {e}")


def search_books_by_name(book_name):
    try:
        search_url = f"https://gutendex.com/books/?search={urllib.parse.quote(book_name)}"
        with urllib.request.urlopen(search_url) as search_response:
            search_results = json.loads(search_response.read())

        return search_results['results']
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to search for books: {e}")
    except Exception as e:
        raise Exception(f"Failed to search for books: {e}")
