from rest_framework.views import APIView
from rest_framework.response import Response

class BookSentimentAnalyserAPIView(APIView):
    def get(self, request):
        # Your logic for analyzing a single book
        return Response({"message": "Analyzing a book"})

class CompareBooksAPIView(APIView):
    def get(self, request):
        # Your logic for comparing multiple books
        return Response({"message": "Comparing books"})
