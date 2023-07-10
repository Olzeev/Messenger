from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import models as django_models
from .forms import *
from .models import *
from django.views.generic import View
from django.http import JsonResponse

def index(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')
    else:
        return render(request, 'main/index.html')
    

def sign_in(request):
    error = ''
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['email'], password=form.data["password"])
            if user is not None:
                login(request, user)
                print('aowiejfoiwjef')
                return redirect('main')
            else:
                error = 'Неверная эл.почта или пароль!'
    else:
        form = SignInForm()

    return render(request, 'main/sign_in.html', {"error": error})


def sign_up(request):
    error = ''
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            users = User.objects.all()
            for user in users:
                if user.username == form.data["email"]:
                    error = 'Пользователь уже существует!'
                    return render(request, 'main/sign_up.html', { "error": error })
            if form.data["password"] != form.data["password_check"]:
                error = 'Пароли должны совпадать!'
                return render(request, 'main/sign_up.html', { "error": error })
            
            user = django_models.User.objects.create_user(username=form.data["email"], password=form.data["password"])
            login(request, user)
            #user_info = User_info(username=form.data["email"])
            #user_info.save()
            return redirect('main')
    else:
        form = SignUpForm()
    return render(request, 'main/sign_up.html', { 'error': error })


def log_out(request):
    logout(request)
    return redirect('sign_in')

class SearchPersonView(View):
    def get(self, request):
        text = request.GET.get('search_input_text')
        
        users_found = []
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            if text in user.username:
                users_found.append(user.username)
        return JsonResponse({'users_found': users_found}, status=200)

        #return render(request, 'main/index.html')