"""redcrypt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hunt.views import index, offline, play, check_ans, leaderboard, rules
from hunt.views import faqs, update_rank
from hunt.views import about, guidelines
from hunt.views import privacy_policy, terms_and_conditions, help_center
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    path("", index, name="index"),
    path("offline/", offline, name="offline"),
    path("offline", offline, name="offline"),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("honeypot/", admin.site.urls),
    path("api/", include(("apis.urls", "apis"), namespace="api")),
    path("accounts/social/connections/", accounts_views.connect, name="connect"),
    path("accounts/", include("allauth.urls")),
    path("profile/", accounts_views.profile, name="profile"),
    path("profile/edit/", accounts_views.edit_profile, name="edit_profile"),
    path("profile/edit/save_profile", accounts_views.save_profile, name="save_profile"),
    path(
        "profile/<str:username>/", accounts_views.public_profile, name="public-profile"
    ),
    path("profile/<str:username>", accounts_views.public_profile),
    path(
        "send_confirmation_email",
        accounts_views.send_confirmation_email,
        name="send_confirmation_email",
    ),
    path(
        "verification-sent", accounts_views.verification_sent, name="verification-sent"
    ),
    path("play/", play, name="play"),
    path("leaderboard/", leaderboard, name="leaderboard"),
    path("faqs/", faqs, name="faqs"),
    path("rules/", rules, name="rules"),
    path("guidelines/", guidelines, name="guidelines"),
    path("about/", about, name="about"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", terms_and_conditions, name="terms_and_conditions"),
    path("check/", check_ans, name="check_ans"),
    path("contact/", accounts_views.contact_form_view, name="contact"),
    path("update_rank/", update_rank, name="update_rank"),
    path("500/", accounts_views.e500, name="500"),
    path("check-email/", views.check_email, name="check_email"),
    path("check-username/", views.check_username, name="check_username"),
    path(
        "contact_form_submit",
        accounts_views.submit_contact_form,
        name="contact_form_submit",
    ),
    path(
        "account/verify-captcha/", accounts_views.verify_captcha, name="verify_captcha"
    ),
    path("", include(("url_shortner.urls", "url_shortner"), namespace="url_shortner")),
    path("help/", help_center, name="help"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
