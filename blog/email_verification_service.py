import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from .models import EmailVerification

User = get_user_model()


class EmailVerificationService:
    """
    Service class for handling email verification operations including:
    - Generating secure verification codes
    - Sending verification emails
    - Validating verification codes
    - Managing code expiration and cleanup
    """
    
    CODE_LENGTH = 6
    CODE_EXPIRY_MINUTES = 15  # Verification codes expire after 15 minutes
    
    @classmethod
    def generate_verification_code(cls):
        """
        Generate a secure 6-digit verification code
        Returns: str - 6-digit numeric code
        """
        return ''.join(random.choices(string.digits, k=cls.CODE_LENGTH))
    
    @classmethod
    def create_verification_code(cls, email, verification_type, user=None):
        """
        Create a new verification code for the given email and type
        
        Args:
            email (str): Email address to send verification to
            verification_type (str): Type of verification ('registration' or 'password_reset')
            user (User, optional): Associated user object
            
        Returns:
            EmailVerification: Created verification instance
        """
        # Cleanup any existing codes for this email and type
        EmailVerification.objects.filter(
            email=email,
            verification_type=verification_type,
            is_used=False
        ).delete()
        
        # Generate new code and expiry time
        code = cls.generate_verification_code()
        expires_at = timezone.now() + timedelta(minutes=cls.CODE_EXPIRY_MINUTES)
        
        # Create verification record
        verification = EmailVerification.objects.create(
            email=email,
            code=code,
            verification_type=verification_type,
            user=user,
            expires_at=expires_at
        )
        
        return verification
    
    @classmethod
    def send_verification_email(cls, email, code, verification_type, user=None):
        """
        Send verification email to the specified address
        
        Args:
            email (str): Recipient email address
            code (str): Verification code to send
            verification_type (str): Type of verification
            user (User, optional): User object for personalization
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string
            
            # Determine email subject and template based on verification type
            if verification_type == 'registration':
                subject = '🎉 Welcome to CyMate - Verify Your Email'
                html_template_name = 'emails/registration_verification.html'
            elif verification_type == 'password_reset':
                subject = '🔐 CyMate Password Reset Verification'
                html_template_name = 'emails/password_reset_verification.html'
            else:
                return False
            
            # Prepare email context
            context = {
                'code': code,
                'email': email,
                'user': user,
                'expiry_minutes': cls.CODE_EXPIRY_MINUTES,
                'verification_type': verification_type,
                'support_email': getattr(settings, 'EMAIL_VERIFICATION_SUPPORT_EMAIL', 'PayifyPayments@gmail.com'),
            }
            
            # Render HTML content
            html_content = render_to_string(html_template_name, context)
            
            # Create plain text fallback
            if verification_type == 'registration':
                text_content = f"""
Welcome to CyMate!

Hi{f' {user.first_name}' if user and user.first_name else ''}!

Thank you for joining CyMate! To complete your registration, please verify your email address.

Your verification code is: {code}

This code will expire in {cls.CODE_EXPIRY_MINUTES} minutes.

Enter this code in the verification form to activate your account.

If you didn't create an account with us, please ignore this email.

Welcome aboard!
The CyMate Team

---
This email was sent to {email}. If you have any questions, contact us at {context['support_email']}.
                """
            else:  # password_reset
                text_content = f"""
CyMate Password Reset

Hi{f' {user.first_name}' if user and user.first_name else ''}!

We received a request to reset the password for your CyMate account.

Your verification code is: {code}

This code will expire in {cls.CODE_EXPIRY_MINUTES} minutes.

Enter this code in the password reset form to continue.

If you didn't request this password reset, please ignore this email. Your account remains secure.

Stay safe,
The CyMate Security Team

---
This email was sent to {email}. If you have any questions, contact us at {context['support_email']}.
                """
            
            # Create email message with HTML
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'CyMate <PayifyPayments@gmail.com>'),
                to=[email]
            )
            
            # Attach HTML version
            msg.attach_alternative(html_content, "text/html")
            
            # Send email with error handling
            try:
                msg.send()
                return True
            except Exception as smtp_error:
                # Try with different SSL settings if initial send fails
                print(f"SMTP Error: {smtp_error}")
                
                # Fallback: try with basic send_mail
                from django.core.mail import send_mail
                send_mail(
                    subject=subject,
                    message=text_content,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'CyMate <PayifyPayments@gmail.com>'),
                    recipient_list=[email],
                    fail_silently=False,
                    html_message=html_content
                )
                return True
            
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
            return False
    
    @classmethod
    def verify_code(cls, email, code, verification_type):
        """
        Verify the provided code for the given email and type
        
        Args:
            email (str): Email address
            code (str): Verification code to verify
            verification_type (str): Type of verification
            
        Returns:
            tuple: (success: bool, message: str, verification: EmailVerification or None)
        """
        try:
            # Find the verification record
            verification = EmailVerification.objects.filter(
                email=email,
                code=code,
                verification_type=verification_type,
                is_used=False
            ).first()
            
            if not verification:
                return False, "Invalid verification code", None
            
            if verification.is_expired():
                return False, "Verification code has expired", None
            
            # Mark as used
            verification.is_used = True
            verification.save()
            
            return True, "Verification successful", verification
            
        except Exception as e:
            return False, f"Verification failed: {str(e)}", None
    
    @classmethod
    def resend_verification_code(cls, email, verification_type, user=None):
        """
        Resend verification code for the given email and type
        
        Args:
            email (str): Email address
            verification_type (str): Type of verification
            user (User, optional): Associated user object
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create new verification code
            verification = cls.create_verification_code(email, verification_type, user)
            
            # Send email
            email_sent = cls.send_verification_email(
                email, 
                verification.code, 
                verification_type, 
                user
            )
            
            if email_sent:
                return True, "Verification code sent successfully"
            else:
                return False, "Failed to send verification email"
                
        except Exception as e:
            return False, f"Failed to resend verification code: {str(e)}"
    
    @classmethod
    def cleanup_expired_codes(cls):
        """
        Clean up expired verification codes
        This should be called periodically, e.g., via a management command or cron job
        """
        EmailVerification.cleanup_expired_codes()
    
    @classmethod
    def get_user_by_email(cls, email):
        """
        Get user by email address
        
        Args:
            email (str): Email address
            
        Returns:
            User or None: User object if found, None otherwise
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None 