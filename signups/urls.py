from django.urls import path

from signups.views import (
    SignupView,
    SendMagicLinkView,
    signup_ok,
    signup_email_already_exists,
    send_magic_link_ok,
)

app_name = 'signups'
urlpatterns = [
    path('', SignupView.as_view(), name='signup'),
    path('send-magic-link/', SendMagicLinkView.as_view(), name='send-magic-link'),
    path('signup-ok/', signup_ok, name='signup-ok'),
    path('signup-email-exists/', signup_email_already_exists, name='signup-email-already-exists'),
    path('send-magic-link/ok/', send_magic_link_ok, name='send-magic-link-ok'),
]
