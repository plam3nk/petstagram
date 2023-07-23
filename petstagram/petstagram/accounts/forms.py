from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_form

UserModel = get_user_model()


class RegisterUserForm(auth_form.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'something'
            })
        }

# class EditUserForm()