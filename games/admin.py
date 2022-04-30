from django.contrib import admin

from games.models import Game
from games.forms import GameAdminForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}
    form = GameAdminForm
    search_fields = ['title', 'notes']
