from urllib.parse import urlencode

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from signups.emails import send_magic_link_email
from signups.forms import SendLinkForm, SignupForm


class SignupView(generic.CreateView):
    template_name = 'signups/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('signups:signup-ok')

    def get_initial(self):
        initial = super().get_initial()
        if 'email' in self.request.GET:
            initial.update(email=self.request.GET['email'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.find_matching_user()
        if user is not None:
            # Send matching link instead of signing up
            return self.send_magic_link_instead(user)
        return super().form_valid(form)

    def send_magic_link_instead(self, user):
        send_magic_link_email(self.request, user)
        return redirect('signups:signup-email-already-exists')


class SendMagicLinkView(SuccessMessageMixin, generic.FormView):
    template_name = 'signups/send_login_link.html'
    form_class = SendLinkForm
    success_message = 'A login link was sent to %(email)s'
    success_url = reverse_lazy('signups:send-magic-link-ok')

    def form_valid(self, form):
        user = form.find_matching_user()
        if user is None:
            # TODO: look for matching signup request
            return self.redirect_to_signup(form.cleaned_data['email'])
        send_magic_link_email(self.request, user)
        return super().form_valid(form)

    def redirect_to_signup(self, email):
        return redirect(reverse('signups:signup') + '?' + urlencode({'email': email}))


signup_ok = generic.TemplateView.as_view(template_name='signups/signup_ok.html')
signup_email_already_exists = generic.TemplateView.as_view(
    template_name='signups/email_already_exists.html'
)
send_magic_link_ok = generic.TemplateView.as_view(template_name='signups/send_magic_link_ok.html')
