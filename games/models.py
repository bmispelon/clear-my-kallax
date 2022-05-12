from urllib.parse import urlparse

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _


class LANG(models.TextChoices):
    FR = 'FR', _("French")
    EN = 'EN', _("English")
    HU = 'HU', _("Hungarian")

    XX = 'XX', _("Language independent")


class VISIBILITY(models.IntegerChoices):
    HIDDEN = 0
    VISIBLE = 1


class GameQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(visibility=VISIBILITY.VISIBLE)

    def visible_to(self, user):
        if user.is_staff:
            return self.all()
        else:
            return self.visible()


class Game(models.Model):
    LANG = LANG
    VISIBILITY = VISIBILITY

    slug = models.SlugField()

    visibility = models.PositiveIntegerField(choices=VISIBILITY.choices, default=VISIBILITY.VISIBLE)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    game_lang = models.CharField(max_length=2, choices=LANG.choices, default=LANG.XX)
    rules_lang = ArrayField(models.CharField(max_length=2))
    links = ArrayField(models.URLField(), blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = GameQuerySet.as_manager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def link_tags_list(self):
        if not self.links:
            return ''

        return format_html_join(
            '\n',
            '<li><a href="{}" target="_blank">{}</a></li>',
            ((url, urlparse(url).hostname) for url in self.links)
        )

    @property
    def rules_lang_display(self):
        return [self.LANG(lang).label for lang in self.rules_lang]

    @property
    def is_visible(self):
        return self.visibility == self.VISIBILITY.VISIBLE

    def set_visibility(self, visibility):
        self.visibility = visibility
        self.save(update_fields=['visibility'])
