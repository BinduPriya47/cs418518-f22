from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from webapp.views import ChangePasswordView



urlpatterns = [
    path('', views.home, name='home'),
    path('signup_page', views.signup_page, name='signup_page'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('confirm_code/<str:id>/', views.confirm_code, name='confirm_code'),
    path('signout/<str:id>/', views.signout, name='signout'),
    path('base/<str:id>/', views.base, name='base'),
    path('signout_user', views.signout_user, name='signout_user'),
    path('signin', views.signin, name='signin'),
    path('forget_password', views.send_email_to_reset_pw, name='send_email_to_reset_pw'),
    path('send_mail_forget_pw/<str:uname>/', views.send_mail_forget_pw, name='send_mail_forget_pw'),
     path('ChangePasswordView/<str:id>/', views.ChangePasswordView, name='ChangePasswordView'),
    # path('ChangePasswordView', ChangePasswordView.as_view(), name='ChangePasswordView'),
    path('updateinfo/<str:id>/', views.updateinfo, name='updateinfo'),
    path('updateuserinfo/<str:id>/', views.updateuserinfo, name='updateuserinfo'),

    path('reset_password/<str:uname>/', views.reset_password, name='reset_password'),
    path('view_profile/<str:id>/', views.view_profile, name='view_profile'),


    # path('reset_password/',
    #  auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
    #  name="reset_password"),

    # path('reset_password_sent/', 
    #     auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
    #     name="password_reset_done"),

    # path('reset/<uidb64>/<token>/',
    #  auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
    #  name="password_reset_confirm"),

    # path('reset_password_complete/', 
    #     auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
    #     name="password_reset_complete"),

    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
    #     name='password_change_done'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='`password_change.html'), 
    #     name='password_change'),
]
