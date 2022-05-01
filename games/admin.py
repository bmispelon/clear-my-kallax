from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from games.models import Game
from games.forms import GameAdminForm


class GameResource(resources.ModelResource):
    class Meta:
        model = Game


@admin.register(Game)
class GameAdmin(ImportExportModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}
    form = GameAdminForm
    search_fields = ['title', 'notes']

    resource_class = GameResource

    def view_on_site(self, obj):
        return reverse('games:detail', kwargs={'slug': obj.slug})

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = super().change_view(request, object_id, form_url, extra_context)
        if request.method == 'POST' and request.POST.get('backto'):
            return HttpResponseRedirect(request.POST['backto'])
        return response
