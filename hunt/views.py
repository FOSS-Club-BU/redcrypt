import threading
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from hunt.decorators import hunt_status, not_banned
from hunt.models import AdditionalHint, Question
from hunt.models import LevelTracking, AnswerAttempt, SampleQuestion
from accounts.models import Profile
from hunt.utils import match_answer, get_rank, update_rank_all
# from sentry_sdk import capture_exception
import os
import requests
from datetime import datetime
import pytz

# Create your views here.


def index(request):
    return render(request, 'homepage.html')


def offline(request):
    return render(request, 'offline.html')


def guidelines(request):
    return render(request, 'guidelines.html', {'url_name': 'guidelines'})


@hunt_status
@login_required
@not_banned
def play(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.current_level == Question.objects.count():
        return render(request, 'complete.html')
    else:
        question = Question.objects.get(level=profile.current_level)
        additionalhints = AdditionalHint.objects.filter(question=question)
        return render(request, 'play.html', {
            'question': question,
            'additionalhints': additionalhints,
            'url_name': 'play'})


@hunt_status
@login_required
def check_ans(request):
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        question = Question.objects.get(level=profile.current_level)
        answer = request.POST['answer']
        try:
            AnswerAttempt.objects.create(
                user=request.user,
                level=profile.current_level,
                answer=answer)
        except Exception as e:
            # capture_exception(e)
            print(e)
        try:
            profile.stats[str(question.level)] += 1
        except KeyError:
            profile.stats[str(question.level)] = 1
        except Exception as e:
            # capture_exception(e)
            print(e)
        if match_answer(question.answer, answer):
            profile.current_level += 1
            profile.score += question.points
            profile.last_completed_time = datetime.now(pytz.timezone('Asia/Kolkata'))
            profile.save()
            try:
                LevelTracking.objects.create(
                    user=request.user,
                    level=profile.current_level)
            except Exception as e:
                # capture_exception(e)
                print(e)
            # url = f"{os.getenv('BOT_HOST')}/level/complete/{profile.discord_id}/{int(profile.current_level)-1}"
            # headers = {"Authorization": os.getenv("API_Authorization")}
            # request = requests.post(url, headers=headers)
            return JsonResponse({'correct': True}, status=200)
        else:
            profile.save()
            return JsonResponse({'correct': False}, status=200)


def leaderboard(request):
    staff = Profile.objects.filter(
        user__is_staff=True).order_by(
            '-score',
            'last_completed_time')
    profiles = Profile.objects.all().exclude(
        is_banned=True).exclude(
            user__is_staff=True).order_by(
                '-score',
                'last_completed_time')
    banned = Profile.objects.filter(
        is_banned=True).order_by(
            'last_completed_time')
    if request.user.is_authenticated:
        rank = get_rank(request.user)
    else:
        rank = 'unauthorised'
    return render(request, 'leaderboard.html', {
        'staff': staff,
        'players': profiles,
        'rank': rank,
        'banned': banned,
        'url_name': 'leaderboard'})


def faqs(request):
    return render(request, 'faqs.html', {'url_name': 'faqs'})


def rules(request):
    return render(request, 'rules.html', {'url_name': 'rules'})


def about(request):
    return render(request, 'about.html', {'url_name': 'about'})


def terms_and_conditions(request):
    return render(request, 'terms-and-conditions.html', {'url_name': 'terms_and_conditions'})


def privacy_policy(request):
    return render(request, 'privacy-policy.html', {'url_name': 'privacy_policy'})


def help_center(request):
    return render(request, 'help.html')


@login_required
def update_rank(request):
    if request.user.is_superuser:
        t = threading.Thread(target=update_rank_all, args=(), kwargs={})
        t.start()
        return JsonResponse({'status': "Updating"}, status=200)
    else:
        return JsonResponse({'status': "Unauthenticated"}, status=403)