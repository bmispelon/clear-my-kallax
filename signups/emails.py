from urllib.parse import urlunsplit

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from sesame.utils import get_query_string


def _get_magic_link(request, user):
    return urlunsplit((
        'https' if request.is_secure() else 'http',
        request.get_host(),
        reverse('games:list'),
        get_query_string(user)[1:],  # remove the leading `?`
        '',  # empty fragment
    ))


def _get_email_body(request, user):
    return f"""
Hi,

Here is your personal magic link for you to log in to my board game giveaway website:

{_get_magic_link(request, user)}

If it wasn't you who requested this link, or if you have any questions please contact me
by replying to this email.

Have a nice day,
Baptiste
"""


def send_magic_link_email(request, user):
    return send_mail(
        subject='Your personal login link',
        message=_get_email_body(request, user),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
