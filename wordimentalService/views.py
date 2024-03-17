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

        # Check if the id parameter is provided
        if book_id is None:
            return Response({"error": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve book data (metadata and content)
            metadata, book_content = gutendexRequestsHelper.getRequest(book_id)

            # Extract title and authors from metadata
            title = metadata.get('title', 'Unknown')
            authors = ', '.join([author['name'] for author in metadata.get('authors', [])])

            # Return book information and content in the response
            return Response({
                "title": title, 
                "authors": authors, 
                "NLKT_analysis":  nltk_analyser.analyze_sentiment(book_content),
                "TextBlob_analysis": textblob_analyser.analyze_sentiment(book_content),
                "Transformers_analysis": transformers_analyser.analyze_sentiment(book_content),
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
            nltk_analysis1 = nltk_analyser.analyze_sentiment(book1_content)
            textblob_analysis1 = textblob_analyser.analyze_sentiment(book1_content)
            transformers_analysis1 = transformers_analyser.analyze_sentiment(book1_content)

            nltk_analysis2 = nltk_analyser.analyze_sentiment(book2_content)
            textblob_analysis2 = textblob_analyser.analyze_sentiment(book2_content)
            transformers_analysis2 = transformers_analyser.analyze_sentiment(book2_content)

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
