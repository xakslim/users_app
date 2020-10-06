from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from snippets.admin import activate_action, deactivate_action, BaseModelAdmin
from users.forms import UserAdminForm, UserCreationForm
from users import models


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass


@admin.register(models.User)
class UserAdmin(UserAdmin):
    """Пользователи"""
    actions = (activate_action, deactivate_action)
    add_form = UserCreationForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('is_active', 'username', 'password', 'created', 'updated')
        }),
        (_('Персональная информация'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('last_name', 'first_name', 'email')
        }),
        (_('Важные даты'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('last_login', 'date_joined')
        }),
        (_('Права доступа'), {
            'classes': ('suit-tab', 'suit-tab-permission'),
            'fields': ('is_staff', 'is_superuser', 'user_permissions')
        })
    )
    form = UserAdminForm
    list_display = ('username', 'get_full_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    readonly_fields = ('last_login', 'date_joined', 'created', 'updated')
    search_fields = ('=id', 'username', 'full_name', 'email')
    suit_form_tabs = (
        ('general', _('Общее')),
        ('permission', _('Права'))
    )

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if 'delete_selected' in actions and not request.user.is_superuser:
            del actions['delete_selected']
        return actions


@admin.register(models.UserCategory)
class UserCategoryAdmin(BaseModelAdmin, admin.ModelAdmin):
    fields = models.UserCategory().collect_fields()
    group_fieldsets = True
    list_editable = ('status', 'ordering')
    ordering = ('ordering',)


@admin.register(models.UserRole)
class UserRoleAdmin(BaseModelAdmin, admin.ModelAdmin):
    fields = models.UserRole().collect_fields()
    group_fieldsets = True
    list_editable = ('status', 'ordering')
    ordering = ('ordering',)
