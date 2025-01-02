import os
from boringavatars import avatar
from django.core.files.base import ContentFile
from django.conf import settings

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
