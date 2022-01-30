from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from account.models import Account


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class UpdateFirstNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',)


class UpdateLastNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name',)


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('image',)