from django.urls import path, re_path, include
from accounts import views
from accounts.views import send_login_email

urlpatterns = [
    re_path(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    re_path(r'^login$', views.login, name='login'),
    # re_path(r'^logout$', views.logout, name='logout'),
]