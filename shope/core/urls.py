from django.urls import path

from core.views import BaseView, AboutView, SetupAdminView, CacheUpdateView


urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('setup-admin/', SetupAdminView.as_view(), name='setup-admin'),
    path('edit-cache/<int:pk>/', CacheUpdateView.as_view(), name='edit-cache')
]
