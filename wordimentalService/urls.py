from django.urls import path
from . import views

urlpatterns = [
    path('sentiment-analyser/analyse-book/', views.BookSentimentAnalyserAPIView.as_view(), name='analyse-book'),
    path('sentiment-analyser/compare-books/', views.CompareBooksAPIView.as_view(), name='compare-books'),    
    path('sentiment-analyser/actor-sentiment-analyser/', views.CharacterSentimentAnalyserAPIView.as_view(), name='analyse-actor'),
    path('sentiment-analyser/list-books/', views.ListBooksAPIView.as_view(), name='list-books'),  
    path('sentiment-analyser/get-book-id/', views.GetBookIDAPIView.as_view(), name='get-book-id'),  

]
