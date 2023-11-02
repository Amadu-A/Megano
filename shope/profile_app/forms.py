"""Forms for Profile app"""

from django import forms
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile
from auth_app.models import User


class EditUserForm(UserChangeForm):
    """Форма редактирования данных пользователя"""
    email = forms.EmailField(label=_('Email'),
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-input',
                                        'id': 'mail',
                                        'data-validate': 'require',
                                        'readonly': True}
    )
    )

    middle_name = forms.CharField(label=_('Full name'),
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-input',
                                             'id': 'name',
                                             'data-validate': 'require'}
    )
    )

    class Meta:
        """Meta Class"""
        model = User
        fields = [
            'email',
            'middle_name',
        ]


class EditProfileForm(forms.ModelForm):
    """Форма редактирования профайла пользователя"""
    phone = PhoneNumberField(label=_('Phone'),
                             required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-input',
                                        'id': 'phone',
                                        'name': 'phone',
                                        'data-validate': 'require'
                                        }))

    avatar = forms.ImageField(label=_('Avatar'),
                              required=False,
                              widget=forms.FileInput(
                                  attrs={'class': 'Profile-file form-input',
                                         'id': 'avatar',
                                         'name': 'avatar',
                                         'data-validate': 'onlyImgAvatar'}))

    class Meta:
        """Meta Class"""
        model = Profile
        fields = [
            'phone',
            'avatar',
        ]


class CustomPasswordChangeForm(SetPasswordForm):
    """Форма изменения пароля"""
    new_password1 = forms.CharField(label=_('New password'),
                                    required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-input',
                                               'id': 'password',
                                               'type': 'password',
                                               'placeholder': _('You can change your password')}
    )
    )

    new_password2 = forms.CharField(label=_('Confirm password'),
                                    required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-input',
                                               'id': 'passwordReply',
                                               'type': 'password',
                                               'placeholder': _('Confirm password')}
    )
    )

    class Meta:
        """Meta Class"""
        model = User
