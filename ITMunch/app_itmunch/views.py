from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['goal', 'gender', 'birthday', 'height', 'current_weight', 'goal_weight', 'activity']

def index(request):
    if not request.user.is_authenticated:
        return redirect('app_itmunch:login')
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'app_itmunch/index.html', {'profile': profile})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('app_itmunch:index')
    else:
        form = AuthenticationForm()
    return render(request, 'app_itmunch/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('app_itmunch:questions')
    else:
        form = UserCreationForm()
    return render(request, 'app_itmunch/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('app_itmunch:login')

def questions_view(request):
    if not request.user.is_authenticated:
        return redirect('app_itmunch:login')
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('app_itmunch:index')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'app_itmunch/questions.html', {'form': form})