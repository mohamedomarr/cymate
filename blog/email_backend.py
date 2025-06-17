"""
Custom email backend for handling SSL certificate issues
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class CustomSMTPEmailBackend(SMTPEmailBackend):
    """
    Custom SMTP email backend that bypasses SSL certificate verification issues
    """
    
    def open(self):
        """
        Open a connection to the email server with custom SSL context
        """
        if self.connection:
            return False
            
        connection_params = {}
        if self.use_tls or self.use_ssl:
            # Create SSL context that doesn't verify certificates
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            connection_params['context'] = context
            
        try:
            if self.use_ssl:
                import smtplib
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port, 
                    timeout=self.timeout,
                    **connection_params
                )
            else:
                self.connection = self.connection_class(
                    self.host, self.port,
                    timeout=self.timeout,
                    **connection_params
                )
                
            if self.use_tls:
                self.connection.starttls(**connection_params)
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
                
            return True
            
        except Exception as e:
            if not self.fail_silently:
                raise
            return False 