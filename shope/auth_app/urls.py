from django.urls import path
from django.views.generic import TemplateView


from .views import SetNewPasswordView, ForgotPasswordView, \
    RegisterView, UserLogoutView, UserLoginView

app_name = 'auth_app'

urlpatterns = [
    # registration
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', TemplateView.as_view(template_name='auth_app/confirm-email.html'), name='confirm-email'),
    path('verify_email/<str:email>/<str:activate_key>/', RegisterView.verify, name='verify_email'),
    # login
    path('login/', UserLoginView.as_view(), name='login'),
    # logout
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # set new password
    path('forgot-password/', ForgotPasswordView.as_view(), name='e-mail'),
    path('check_email_for_password_restore/',
         TemplateView.as_view(template_name='auth_app/change_password_success.html'),
         name='check_email_for_password_restore'),
    path('set-new-password/<str:uidb64>/<str:token>/', SetNewPasswordView.as_view(),
         name='restore_password'),
]
