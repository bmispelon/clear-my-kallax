import logging

from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from games.models import Game


class GameAdminForm(forms.ModelForm):
    rules_lang = forms.MultipleChoiceField(choices=Game.LANG.choices, required=False)
    links = SimpleArrayField(forms.URLField(), delimiter='\n', widget=forms.Textarea, required=False)

    class Meta:
        model = Game
        fields = ['title', 'slug', 'notes', 'game_lang', 'rules_lang', 'links']


class FilterForm(forms.Form):
    keyword = forms.CharField(required=False)
    game_lang = forms.MultipleChoiceField(choices=Game.LANG.choices, required=False)
    rules_lang = forms.MultipleChoiceField(choices=Game.LANG.choices, required=False)

    @classmethod
    def from_request(cls, request):
        if any(f in request.GET for f in cls.base_fields):
            return cls(request.GET)
        else:
            return cls()

    def apply_to_queryset(self, queryset):
        if not self.is_valid():
            logging.debug("Invalid filter form")
            return queryset

        if self.cleaned_data['keyword']:
            queryset = queryset.filter(title__icontains=self.cleaned_data['keyword'])

        if self.cleaned_data['game_lang']:
            queryset = queryset.filter(game_lang__in=self.cleaned_data['game_lang'])

        if self.cleaned_data['rules_lang']:
            queryset = queryset.filter(rules_lang__overlap=self.cleaned_data['rules_lang'])

        return queryset
