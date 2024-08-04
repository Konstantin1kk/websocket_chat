from itertools import chain
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.views import LoginView, LogoutView
from .models import User, Chat
from . import forms


def get_chats(request: HttpRequest):
    return render(request, template_name='chats.html', context={})


def get_chat(request: HttpRequest):
    if request.method == 'GET':
        id_chat = request.GET.get()
        return render(request, template_name='chat.html')
    elif request.method == 'POST':
        pass


def user_profile(request: HttpRequest):
    if request.method == 'GET':
        return render(request, template_name='user_profile.html')
    elif request.method == 'POST':
        pass


def registration(request: HttpRequest):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, template_name='chats.html')
    elif request.method == 'GET':
        form = forms.RegisterUserForm()
        return render(request, template_name='registration/registration.html', context={'form': form})


class FindUsersListView(ListView):
    model = User
    template_name = 'find_users.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        parameter_find = self.request.GET.get('user')
        if parameter_find:
            username_users = User.objects.filter(username__icontains=parameter_find)
            list_firstnames_users = User.objects.filter(first_name__icontains=parameter_find)
            list_lastname_users = User.objects.filter(last_name__icontains=parameter_find)
            self.users = list(chain(list_firstnames_users, list_lastname_users, username_users))
        else:
            self.users = []
        return self.users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.users
        return context


class CreateChatView(View):
    def get(self, request, pk):
        user_for_id = User.objects.get(id=pk)
        chat, created = Chat.objects.get_or_create(first_user=self.request.user, second_user=user_for_id)

        return redirect(to='get_chat', pk=chat.pk)


class ChatView(DetailView):
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'chat'


class Login(LoginView):
    template_name = 'registration/login.html'


class Logout(LogoutView):
    template_name = 'registration/logout.html'
