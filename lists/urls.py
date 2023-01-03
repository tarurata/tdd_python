from django.urls import path, re_path, include
from lists import views

urlpatterns = [
    re_path(r'^(\d+)/$', views.view_list, name='view_list'),
    re_path(r'^new$', views.new_list, name='new_list'),
    re_path(r'^users/(.+)/$', views.my_lists, name='my_lists'),
]
