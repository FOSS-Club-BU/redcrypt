import os
from boringavatars import avatar
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

def generate_avatar(username):
    """Generate a beam-style avatar for the given username"""
    # Create beam-style SVG avatar
    svg_avatar = avatar(
        name=username,
        variant="beam",  # Use beam variant
        size=512,
        colors=["08B74F", "006D6D", "002A2A", "055D5D", "074848"],
        square=True
    )
    
    # Create avatars directory if it doesn't exist
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)
        
    # Generate filename
    filename = f"avatar_{username}.svg"
    filepath = os.path.join(avatar_dir, filename)
    
    # Save the avatar
    with open(filepath, 'w') as f:
        f.write(svg_avatar)
        
    return f'avatars/{filename}'

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
