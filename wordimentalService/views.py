from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sentiment_analyser.helpers import gutendexRequestsHelper

class BookSentimentAnalyserAPIView(APIView):
    def post(self, request):
        # Get the id parameter from the request data
        id = request.data.get('id')

        # Check if the id parameter is provided
        if id is None:
            return Response({"error": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve book data from Gutendex API
        gutendex_url = f"https://gutendex.com/books/{id}.json"
        
        try:
            # Make the request using the helper function
            book_data = gutendexRequestsHelper.getRequest(gutendex_url)
            
            # Example: Extract relevant book information (e.g., title, author)
            title = book_data.get('title', 'Unknown')
            authors = book_data.get('authors', 'Unknown')
            # Return book information in the response
            return Response({"title": title, "authors": authors})
        except Exception as e:
            # Return error response if book data retrieval fails
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class CompareBooksAPIView(APIView):
    def get(self, request):
        # Your logic for comparing multiple books
        return Response({"message": "Comparing books"})
