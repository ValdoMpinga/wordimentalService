from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from sentiment_analyser.helpers import gutendexRequestsHelper
from sentiment_analyser.sentiment_analysers.NLTK import nltk_analyser
from sentiment_analyser.sentiment_analysers.TextBlob import textblob_analyser

class ListBooksAPIView(APIView):
    def get(self, request):
        # Define the number of books per request
        num_books_per_request = 25

        try:
            # Fetch the books from Gutendex
            books = gutendexRequestsHelper.get_books(num_books_per_request)

            # Extract relevant information from the books
            books_info = []
            for book in books:
                book_info = {
                    "id": book['id'],
                    "title": book['title'],
                    "authors": ', '.join([author['name'] for author in book['authors']])
                }
                books_info.append(book_info)

            return Response(books_info)
        except Exception as e:
            # Return error response if book retrieval fails
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class GetBookIDAPIView(APIView):
    def post(self, request):
        book_name = request.data.get('name')

        if not book_name:
            return Response({"error": "Parameter 'name' is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            books_data = gutendexRequestsHelper.search_books_by_name(book_name)

            if not books_data:
                raise NotFound(f"No book found with name '{book_name}'")

            book_id = books_data[0]['id']
            return Response({"id": book_id})
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
class BookSentimentAnalyserAPIView(APIView):
    def post(self, request):

        book_id = request.data.get('id')

        print("the book_id parameter" , book_id)
        if book_id is None:
            return Response({"error": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            metadata, book_content = gutendexRequestsHelper.getRequest(book_id)

            title = metadata.get('title', 'Unknown')
            authors = ', '.join([author['name'] for author in metadata.get('authors', [])])
            
            
            print("authors: ", metadata.get('authors'))
            print("title: ", title)
            return Response({
                "title": title, 
                "authors": authors, 
                "NLTK_analysis":  nltk_analyser.nltk_analyze_sentiment(book_content),
                "TextBlob_analysis": textblob_analyser.textblob_analyze_sentiment(book_content),
                })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompareBooksAPIView(APIView):
    def post(self, request):
        book1_id = request.data.get('id1')
        book2_id = request.data.get('id2')

        if book1_id is None or book2_id is None:
            return Response({"error": "Parameters 'id1' and 'id2' are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            metadata1, book1_content = gutendexRequestsHelper.getRequest(book1_id)
            metadata2, book2_content = gutendexRequestsHelper.getRequest(book2_id)

            title1 = metadata1.get('title', 'Unknown')
            authors1 = ', '.join([author['name'] for author in metadata1.get('authors', [])])

            title2 = metadata2.get('title', 'Unknown')
            authors2 = ', '.join([author['name'] for author in metadata2.get('authors', [])])

            nltk_analysis1 = nltk_analyser.nltk_analyze_sentiment(book1_content)
            textblob_analysis1 = textblob_analyser.textblob_analyze_sentiment(book1_content)

            nltk_analysis2 = nltk_analyser.nltk_analyze_sentiment(book2_content)
            textblob_analysis2 = textblob_analyser.textblob_analyze_sentiment(book2_content)

            return Response({
                "book1": {
                    "title": title1,
                    "authors": authors1,
                    "NLTK_analysis": nltk_analysis1,
                    "TextBlob_analysis": textblob_analysis1,
                },
                "book2": {
                    "title": title2,
                    "authors": authors2,
                    "NLTK_analysis": nltk_analysis2,
                    "TextBlob_analysis": textblob_analysis2,
                }
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CharacterSentimentAnalyserAPIView(APIView):
    def post(self, request):
        book_id = request.data.get('id')
        character_name = request.data.get('character')

        if book_id is None or character_name is None:
            return Response({"error": "Parameters 'id' and 'character' are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            metadata, book_content = gutendexRequestsHelper.getRequest(book_id)

            character_sentiment = analyze_character_sentiment(book_content, character_name)

            title = metadata.get('title', 'Unknown')
            authors = ', '.join([author['name'] for author in metadata.get('authors', [])])
            
            return Response({
                "title": title, 
                "authors": authors,
                "character": character_name,
                "sentiment_analysis": character_sentiment
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def analyze_character_sentiment(book_content, character_name):
    
    # NLTK
    nltk_sentiment = nltk_analyser.nltk_analyze_character_sentiment(book_content, character_name)
    print("NLTK Sentiment Analysis ", nltk_sentiment)
    
    # TextBlob
    textblob_sentiment = textblob_analyser.textblob_analyze_character_sentiment(book_content, character_name)
    print("TextBlob Sentiment Analysis ", textblob_sentiment)

    return {
        "NLTK_analysis": nltk_sentiment,
        "TextBlob_analysis": textblob_sentiment,
    }



# {
# 	"id": 23,
# 	"character":"Frederick"
# }
    
# {
# 	"id": 4,
# 	"character":"Lincoln"
# }

# {
# 	"id": 10,
# 	"character":"Jesus"
# }
