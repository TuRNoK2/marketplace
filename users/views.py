from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash

from products.models import Product
from .forms import RegisterForm, LoginForm, ProfileEditForm


# регистрация \ логин \ выход
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
# конец




# смена пароля
@login_required
def custom_password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # чтобы не выкинуло из аккаунта
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change.html', {'form': form})

# конец



@login_required
def profile_view(request):
    user = request.user
    products = Product.objects.filter(seller=user)
    return render(request, 'users/profile.html', {'products': products})




@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})
