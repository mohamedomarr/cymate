from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.models import Group

from .serializers import CustomRegisterSerializer
from .email_verification_service import EmailVerificationService
from .models import EmailVerification

User = get_user_model()


class EnhancedRegistrationView(APIView):
    """
    Enhanced registration view that requires email verification
    
    POST /api/auth/enhanced-registration/
    {
        "username": "testuser",
        "email": "user@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "John",
        "last_name": "Doe",
        "verification_code": "123456"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        verification_code = request.data.get('verification_code')
        email = request.data.get('email')
        
        if not verification_code:
            return Response({
                'error': 'Verification code is required',
                'detail': 'Please verify your email first by requesting a verification code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the email verification code first
        success, message, verification = EmailVerificationService.verify_code(
            email=email,
            code=verification_code,
            verification_type='registration'
        )
        
        if not success:
            return Response({
                'error': 'Email verification failed',
                'detail': message
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a copy of request data without verification_code for serializer
        registration_data = request.data.copy()
        registration_data.pop('verification_code', None)
        
        # Validate registration data
        serializer = CustomRegisterSerializer(data=registration_data)
        
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user with verified email
        try:
            with transaction.atomic():
                # Save the user
                user = serializer.save(request)
                
                # Mark email as verified since we verified it above
                user.emailaddress_set.filter(email=email).update(verified=True)
                
                return Response({
                    'message': 'Registration successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email_verified': True
                    }
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': f'Registration failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PreRegistrationEmailVerificationView(APIView):
    """
    View to send email verification before registration
    
    POST /api/auth/pre-registration-verify/
    {
        "email": "user@example.com"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'User with this email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Send verification code
        try:
            verification = EmailVerificationService.create_verification_code(
                email=email,
                verification_type='registration'
            )
            
            email_sent = EmailVerificationService.send_verification_email(
                email=email,
                code=verification.code,
                verification_type='registration'
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