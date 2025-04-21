from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from .views import custom_password_change_view, profile_view, edit_profile, register_view, login_view, logout_view

urlpatterns = [
    path('register/',
         register_view, name='register'),
    path('login/',
         login_view, name='login'),
    path('logout/',
         logout_view, name='logout'),

    path('password-change/',
         custom_password_change_view,name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),

    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
