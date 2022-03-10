from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in (
                self.fields['email'], self.fields['username'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control '})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
