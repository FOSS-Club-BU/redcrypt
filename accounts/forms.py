from django import forms
from allauth.account.forms import SignupForm, ResetPasswordForm, LoginForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from accounts.models import Profile
from hcaptcha.fields import hCaptchaField
from datetime import datetime
from allauth.socialaccount.adapter import get_adapter

import pytz


class MyCustomSocialSignupForm(SocialSignupForm):
    name = forms.CharField(required=False, label="Name [Optional]")
    organization = forms.CharField(required=False, label='College/Organization [Optional]')
    email = forms.EmailField(required=False) 

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        self.custom_signup(request, user)
        try:
            avatar_url = self.sociallogin.account.get_avatar_url()
        except:
            avatar_url = f"https://api.dicebear.com/9.x/fun-emoji/svg?seed={user.username}&backgroundColor=059ff2,71cf62,d84be5,d9915b,f6d594,fcbc34,b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf&backgroundRotation[]"
        
        current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        profile = Profile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            organization=self.cleaned_data['organization'],
            avatar=avatar_url,
            last_completed_time=current_time,
            last_activity=current_time)
        profile.save()
        return user

    def validate_unique_email(self, value):
        try:
            return super(MyCustomSocialSignupForm, self).validate_unique_email(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                get_adapter().error_messages["email_taken"]
                % self.sociallogin.account.get_provider().name
            )

class MyCustomSignupForm(SignupForm):
    name = forms.CharField(required=False, label="Name [Optional]")
    organization = forms.CharField(required=False, label='College/Organization [Optional]')
    hcaptcha = hCaptchaField(theme='dark')

    field_order = [
        'name', 'organization', 'username', 'email', 'password1', 'password2',
        'hcaptcha'
    ]

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)

        profile = Profile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            organization=self.cleaned_data['organization'],
            avatar=f"https://api.dicebear.com/9.x/fun-emoji/svg?seed={user.username}&backgroundColor=059ff2,71cf62,d84be5,d9915b,f6d594,fcbc34,b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf&backgroundRotation[]",
            last_completed_time=datetime.now(pytz.timezone('Asia/Kolkata')))
        profile.save()
        return user




class CustomForgetPassword(ResetPasswordForm):
    hcaptcha = hCaptchaField(theme='dark')


class ContactForm(forms.Form):
    subject = forms.CharField(
        required=True,
        max_length=150,
        label="Subject",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter subject',
        })
    )
    body = forms.CharField(
        required=True,
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Type your message here...',
            'rows': 4,
        })
    )
    hCaptcha = hCaptchaField(theme='dark')
