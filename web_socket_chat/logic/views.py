from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import login, authenticate, logout
from .models import User, Chat
from . import forms


def get_chats(request: HttpRequest):
    if request.user.is_authenticated:
        current_user = request.user
        chats = Chat.objects.filter(
            Q(first_user=current_user) | Q(second_user=current_user)
        ).prefetch_related('first_user', 'second_user')

        users_in_chats = set()
        for chat in chats:
            if chat.first_user != current_user:
                users_in_chats.add(chat.first_user)
            if chat.second_user != current_user:
                users_in_chats.add(chat.second_user)

        paginator = Paginator(QuerySet(users_in_chats), 15)

        return render(request, template_name='chats.html', context={'users': users_in_chats})
    else:
        return redirect('login')


def user_profile(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, template_name='user_profile.html', context={'user': request.user})
        elif request.method == 'POST':
            params = request.POST.dict()
            user = User.objects.get(id=request.user.id)
            if 'avatar' in request.FILES:
                user.avatar.delete(save=False)
                user.avatar = request.FILES['avatar']
            user.username = params['username']
            user.first_name = params['first_name']
            user.last_name = params['last_name']
            user.save()
            return render(request, template_name='user_profile.html', context={'user': user})
    else:
        return redirect('login')


def registration(request: HttpRequest):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return render(request, template_name='chats.html')
    elif request.method == 'GET':
        form = forms.RegisterUserForm()
        return render(request, template_name='registration/registration.html', context={'form': form})


def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('get_chats'))
            else:
                return render(request, template_name='registration/login.html', context={'message': 'Invalid first name or/and password', 'form': form})
        else:
            return render(request, template_name='registration/login.html', context={'message': 'Invalid first name or/and password', 'form': form})
    elif request.method == 'GET':
        return render(request, template_name='registration/login.html', context={'form': forms.LoginUserForm})


def logout_view(request: HttpRequest):
    if request.method == 'GET':
        logout(request)
        return redirect('login')


class FindUsersListView(ListView):
    model = User
    template_name = 'find_users.html'
    context_object_name = 'users'
    paginate_by = 14

    def get_queryset(self):
        queryset = super().get_queryset()
        parameter_find = self.request.GET.get('user')
        if parameter_find:
            users = User.objects.filter(Q(username__icontains=parameter_find) |
                Q(first_name__icontains=parameter_find) |
                Q(last_name__icontains=parameter_find)
                )
            self.users = users
        else:
            self.users = []
        return self.users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['users'] = self.users
        context['user'] = current_user
        return context


class CreateChatView(View):
    def get(self, request, pk):
        user_for_id = User.objects.get(id=pk)
        chat, created = Chat.objects.get_or_create(first_user=self.request.user, second_user=user_for_id)
        return redirect('get_chat', pk=chat.pk)


class ChatView(DetailView):
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_user = self.request.user
        chat = Chat.objects.get(pk=self.kwargs.get('pk'))

        second_user = None

        if chat.first_user != current_user:
            second_user = chat.first_user
        elif chat.second_user != current_user:
            second_user = chat.second_user

        context['current_user'] = current_user
        context['second_user'] = second_user

        return context
