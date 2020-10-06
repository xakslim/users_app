import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from entities import models as entity_models


from snippets.models import LastModMixin, BaseModel, BasicModel
from users.managers import UserManager


class UserCategory(BaseModel):
    """Категория работника"""
    title = models.CharField(_('Категория'), max_length=255, db_index=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('Категория работника')
        verbose_name_plural = _('Категории работника')

    def __str__(self):
        return self.title


class UserRole(BaseModel):
    """Роль работника"""
    title = models.CharField(_('Роль'), max_length=255, db_index=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('Роль работника')
        verbose_name_plural = _('Роли работника')

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin, LastModMixin, BasicModel):
    """Модель профилей"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('Имя учетной записи'),
        max_length=60,
        unique=True,
        help_text=_('Максимум 60 символов. Буквы, числа знакии: @/./+/-/_ .'),
        validators=[username_validator],
        error_messages={
            'unique': _("Данное имя уже используется"),
        },
    )
    first_name = models.CharField(_('Фамилия'), max_length=60)
    last_name = models.CharField(verbose_name=_('Имя'), max_length=60, blank=True, null=True)
    middle_name = models.CharField(_('Отчество'), max_length=60, blank=True, null=True)
    full_name = models.CharField(_('ФИО'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('Адрес электронной почты'))
    position = models.CharField(_('Должность'), max_length=60, blank=True, null=True)
    work_phone = models.CharField(_('Рабочий телефон'), max_length=60, blank=True, null=True)
    mobile_phone = models.CharField(_('Мобильный телефон'), max_length=60, blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(_('Запись асктивна'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    category = models.ForeignKey(
        UserCategory, verbose_name=_('Категория пользователя'), related_name='categories', on_delete=models.CASCADE,
        blank=True, null=True
    )
    role = models.ForeignKey(
        UserRole, verbose_name=_('Роль пользователя'), related_name='roles', on_delete=models.CASCADE,
        blank=True, null=True
    )
    entity = models.ForeignKey(
        entity_models.Entity, verbose_name=_('Организация'), related_name='entities', on_delete=models.CASCADE,
        blank=True, null=True
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.full_name

    def get_full_name(self):
        parts = filter(
            None, (self.last_name, self.first_name, self.middle_name)
        )
        full_name = ' '.join(parts)

        return full_name or self.username

    get_full_name.short_description = 'Полное имя'
    get_full_name.admin_order_field = 'full_name'

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super(User, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

