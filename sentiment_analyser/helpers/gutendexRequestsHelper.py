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


def divide_into_chapters(book_content):
    # Parse the book content using spaCy
    doc = nlp(book_content)

    # Initialize chapter boundaries
    chapter_boundaries = []

    # Iterate over sentences and identify potential chapter boundaries
    for i, sent in enumerate(doc.sents):
        # If the sentence starts with a capitalized word and ends with a period,
        # it might indicate the start of a new chapter
        if sent.text[0].isupper() and sent.text[-1] == '.':
            chapter_boundaries.append(i)

    # Split the book content into chapters based on identified boundaries
    chapters = []
    start = 0
    for boundary in chapter_boundaries:
        chapters.append(book_content[start:boundary].strip())
        start = boundary

    # Append the remaining content as the last chapter
    chapters.append(book_content[start:].strip())

    return chapters
