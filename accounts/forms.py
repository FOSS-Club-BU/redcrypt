from django import forms
from allauth.account.forms import SignupForm, ResetPasswordForm
from accounts.models import Profile
from hcaptcha.fields import hCaptchaField
from datetime import datetime
import pytz
from accounts.utils import generate_avatar


class MyCustomSignupForm(SignupForm):
    name = forms.CharField(required=False, label="Name [Optional]")
    organization = forms.CharField(required=False,
                                   label='School/Organization [Optional]')
    hcaptcha = hCaptchaField(theme='dark')

    field_order = [
        'name', 'organization', 'username', 'email', 'password1', 'password2',
        'hcaptcha'
    ]

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        profile = Profile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            organization=self.cleaned_data['organization'],
            last_completed_time=datetime.now(pytz.timezone('Asia/Kolkata')))
        profile.save()  # This will trigger the avatar generation in the model's save method

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
