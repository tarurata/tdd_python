from django.shortcuts import render, redirect
import uuid
import sys
from django.contrib.auth import authenticate
# from accounts.authentication import PasswordlessAuthenticationBackend
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render
from django.core.mail import send_mail

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for superlists',
        f'Use this link to log in:\n\n{url}',
        'saycheese5963@gmail.com',
        [email],
    )
    return render(request, 'login_email_sent.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    print(f'uid: {uid}')
    # 本来ここがデフォルトのauthenticateの次に、カスタムのauthenticateが使われるはず
    user = authenticate(request, uid=uid)
    print(f'user: {user}')
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
