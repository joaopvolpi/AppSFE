from __future__ import unicode_literals
from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
'''
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
'''

admin.site.register(Palestra)
admin.site.register(User)


'''
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('nome', 'email', 'dre',)
    list_filter = ('nome', 'email', 'dre',)
'''




