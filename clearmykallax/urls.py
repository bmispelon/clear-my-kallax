from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from .views import favicon, robots_txt, landing, login


def trigger_error(request):
    raise Exception("oh no")


urlpatterns = [
    path('', landing, name='landing'),
    path('games/', include('games.urls', namespace='games')),
    path('signups/', include('signups.urls', namespace='signups')),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('favicon.ico', favicon),
    path('robots.txt', robots_txt),

    path('adm/', admin.site.urls),
    path('_error/', trigger_error),
]
