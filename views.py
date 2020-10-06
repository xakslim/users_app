from copy import deepcopy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views

from snippets.http.response import success_response, form_validation_error_response, error_response

from snippets.views import BaseTemplateView
from users import forms
from users import models as user_models


class UserView(CreateView):
    """Вывод организации"""
    template_name = 'users/user_card.html'
    form_class = forms.UserAdminForm

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context.update(
            form=form
        )

        return context


class UserListView(BaseTemplateView):
    """Страница перечня работников"""
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs, ):
        context = super(UserListView, self).get_context_data(**kwargs)

        sort_mapping = {
            'name_asc': 'full_name',
            'name_dsc': '-full_name',
            'role_asc': 'role__title',
            'role_dsc': '-role__title',
            'email_asc': 'email',
            'email_dsc': '-email',
            'pos_asc': 'position',
            'pos_dsc': '-position'
        }

        sorting = self.request.GET.get('s', 'name_asc')
        if sorting and sorting in sort_mapping:

            users = user_models.User.objects.all().order_by(sort_mapping[sorting])
        else:
            sorting = 'name_asc'
            users = user_models.User.objects.all().order_by('name_asc')

        context.update(
            users=users,
            sorting=sorting,
        )

        return context


class UserCreationView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'users/user_card.html'
    success_message = 'Ваш запрос благополучно отправлен'

    def get_context_data(self, **kwargs):
        context = super(UserCreationView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context.update(
            form=form
        )

        return context

    def post(self, request, **kwargs):
        data = deepcopy(request.POST)
        form = self.form_class(data)

        if form.is_valid():
            form.instance.is_active = True
            form.instance.is_staff = True
            role = str(form.cleaned_data['role'].pk)
            if role == '40b280fc-53d0-4c61-a219-459c314bcbc8':
                form.instance.is_superuser = True

            post = form.save()

            return redirect('users:user_edit', pk=post.pk)

        return form_validation_error_response(form.errors)


def user_edit(request, **kwargs):
    # pk = user_models.User.objects.all().first().pk
    post = get_object_or_404(user_models.User, pk__exact=kwargs.get('pk'))
    template_name = 'users/user_edit.html'

    if request.method == "POST":
        form = forms.UserChangeForm(request.POST, instance=post)
        if form.is_valid():
            form.instance.password = form.cleaned_data['password']
            form.instance.is_active = True
            form.instance.is_staff = True
            role = str(form.cleaned_data['role'].pk)
            if role == '40b280fc-53d0-4c61-a219-459c314bcbc8':
                form.instance.is_superuser = True
            form.save()
            # return success_response(self.success_message)
            return redirect('users:user_edit', pk=post.pk)
        else:
            return form_validation_error_response(form.errors)
    else:
        form = forms.UserChangeForm(instance=post)
    return render(request, template_name, {'form': form})


class UserLogin(auth_views.LoginView):
    template_name = 'registration/login.html'
    template_engine = 'jinja2'
    content_type = 'text/html'


class UserLogout(auth_views.LogoutView):
    template_engine = 'jinja2'
    content_type = 'text/html'


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    template_engine = 'jinja2'
    content_type = 'text/html'
    success_url = '/password-reset/done/'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_engine = 'jinja2'
    content_type = 'text/html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = '/reset/done/'
    template_engine = 'jinja2'
    content_type = 'text/html'


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_engine = 'jinja2'
    content_type = 'text/html'

