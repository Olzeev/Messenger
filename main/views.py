from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import models as django_models
from .forms import *
from .models import *
from django.views.generic import View
from django.http import JsonResponse


def find_last_communicated(request):
    messages = (Message.objects.filter(id_sender=request.user.id) | Message.objects.filter(id_reciever=request.user.id)).order_by("-time")
    users = []

    for message in messages:
        if int(message.id_sender) == request.user.id:
            if message.id_reciever not in users:
                users.append(message.id_reciever)
        elif int(message.id_reciever) == request.user.id:
            if message.id_sender not in users:
                users.append(message.id_sender)
                
    users_found = []

    index = 0
    for user_id in users:
        user = get_user_model().objects.get(id=user_id)
        user_info = User_info.objects.get(user_info_id=user_id)

        users_found.append([user.first_name, user_info.status, user_info.avatar.url, user.id, index])
        index += 1
    return users_found


def index(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')
    else:
        users_found = find_last_communicated(request)
        return render(request, 'main/index.html', {"users": users_found, 
                                                   "length": len(users_found), 
                                                   "username": request.user.first_name, 
                                                   "avatar": User_info.objects.get(user_info_id=request.user.id).avatar.url, 
                                                   "user_id": request.user.id, 
                                                   "blocked": False, 
                                                   "is_blocked": False})
    

def sign_in(request):
    error = ''
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['email'], password=form.data["password"])
            if user is not None:
                login(request, user)
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
            user_info = User_info(user_info_id=request.user.id)
            
            user_info.save()
            return redirect('edit_info')
    else:
        form = SignUpForm()
    return render(request, 'main/sign_up.html', { 'error': error })


def log_out(request):
    logout(request)
    return redirect('sign_in')

def edit_info(request):
    if request.method == "POST":
        form = EditInfoForm(request.POST, request.FILES)
        if form.is_valid():
            user_info = User_info.objects.get(user_info_id=request.user.id)
            user_info.status = form.data["status"]
            if form.data["username"]:
                request.user.first_name = form.data["username"]
            else:
                request.user.first_name = f"User{request.user.id}"
            request.user.save()
            if len(request.FILES) != 0:
                user_info.avatar = request.FILES["avatar"]
            user_info.save()
            return redirect('main')
    else:
        form = EditInfoForm()
        username = request.user.first_name
        user_info = User_info.objects.get(user_info_id=request.user.id)
        status = user_info.status
        avatar = user_info.avatar
    return render(request,"main/edit_info.html", {'username': username, 
                                                  "status": status, 
                                                  'avatar': avatar})

                                            
def settings(request):
    username = request.user.first_name
    email = request.user.email
    user_info = User_info.objects.get(user_info_id=str(request.user.id))
    return render(request, 'main/settings.html', {'avatar': user_info.avatar, 
                                                    'status': user_info.status})

class SearchPersonView(View):
    def get(self, request):
        text = request.GET.get('search_input_text')
        if not text:
            users_found = find_last_communicated(request)

            return JsonResponse({'users_found': users_found}, status=200)
        users_found = []
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            if text.lower() in user.first_name.lower() and user.id != request.user.id:
                
                user_info = User_info.objects.get(user_info_id=user.id)

                messages = ((Message.objects.filter(id_sender=str(request.user.id), id_reciever=str(user.id)) | Message.objects.filter(id_reciever=str(request.user.id), id_sender=str(user.id)))).order_by("time")
                if len(messages) != 0:
                    status = messages.reverse()[0].text
                else:
                    status = user_info.status
                avatar = user_info.avatar
                users_found.append([user.first_name, status, avatar.url, user.id])
        return JsonResponse({'users_found': users_found}, status=200)

        #return render(request, 'main/index.html')

class SendMessageView(View):
    def get(self, request):
        text = request.GET.get('message_text')
        id_reciever = request.GET.get('id')
        if not User_blocked.objects.filter(user_id=str(request.user.id), id_user_blocked=id_reciever).exists() and \
            not User_blocked.objects.filter(user_id=id_reciever, id_user_blocked=str(request.user.id)).exists():
            message = Message(id_sender=request.user.id, id_reciever=id_reciever, text=text, time=timezone.now())
            message.save()
            return JsonResponse({'time': timezone.now(), 
                                'id_sender': request.user.id}, status=200)


class GetMessagesView(View):
    def get(self, request):
        id_with = request.GET.get('id')
        
        blocked = User_blocked.objects.filter(user_id=str(request.user.id), id_user_blocked=str(id_with)).exists()
        is_blocked = User_blocked.objects.filter(user_id=str(id_with), id_user_blocked=str(request.user.id)).exists()

        messages = (Message.objects.filter(id_sender=str(request.user.id), id_reciever=id_with) | Message.objects.filter(id_reciever=str(request.user.id), id_sender=id_with))
        messages_send = []
        for message in messages:
            messages_send.append([message.text, message.time, 1 if message.id_sender==str(request.user.id) else 0])
        return JsonResponse({'messages': messages_send, 
                            'blocked': blocked, 
                            'is_blocked': is_blocked, 
                            'user_id': str(request.user.id)}, status=200)


class BlockUserView(View):
    def get(self, request):
        id_blocking = request.GET.get('user_id_blocking')
        id_blocked = request.GET.get('user_id_blocked')

        user_blocked = User_blocked(user_id=id_blocking, id_user_blocked=id_blocked)
        user_blocked.save()
        return JsonResponse({}, status=200)


class UnblockUserView(View):
    def get(self, request):
        id_unblocking = request.GET.get('user_id_unblocking')
        id_unblocked = request.GET.get('user_id_unblocked')

        User_blocked.objects.get(user_id=id_unblocking, id_user_blocked=id_unblocked).delete()
        is_blocked = User_blocked.objects.filter(user_id=id_unblocked, id_user_blocked=id_unblocking).exists()

        return JsonResponse({'is_blocked': is_blocked}, status=200)


class ClearHistoryView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        Message.objects.filter(id_sender=str(request.user.id), id_reciever=str(user_id)).delete()
        Message.objects.filter(id_sender=str(user_id), id_reciever=str(request.user.id)).delete()
        print(user_id, request.user.id)

        return JsonResponse({}, status=200)

class GetId(View):
    def get(self, request):
        return JsonResponse({'id': str(request.user.id) }, status=200)


