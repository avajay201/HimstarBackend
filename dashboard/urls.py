# urls.py
from django.urls import path
from .views import CompetitionsByCategoryView, MyCompetitions, TournamentsByCategoryView, CategoryListView,CategoryDetailView, RoundListCreateView, RoundDetailView, EliminateParticipantsView, StartNextRoundView, LeaderBoard

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('competitions/', CompetitionsByCategoryView.as_view(), name='competitions_by_category'),
    path('tournaments/', TournamentsByCategoryView.as_view(), name='tournaments_by_category'),
    path('rounds/', RoundListCreateView.as_view(), name='round-list-create'),
    path('rounds/<int:pk>/', RoundDetailView.as_view(), name='round-detail'),
    path('my-competitions/', MyCompetitions.as_view(), name='my-competitions'),
    path('leaderboard/', LeaderBoard.as_view(), name='leaderboard'),
]