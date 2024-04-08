import urllib.request
import json
import spacy


nlp = spacy.load("en_core_web_sm")

def getRequest(book_id):
    try:
        # Fetch metadata
        metadata_url = f"https://gutendex.com/books/{book_id}.json"
        with urllib.request.urlopen(metadata_url) as metadata_response:
            metadata = json.loads(metadata_response.read())
        
        # Fetch content
        content_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
        with urllib.request.urlopen(content_url) as content_response:
            book_content = content_response.read().decode('utf-8')

        #print(metadata)
        return metadata, book_content
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found)
        raise Exception(f"Failed to retrieve data for book ID {book_id}: {e}")
    except Exception as e:
        # Handle other errors
        raise Exception(f"Failed to retrieve data for book ID {book_id}: {e}")

def get_books(num_books):
    try:
        # Fetch books metadata
        books_url = f"https://gutendex.com/books?limit={num_books}"
        with urllib.request.urlopen(books_url) as books_response:
            books_data = json.loads(books_response.read())
        
        return books_data['results']
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found)
        raise Exception(f"Failed to retrieve books: {e}")
    except Exception as e:
        # Handle other errors
        raise Exception(f"Failed to retrieve books: {e}")
