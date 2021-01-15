from django import forms
from django.forms import fields
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from core.models import User


class UserCreationForm(BaseUserCreationForm):
    username = fields.CharField(
        label=_('Username'),
    )
    password1 = fields.CharField(
        widget=forms.PasswordInput,
        label=_('Password'),
    )
    password2 = fields.CharField(
        widget=forms.PasswordInput,
        label=_('Confirm Password'),
        help_text=_(
            'Enter the password again.'
        ),
    )
    email = fields.EmailField(
        label=_('Email')
    )
    first_name = fields.CharField(
        label=_('First Name'),
    )
    last_name = fields.CharField(
        label=_('Last Name'),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
        )

    fields_order = [
        'username',
        'password1',
        'password2',
        'email',
        'first_name',
        'last_name',
    ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

class UserChangeForm(BaseUserChangeForm):
    password = None
    username = fields.CharField(
        label=_('Username'),
    )
    email = fields.EmailField(
        label=_('Email')
    )
    first_name = fields.CharField(
        label=_('First Name'),
    )
    last_name = fields.CharField(
        label=_('Last Name'),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    fields_order = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
