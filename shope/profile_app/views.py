"""Views for profile app"""

from typing import Any
import inject
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

from django.views.generic import (
    UpdateView,
    DetailView
)

from .forms import EditUserForm, EditProfileForm, CustomPasswordChangeForm
from interface.order_interface import IOrder


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование данных пользователя"""
    model = Profile
    template_name = 'profile_app/profile.html'
    form_class = EditProfileForm
    _SUCCESS_MESSAGE = _('Your profile has been updated')

    def get_success_url(self) -> str:
        return reverse('profile')

    def get_object(self, *args, **kwargs):
        """get object"""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """get context data"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = EditUserForm(self.request.POST,
                                                instance=self.request.user)
            context['password_form'] = CustomPasswordChangeForm(self.request.user,
                                                                self.request.POST)
        else:
            context['user_form'] = EditUserForm(instance=self.request.user)
            context['password_form'] = CustomPasswordChangeForm(self.request.user)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        user_form = context['user_form']
        password_form = context['password_form']
        valid_list = [form.is_valid(), user_form.is_valid()]
        if password_form.has_changed():
            valid_list.append(password_form.is_valid())

        if all(valid_list):
            user_form.save()
            form.save()

            if password_form.has_changed():
                password_form.save()
                update_session_auth_hash(self.request, password_form.user)

        else:
            context.update({'user_form': user_form,
                            'password_form': password_form})

            return self.render_to_response(context)
        messages.success(self.request, self._SUCCESS_MESSAGE)
        return super().form_valid(form)


class AccountView(LoginRequiredMixin, DetailView):
    """Аккаунт пользователя"""

    template_name = 'profile_app/account.html'
    model = Profile
    _last_order: IOrder = inject.attr(IOrder)

    def get_object(self, *args, **kwargs):
        """get object"""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_order'] = self._last_order.get_last_by_user(self.request.user)
        return context
