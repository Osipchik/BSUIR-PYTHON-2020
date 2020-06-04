from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from .. import forms
from ..AccountActivationTokenGenerator import account_activation_token


def signup_view(request):
    form = forms.UserCreateForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', {'form': form})
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            context = {'form': form}
            if User.objects.filter(email=email).exists():
                context["error_mail"] = "Данная почта уже зарегестрирована"
            if len(context) == 1:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()
                use_https = request.is_secure()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта.'
                token = account_activation_token.make_token(user)
                message = render_to_string('emails/verify_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': token,
                    'protocol': 'https' if use_https else 'http',
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'pages/extends/verify_email.html')
            return render(request, 'accounts/signup.html', context)

        context = {'form': form}
        if 'username' in form.errors.as_data():
            context["error_name"] = "Данное имя уже зарегестрировано"
        return render(request, 'accounts/signup.html', context)


def login_view(request):
    form = forms.AuthenticateForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')

    return render(request, 'accounts/login.html', context={'form': form})


@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('home')


def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/login.html')

    return HttpResponse('Activation link is invalid!')
