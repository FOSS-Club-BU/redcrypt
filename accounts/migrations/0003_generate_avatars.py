from django.db import migrations
from django.conf import settings
import os
from boringavatars import avatar

def generate_migration_avatar(username):
    """Generate avatar specifically for migration"""
    svg_avatar = avatar(
        name=username,
        variant="beam",
        size=512,
        colors=["08B74F", "006D6D", "002A2A", "055D5D", "074848"],
        square=True
    )
    
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)
        
    filename = f"avatar_{username}.svg"
    filepath = os.path.join(avatar_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(svg_avatar)
        
    return f'avatars/{filename}'

def generate_avatars_for_existing_users(apps, schema_editor):
    Profile = apps.get_model('accounts', 'Profile')
    for profile in Profile.objects.all():
        avatar_path = generate_migration_avatar(profile.user.username)
        profile.avatar.name = avatar_path
        profile.save()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_update_avatar_field'),
    ]

    operations = [
        migrations.RunPython(generate_avatars_for_existing_users),
    ]
