from django.urls import path

from games.views import detail, games_list

app_name = 'games'
urlpatterns = [
    path('', games_list, name='list'),
    path('<slug:slug>/', detail, name='detail')
]
