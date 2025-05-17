from django.urls import path
from .views import (
    RegisterView, ValidateTokenView, ConfirmEmailView, 
    ResendConfirmationEmailView, LoginView
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/validate/', ValidateTokenView.as_view(), name='token_validate'),
    path('confirm-email/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('resend-confirmation/', ResendConfirmationEmailView.as_view(), name='resend-confirmation'),
]