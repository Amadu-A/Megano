from django.urls import path

from .views import (
    EditProfileView,
    AccountView,
)


urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', EditProfileView.as_view(), name='profile'),
]
