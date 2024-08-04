from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . import models

admin.site.register(models.User, UserAdmin)
