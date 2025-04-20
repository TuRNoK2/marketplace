from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views
from .views import custom_password_change_view

urlpatterns = [
    path('register/',
         views.register_view, name='register'),
    path('login/',
         views.login_view, name='login'),
    path('logout/',
         views.logout_view, name='logout'),

    path('password-change/',
         custom_password_change_view,name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),
]
