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
    def get(self, request):
        # Your logic for comparing multiple books
        return Response({"message": "Comparing books"})
