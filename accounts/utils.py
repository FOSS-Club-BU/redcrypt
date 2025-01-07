from datetime import timedelta
from django.utils import timezone


def can_send_verification_email(user):
    """Check if user can send another verification email"""
    profile = user.profile
    
    # Allow 2 additional sends after signup (total 3 including signup email)
    if profile.verification_emails_sent < 3:
        return True
        
    if not profile.last_verification_email_sent:
        return True
        
    cooldown_period = timedelta(hours=3)
    time_since_last = timezone.now() - profile.last_verification_email_sent
    
    return time_since_last > cooldown_period

def get_next_available_time(user):
    """Get timestamp when user can send next verification email"""
    profile = user.profile
    if not profile.last_verification_email_sent:
        return None
        
    next_time = profile.last_verification_email_sent + timedelta(hours=3)
    return next_time
