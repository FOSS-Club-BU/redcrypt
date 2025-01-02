import json
import logging
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from accounts.models import Profile, contact_form
from django.contrib import messages

logger = logging.getLogger(__name__)
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from hunt.decorators import not_banned
from allauth.account.utils import send_email_confirmation
from django.core.exceptions import ObjectDoesNotExist
from hunt.utils import get_rank
# from sentry_sdk import capture_exception
from accounts.forms import ContactForm
import requests
from django.conf import settings


@login_required
@not_banned
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    k = SocialAccount.objects.filter(user=request.user)
    rank = get_rank(request.user)
    if len(k) > 0:
        connected = True
        username = f"{k[0].extra_data['username']}#{k[0].extra_data['discriminator']}"
    else:
        connected = False
        username = None
    return render(
        request,
        'profile.html',
        {
            'user': user,
            'profile': profile,
            'connected': connected,
            'discord': username,
            'rank': rank,
        })


@login_required
@not_banned
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(
        request,
        'edit_profile.html',
        {
            'user': user,
            'profile': profile,
        })


@login_required
@not_banned
def save_profile(request):
    if request.method == "POST":
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.name = request.POST['name']
            try:
                if request.POST['is_name_public'] == "on":
                    profile.is_public_name = True
                else:
                    profile.is_public_name = False
            except KeyError:
                profile.is_public_name = False
            profile.organization = request.POST['organization']
            try:
                if request.POST['is_organization_public'] == "on":
                    profile.is_public_organization = True
                else:
                    profile.is_public_organization = False
            except KeyError:
                profile.is_public_organization = False
            profile.save()
            return JsonResponse({'saved': True}, status=200)
        except Exception as e:
            # capture_exception(e)
            return JsonResponse({'saved': False}, status=400)


def public_profile(request, username):
    try:
        usern = User.objects.get(username=username)
        profile = Profile.objects.get(user=usern)
        rank = get_rank(usern)
        return render(
            request,
            'public_profile.html',
            {'usern': usern, 'profile': profile, 'rank': rank})
    except ObjectDoesNotExist:
        return render(request, '404.html', status=404)


@login_required
@not_banned
def connect(request):
    profile = Profile.objects.get(user=request.user)
    sa = SocialAccount.objects.get(user=request.user)
    profile.discord_id = sa.uid
    profile.avatar_url = sa.get_avatar_url()
    profile.save()
    return redirect('profile')


@login_required
@not_banned
def send_confirmation_email(request):
    try:
        send_email_confirmation(request, request.user, signup=False)
        messages.success(request, "Verification email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        messages.error(request, "Failed to send verification email. Please try again or contact support.")
    return redirect('verification-sent')


@login_required
def verification_sent(request):
    # Check if email is already verified
    if request.user.emailaddress_set.filter(verified=True).exists():
        messages.info(request, "Your email is already verified!")
        return redirect('profile')
    return render(request, 'verification_sent.html')


def contact_form_view(request):
    return render(request, 'contact_form.html', {'form': ContactForm},  status=200)


def submit_contact_form(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['body']
        h_captcha_response = request.POST['h-captcha-response']
        try:
            if h_captcha_response == "":
                return JsonResponse({'success': False, 'message': "Please verify that you are not a robot."}, status=400)
            else:
                form_model = contact_form.objects.create(
                    user=request.user,
                    subject=subject,
                    body=message)
                form_model.save()
                return JsonResponse({'saved': True}, status=200)
        except Exception as e:
            # capture_exception(e)
            return JsonResponse({'saved': False, 'message': str(e)}, status=400)

def check_unique(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')

        email_exists = User.objects.filter(email=email).exists()
        username_exists = User.objects.filter(username=username).exists()

        return JsonResponse({'emailExists': email_exists, 'usernameExists': username_exists})
    else:
        return HttpResponse(status=405)

def e500(request):
    return render(request, '500.html', status=500)

def verify_captcha(request):
    if request.method == "POST":
        try:
            # Get hCaptcha response token from form
            captcha_response = request.POST.get('h-captcha-response')
            
            # Verify with hCaptcha API
            data = {
                'secret': settings.HCAPTCHA_SECRET,
                'response': captcha_response
            }
            response = requests.post('https://hcaptcha.com/siteverify', data=data)
            result = response.json()
            
            return JsonResponse({
                'captchaValid': result.get('success', False)
            })
            
        except Exception as e:
            logger.error(f"Captcha verification error: {str(e)}")
            return JsonResponse({
                'captchaValid': False,
                'error': 'Verification failed'
            }, status=400)
            
    return JsonResponse({
        'captchaValid': False,
        'error': 'Invalid request method'
    }, status=405)
