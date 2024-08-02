from django.shortcuts import render
from django.http import HttpRequest
from .models import User


def get_chats(request: HttpRequest):
    return render(request, template_name='chats.html', context={})


def user_profile(request: HttpRequest):
    if request.method == 'GET':
        return render(request, template_name='user_profile.html')


def get_find_users(request: HttpRequest):
    if request.method == 'GET':
        find_user = request.GET.get('user')
        if find_user:
            list_names_users = User.objects.filter(name__icontains=find_user)
            list_lastname_users = User.objects.filter(last_name__icontains=find_user)
            all_find = list_names_users + list_lastname_users
            return render(request, template_name='find_users.html', context={'found_users': all_find})
        else:
            return render(request, template_name='find_users.html', context={'users': User.objects.all()})
