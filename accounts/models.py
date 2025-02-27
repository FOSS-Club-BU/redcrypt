"Django Models"
from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
import requests
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class Profile(models.Model):
    "User model extended with more fields"
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    score = models.IntegerField(default=0)
    last_completed_time = models.DateTimeField(null=True, blank=True)
    is_public_name = models.BooleanField(default=False)
    current_level = models.IntegerField(default=0)
    discord_id = models.IntegerField(default=0)
    organization = models.CharField(max_length=150, blank=True)
    is_public_organization = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    banned_reason = models.CharField(max_length=150, blank=True)
    ip_address = models.JSONField(default=list)
    ip_address_count = models.IntegerField(default=0)
    avatar = models.URLField(default="https://api.dicebear.com/9.x/fun-emoji/svg?seed=Easton&backgroundColor=059ff2,71cf62,d84be5,d9915b,f6d594,fcbc34,b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf")
    stats = models.JSONField(default=dict, blank=True)
    rank = models.CharField(default='0', max_length=5, blank=True)
    last_verification_email_sent = models.DateTimeField(null=True, blank=True)
    verification_emails_sent = models.IntegerField(default=0)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar
        return ''

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "User Profiles"


class IPs(models.Model):
    "IP address model for catching cheaters"
    ip_address = models.CharField(max_length=150)
    users_from_ip = models.ManyToManyField(User)
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.ip_address)

    class Meta:
        verbose_name_plural = "IP addresses"


class contact_form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    body = models.TextField()


@receiver(social_account_added)
def social_account_added_(request, **kwargs):
    profile = Profile.objects.get(user=request.user)
    sa = SocialAccount.objects.get(user=request.user)
    profile.discord_id = sa.uid
    if sa.extra_data['avatar'] == None:
        pass
    else:
        profile.avatar_url = sa.get_avatar_url()
    profile.save()
    print("here")
    user = request.user
    profile = Profile.objects.get(user=user)
    base_url = os.getenv("BOT_HOST")
    url = f"{base_url}/connect/discord/{user.username}/{profile.discord_id}"
    headers = {"Authorization": os.getenv("API_Authorization")}
    try:
        requests.post(url, headers=headers)
    except:
        pass
