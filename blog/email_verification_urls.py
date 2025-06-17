from django.urls import path
from .email_verification_views import (
    SendVerificationCodeView,
    VerifyCodeView,
    ResendVerificationCodeView,
    PasswordResetConfirmView,
    EmailVerificationStatusView
)

urlpatterns = [
    # Send verification code (for both registration and password reset)
    path('send-code/', SendVerificationCodeView.as_view(), name='send-verification-code'),
    
    # Verify verification code
    path('verify-code/', VerifyCodeView.as_view(), name='verify-verification-code'),
    
    # Resend verification code
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-verification-code'),
    
    # Confirm password reset with verified code
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Check verification status
    path('status/', EmailVerificationStatusView.as_view(), name='verification-status'),
] 