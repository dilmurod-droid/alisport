from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import BotUser


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = BotUser
        fields = ['username','phone_number']