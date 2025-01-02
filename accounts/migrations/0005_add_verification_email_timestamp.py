from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_merge"),  # Replace with actual previous migration name
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_verification_email_sent",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="verification_emails_sent",
            field=models.IntegerField(default=0),
        ),
    ]
