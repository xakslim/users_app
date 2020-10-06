# -*- coding: utf-8 -*-
from django.conf.urls import url, re_path
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = (
    re_path(r'^user/$', views.UserListView.as_view(), name='user_list'),
    re_path(r'^user/new/$', views.UserCreationView.as_view(), name='create_user'),
    re_path(r'^user/edit/(?P<pk>[-\w]{1,150})/$', views.user_edit, name='user_edit'),
    re_path(r'^login/$', views.UserLogin.as_view(), name='login'),
    re_path(r'^logout/$', views.UserLogout.as_view(), name='logout'),
    re_path(r'^reset_password/$', views.UserPasswordResetView.as_view(), name='reset_password'),
    re_path(r'^password-reset/done/$', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(
        r'^reset/(?P<uidb64>[-\w]{1,150})/(?P<token>[-\w]{1,255})/$',
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'
    ),
    re_path(r'^reset/done/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
)
