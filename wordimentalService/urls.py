from django.urls import path
from . import views

urlpatterns = [
    path('sentiment-analyser/book/', views.BookSentimentAnalyserAPIView.as_view(), name='analyse-book'),
    path('sentiment-analyser/compare-books/', views.CompareBooksAPIView.as_view(), name='analyse-compare-books'),
]
