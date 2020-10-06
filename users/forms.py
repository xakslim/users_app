from django import forms
from django.contrib.auth import forms as auth_forms

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users import models


class UserAdminForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(
        label='Пароль',
        help_text=_(
             'Raw passwords are not stored, so there is no way to see '
             'this user\'s password, but you can change the password '
             'using <a href="../password/">this form</a>.'
        )
    )

    class Meta:
        model = models.User
        fields = '__all__'
        exclude = ['password', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

    def clean_password(self):
        return self.initial['password']

    def clean_username(self):
        return str(self.cleaned_data.get('username'))


class UserCreationForm(auth_forms.UserCreationForm):
    # Form from contrib.auth. Because of:
    # https://code.djangoproject.com/ticket/20086
    class Meta:
        model = models.User
        fields = '__all__'
        exclude = ('date_joined',)
        # ('username', 'password1', 'password2')
        error_messages = {
            'password1': {
                'required': _('Please enter a password.')
            },
            'password2': {
                'required': _('Please enter a password.')
            }
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

    def clean_username(self):
        username = str(self.cleaned_data.get('username'))

        if models.User._default_manager.filter(username=username).exists():
            self.add_error('username', 'Пользователь с указанным логином уже есть в системе')

        return username


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = models.User
        fields = '__all__'
        exclude = (
            'date_joined', 'is_superuser', 'user_permissions',
            'is_active'
        )
