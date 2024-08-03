from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import ListView
from .models import Client


def get_chats(request: HttpRequest):
    return render(request, template_name='chats.html', context={})


def user_profile(request: HttpRequest):
    if request.method == 'GET':
        return render(request, template_name='user_profile.html')
    elif request.method == 'POST':
        pass


class FindUsersListView(ListView):
    model = Client
    template_name = 'find_users.html'
    context_object_name = 'all_find'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        parameter_find = self.request.GET.get('user')
        if parameter_find:
            list_firstnames_users = Client.objects.filter(first_name__icontains=parameter_find)
            list_lastname_users = Client.objects.filter(last_name__icontains=parameter_find)
            queryset = list_firstnames_users + list_lastname_users
        else:
            queryset = []
        return queryset
