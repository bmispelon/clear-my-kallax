from django import forms
from django.contrib.auth.models import User

from ipware import get_client_ip

from signups.models import Request


class FindmatchingUserMixin:
    def find_matching_user(self):
        try:
            return User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return None


class SignupForm(FindmatchingUserMixin, forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name', 'email', 'comments']

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        if request is not None:
            self.instance.ip_address, _ = get_client_ip(request)

    def clean_email(self):
        email = self.cleaned_data['email']
        if Request.objects.pending().filter(email=email).exists():
            raise forms.ValidationError("This email address has already signed up")
        return email



class SendLinkForm(FindmatchingUserMixin, forms.Form):
    email = forms.EmailField()
