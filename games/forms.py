import logging

from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.utils.html import format_html

from games.models import Game


class GameAdminForm(forms.ModelForm):
    rules_lang = forms.MultipleChoiceField(choices=Game.LANG.choices, required=False)
    links = SimpleArrayField(
        forms.URLField(),
        delimiter='\n',
        widget=forms.Textarea,
        required=False,
    )

    class Meta:
        model = Game
        fields = ['title', 'slug', 'visibility', 'notes', 'game_lang', 'rules_lang', 'links']


_LANG_SMALL = {
    Game.LANG.XX: '\N{EMPTY SET}'
}


class LangChoiceCheckboxList(forms.CheckboxSelectMultiple):
    # To make sure the CSS class applies to the wrapper <div> but not the <input>
    option_inherits_attrs = False

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).setdefault('class', '')
        kwargs['attrs']['class'] += ' lang-choice-widget'
        super().__init__(*args, **kwargs)


class LangChoiceField(forms.MultipleChoiceField):
    LANG_CHOICES = [
        (value, format_html('<abbr title="{}">{}</abbr>', label, _LANG_SMALL.get(value, value)))
        for value, label in Game.LANG.choices
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', self.LANG_CHOICES)
        kwargs.setdefault('initial', Game.LANG.values)
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', LangChoiceCheckboxList)
        super().__init__(*args, **kwargs)


class FilterForm(forms.Form):
    keyword = forms.CharField(required=False, help_text="In game's title or description")
    game_lang = LangChoiceField()
    rules_lang = LangChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget.attrs['placeholder'] = self.fields['keyword'].help_text

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
