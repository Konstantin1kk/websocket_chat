from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

    def __str__(self):
        return f'{self.user.name}'

    class Meta:
        verbose_name = 'user'
        app_label = 'logic'


class Chat(models.Model):
    id_chat = models.IntegerField(unique=True)
    first_user = models.IntegerField()
    second_user = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'chat'
        app_label = 'logic'


class Message(models.Model):
    id_message = models.IntegerField(unique=True)
    text = models.CharField(max_length=255)
    id_chat = models.ForeignKey(to='Chat', on_delete=models.CASCADE)
    id_sender = models.GenericIPAddressField(max_length=15)
    id_recipient = models.IntegerField()
    message_isread = models.BooleanField()
    time_send_message = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'message'
        app_label = 'logic'
