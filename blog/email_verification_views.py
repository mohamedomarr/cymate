import secrets
import hashlib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from .serializer import (
    SendVerificationCodeSerializer,
    VerifyCodeSerializer,
    PasswordResetConfirmSerializer
)
from .email_verification_service import EmailVerificationService
from .models import EmailVerification

User = get_user_model()


class SendVerificationCodeView(APIView):
    """
    API endpoint to send verification codes for registration or password reset
    
    POST /api/email-verification/send-code/
    {
        "email": "user@example.com",
        "verification_type": "registration"  // or "password_reset"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        verification_type = serializer.validated_data['verification_type']
        
        # Get user if exists (for password reset)
        user = EmailVerificationService.get_user_by_email(email)
        
        # Create and send verification code
        try:
            verification = EmailVerificationService.create_verification_code(
                email=email,
                verification_type=verification_type,
                user=user
            )
            
            email_sent = EmailVerificationService.send_verification_email(
                email=email,
                code=verification.code,
                verification_type=verification_type,
                user=user
            )
            
            if email_sent:
                return Response({
                    'message': 'Verification code sent successfully',
                    'email': email,
                    'expires_in_minutes': EmailVerificationService.CODE_EXPIRY_MINUTES
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send verification email'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'error': f'Failed to send verification code: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyCodeView(APIView):
    """
    API endpoint to verify verification codes
    
    POST /api/email-verification/verify-code/
    {
        "email": "user@example.com",
        "code": "123456",
        "verification_type": "registration"  // or "password_reset"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        verification_type = serializer.validated_data['verification_type']
        
        # Verify the code
        success, message, verification = EmailVerificationService.verify_code(
            email=email,
            code=code,
            verification_type=verification_type
        )
        
        if success:
            # Generate a temporary token for password reset flow
            verification_token = None
            if verification_type == 'password_reset':
                verification_token = self._generate_verification_token(email)
            
            response_data = {
                'message': message,
                'email': email,
                'verification_type': verification_type,
                'verified_at': verification.created_at if verification else timezone.now()
            }
            
            if verification_token:
                response_data['verification_token'] = verification_token
                response_data['token_expires_in_minutes'] = 30  # Token valid for 30 minutes
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': message
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_verification_token(self, email):
        """
        Generate a secure token for password reset confirmation
        This token will be used to verify that the user has verified their email
        """
        # Create a secure token based on email and current time
        timestamp = str(int(timezone.now().timestamp()))
        secret_key = getattr(settings, 'SECRET_KEY', 'fallback-key')
        token_data = f"{email}:{timestamp}:{secret_key}"
        
        # Generate hash
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        # Store token temporarily (in a real app, you might want to store this in cache/database)
        # For simplicity, we'll include timestamp in token for validation
        return f"{token}:{timestamp}"


class ResendVerificationCodeView(APIView):
    """
    API endpoint to resend verification codes
    
    POST /api/email-verification/resend-code/
    {
        "email": "user@example.com",
        "verification_type": "registration"  // or "password_reset"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        verification_type = serializer.validated_data['verification_type']
        
        # Get user if exists
        user = EmailVerificationService.get_user_by_email(email)
        
        # Resend verification code
        success, message = EmailVerificationService.resend_verification_code(
            email=email,
            verification_type=verification_type,
            user=user
        )
        
        if success:
            return Response({
                'message': message,
                'email': email,
                'expires_in_minutes': EmailVerificationService.CODE_EXPIRY_MINUTES
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset with verified email
    
    POST /api/email-verification/reset-password-confirm/
    {
        "email": "user@example.com",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123",
        "verification_token": "token_from_verify_code_response"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        verification_token = serializer.validated_data['verification_token']
        
        # Validate the verification token
        if not self._validate_verification_token(email, verification_token):
            return Response({
                'error': 'Invalid or expired verification token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validate new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({
                'error': 'Password validation failed',
                'details': list(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update password
        try:
            user.set_password(new_password)
            user.save()
            
            # Clean up any remaining verification codes for this user
            EmailVerification.objects.filter(
                email=email,
                verification_type='password_reset'
            ).delete()
            
            return Response({
                'message': 'Password reset successfully',
                'email': email
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to reset password: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _validate_verification_token(self, email, token):
        """
        Validate the verification token
        Token format: hash:timestamp
        """
        try:
            from django.conf import settings
            
            if ':' not in token:
                return False
            
            token_hash, timestamp = token.rsplit(':', 1)
            
            # Check if token is not too old (30 minutes)
            token_time = int(timestamp)
            current_time = int(timezone.now().timestamp())
            
            if current_time - token_time > 1800:  # 30 minutes
                return False
            
            # Regenerate expected token
            secret_key = getattr(settings, 'SECRET_KEY', 'fallback-key')
            token_data = f"{email}:{timestamp}:{secret_key}"
            expected_hash = hashlib.sha256(token_data.encode()).hexdigest()
            
            return token_hash == expected_hash
            
        except (ValueError, TypeError):
            return False


class EmailVerificationStatusView(APIView):
    """
    API endpoint to check email verification status
    
    GET /api/email-verification/status/?email=user@example.com&type=registration
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        email = request.query_params.get('email')
        verification_type = request.query_params.get('type')
        
        if not email or not verification_type:
            return Response({
                'error': 'Email and type parameters are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for valid verification codes
        active_verification = EmailVerification.objects.filter(
            email=email,
            verification_type=verification_type,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if active_verification:
            return Response({
                'has_active_code': True,
                'expires_at': active_verification.expires_at,
                'created_at': active_verification.created_at
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'has_active_code': False,
                'message': 'No active verification code found'
            }, status=status.HTTP_200_OK) 