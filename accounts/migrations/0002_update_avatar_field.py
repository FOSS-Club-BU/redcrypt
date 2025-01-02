from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # First remove the old avatar_url field
        migrations.RemoveField(
            model_name='profile',
            name='avatar_url',
        ),
        # Then add the new avatar field
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, upload_to='avatars/'),
        ),
    ]
