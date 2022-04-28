from django.contrib.auth.models import User
from django.db import models


class RequestQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(user__isnull=True)

    def approved(self):
        return self.filter(user__isnull=False)


class Request(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comments = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    sent_on = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('auth.User', blank=True, null=True, on_delete=models.CASCADE)

    objects = RequestQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} <{self.email}>'

    @property
    def is_pending(self):
        return self.user_id is None

    @property
    def auto_username(self):
        return self.name.replace(' ', '_').lower()

    def approve(self):
        assert self.user is None
        self.user = User.objects.create(username=self.auto_username, email=self.email)
        self.save(update_fields=['user'])
