from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sentiment_analyser.helpers import gutendexRequestsHelper
from sentiment_analyser.sentiment_analysers.NLTK import nltk_analyser
from sentiment_analyser.sentiment_analysers.TextBlob import textblob_analyser
from sentiment_analyser.sentiment_analysers.Transformers import transformers_analyser

class BookSentimentAnalyserAPIView(APIView):
    def post(self, request):
        # Get the id parameter from the request data

        book_id = request.data.get('id')

        print("the book_id parameter" , book_id)
        # Check if the id parameter is provided
        if book_id is None:
            return Response({"error": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve book data (metadata and content)
            metadata, book_content = gutendexRequestsHelper.getRequest(book_id)

            # Extract title and authors from metadata
            title = metadata.get('title', 'Unknown')
            authors = ', '.join([author['name'] for author in metadata.get('authors', [])])
            
            
            print("authors: ", metadata.get('authors'))
            print("title: ", title)
            # print(book_content)
            # Return book information and content in the response
            return Response({
                "title": title, 
                "authors": authors, 
                "NLKT_analysis":  nltk_analyser.nltk_analyze_sentiment(book_content),
                "TextBlob_analysis": textblob_analyser.textblob_analyze_sentiment(book_content),
                })
        except Exception as e:
            # Return error response if book data retrieval fails
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompareBooksAPIView(APIView):
    def post(self, request):
        # Get the id parameters from the request data
        book1_id = request.data.get('id1')
        book2_id = request.data.get('id2')

        # Check if both id parameters are provided
        if book1_id is None or book2_id is None:
            return Response({"error": "Parameters 'id1' and 'id2' are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve book data for both books (metadata and content)
            metadata1, book1_content = gutendexRequestsHelper.getRequest(book1_id)
            metadata2, book2_content = gutendexRequestsHelper.getRequest(book2_id)

            # Extract title and authors from metadata
            title1 = metadata1.get('title', 'Unknown')
            authors1 = ', '.join([author['name'] for author in metadata1.get('authors', [])])

            title2 = metadata2.get('title', 'Unknown')
            authors2 = ', '.join([author['name'] for author in metadata2.get('authors', [])])

            # Perform sentiment analysis for both books
            nltk_analysis1 = nltk_analyser.nltk_analyze_sentiment(book1_content)
            textblob_analysis1 = textblob_analyser.textblob_analyze_sentiment(book1_content)
            transformers_analysis1 = transformers_analyser.transformers_analyze_sentiment(book1_content)

            nltk_analysis2 = nltk_analyser.nltk_analyze_sentiment(book2_content)
            textblob_analysis2 = textblob_analyser.textblob_analyze_sentiment(book2_content)
            transformers_analysis2 = transformers_analyser.transformers_analyze_sentiment(book2_content)

            # Return the sentiment analysis results for both books in the response
            return Response({
                "book1": {
                    "title": title1,
                    "authors": authors1,
                    "NLKT_analysis": nltk_analysis1,
                    "TextBlob_analysis": textblob_analysis1,
                    "Transformers_analysis": transformers_analysis1
                },
                "book2": {
                    "title": title2,
                    "authors": authors2,
                    "NLKT_analysis": nltk_analysis2,
                    "TextBlob_analysis": textblob_analysis2,
                    "Transformers_analysis": transformers_analysis2
                }
            })
        except Exception as e:
            # Return error response if book data retrieval fails
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# {
# 	"id": 23,
# 	"character":"Frederick"
# }
    
# {
# 	"id": 4,
# 	"character":"Lincoln"
# }
# 

# {
# 	"id": 10,
# 	"character":"Jesus"
# }
class CharacterSentimentAnalyserAPIView(APIView):
    def post(self, request):
        # Get the id parameter and character name from the request data
        book_id = request.data.get('id')
        character_name = request.data.get('character')

        # Check if both parameters are provided
        if book_id is None or character_name is None:
            return Response({"error": "Parameters 'id' and 'character' are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve book data (metadata and content)
            metadata, book_content = gutendexRequestsHelper.getRequest(book_id)

            # Analyze sentiment about the character in the book content
            character_sentiment = analyze_character_sentiment(book_content, character_name)

            # Extract title and authors from metadata
            title = metadata.get('title', 'Unknown')
            authors = ', '.join([author['name'] for author in metadata.get('authors', [])])
            
            # Return book information and character sentiment analysis in the response
            return Response({
                "title": title, 
                "authors": authors,
                "character": character_name,
                "sentiment_analysis": character_sentiment
            })
        except Exception as e:
            # Return error response if book data retrieval fails
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def analyze_character_sentiment(book_content, character_name):
    # Perform sentiment analysis focusing on the character in the book content
    # using NLTK, TextBlob, and Transformers libraries
    
    # NLTK
    nltk_sentiment = nltk_analyser.nltk_analyze_character_sentiment(book_content, character_name)
    print("NLTK Sentiment Analysis ", nltk_sentiment)
    
    # TextBlob
    textblob_sentiment = textblob_analyser.textblob_analyze_character_sentiment(book_content, character_name)
    print("TextBlob Sentiment Analysis ", textblob_sentiment)

    # Transformers
    transformers_sentiment = transformers_analyser.transformers_analyze_character_sentiment(book_content, character_name)
    print("Transformers Sentiment Analysis ", transformers_sentiment)


    return {
        "NLTK_analysis": nltk_sentiment,
        "TextBlob_analysis": textblob_sentiment,
        "Transformers_analysis": transformers_sentiment
    }
