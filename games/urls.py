from django.urls import path

from games.views import detail, games_list, hide_game, show_game

app_name = 'games'
urlpatterns = [
    path('', games_list, name='list'),
    path('<slug:slug>/', detail, name='detail'),
    path('<slug:slug>/show/', show_game, name='show'),
    path('<slug:slug>/hide/', hide_game, name='hide'),
]
