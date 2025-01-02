from django import forms
from allauth.account.forms import SignupForm, ResetPasswordForm, LoginForm
from accounts.models import Profile
from hcaptcha.fields import hCaptchaField
from datetime import datetime
import pytz


class MyCustomSignupForm(SignupForm):
    name = forms.CharField(required=False, label="Name [Optional]")
    organization = forms.CharField(required=False, label='School/Organization [Optional]')
    hcaptcha = hCaptchaField(theme='dark')
    print("here")
    print(hcaptcha)


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

        # Add your own processing here.

        # You must return the original result.
        return user




class CustomForgetPassword(ResetPasswordForm):
    hcaptcha = hCaptchaField(theme='dark')


class ContactForm(forms.Form):
    subject = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'text-green-600 p-2'}))
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'text-green-600 p-2'}))
    hCaptcha = hCaptchaField(theme='dark')
