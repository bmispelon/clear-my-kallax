from django.urls import path

from games.views import (
    games_list,
    detail,
)

app_name = 'games'
urlpatterns = [
    path('', games_list, name='list'),
    path('<slug:slug>/', detail, name='detail')
]
