from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import Member


class MemberCreationForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ("username",)
        field_classes = {'username': UsernameField}

class MemberChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = '__all__'
        field_classes = {'username': UsernameField}