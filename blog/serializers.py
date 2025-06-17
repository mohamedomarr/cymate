from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import Profile, EmailVerification

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # Add custom fields for registration
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        })
        return data

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'job_title', 'job_status', 'brief', 
                 'years_of_experience', 'profile_image', 'phone_number')


class SendVerificationCodeSerializer(serializers.Serializer):
    """Serializer for sending verification codes"""
    email = serializers.EmailField()
    verification_type = serializers.ChoiceField(
        choices=EmailVerification.VERIFICATION_TYPES,
        help_text="Type of verification: 'registration' or 'password_reset'"
    )

    def validate_email(self, value):
        """Validate email based on verification type"""
        verification_type = self.initial_data.get('verification_type')
        
        if verification_type == 'registration':
            # For registration, email should not already exist
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("User with this email already exists")
        elif verification_type == 'password_reset':
            # For password reset, email must exist
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError("No user found with this email address")
        
        return value


class VerifyCodeSerializer(serializers.Serializer):
    """Serializer for verifying codes"""
    email = serializers.EmailField()
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        help_text="6-digit verification code"
    )
    verification_type = serializers.ChoiceField(
        choices=EmailVerification.VERIFICATION_TYPES,
        help_text="Type of verification: 'registration' or 'password_reset'"
    )

    def validate_code(self, value):
        """Validate that code contains only digits"""
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must contain only digits")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset with verified code"""
    email = serializers.EmailField()
    new_password = serializers.CharField(
        min_length=8,
        write_only=True,
        help_text="New password (minimum 8 characters)"
    )
    confirm_password = serializers.CharField(
        min_length=8,
        write_only=True,
        help_text="Confirm new password"
    )
    verification_token = serializers.CharField(
        help_text="Token received after successful code verification"
    )

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class EmailVerificationSerializer(serializers.ModelSerializer):
    """Serializer for EmailVerification model (read-only, for admin/debugging)"""
    
    class Meta:
        model = EmailVerification
        fields = ['id', 'email', 'verification_type', 'is_used', 'created_at', 'expires_at']
        read_only_fields = ['id', 'created_at']