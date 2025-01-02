from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        required_settings = [
            'EMAIL_HOST',
            'EMAIL_PORT',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'EMAIL_SENDER'
        ]
        
        smtp_configured = all(hasattr(settings, setting) and getattr(settings, setting) 
                            for setting in required_settings)

        if not smtp_configured:
            logger.warning(
                "SMTP credentials not configured. Skipping email send. "
                "Please configure EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, and EMAIL_SENDER"
            )
            return

        try:
            from_email = f"Re-Dcrypt <{settings.EMAIL_SENDER}>"
            
            # Remove duplication prior to building final paths
            if template_prefix.startswith('account/email/'):
                template_prefix = template_prefix.replace('account/email/', '')

            html_template = f"account/email/{template_prefix}_message.html"
            text_template = f"account/email/{template_prefix}_message.txt"
            
            try:
                context['activate_url'] = context.get('activate_url', '')
                context['current_site'] = context.get('current_site', '')
                html_body = render_to_string(html_template, context)
                text_body = render_to_string(text_template, context)
            except Exception as e:
                logger.warning(f"Template rendering failed: {str(e)}")
                # Fallback to basic text email
                text_body = (
                    f"Welcome to Re-Dcrypt!\n\n"
                    f"Please verify your email by clicking this link: {context.get('activate_url', '')}\n\n"
                    f"If you did not request this email, please ignore it."
                )
                html_body = text_body.replace('\n', '<br>')
            
            # Create email message
            msg = EmailMultiAlternatives(
                subject=f"Re-Dcrypt - {context.get('subject', 'Verify your email')}",
                body=text_body,
                from_email=from_email,
                to=[email],
                headers={'From': from_email}
            )
            
            if html_body:
                msg.attach_alternative(html_body, "text/html")
            
            msg.send()
            logger.info(f"Successfully sent verification email to {email}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            logger.exception(e)
