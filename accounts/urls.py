from django.urls import path
from . import views

urlpatterns = [
    path('check-email/', views.check_email, name='check_email'),
    path('check-username/', views.check_username, name='check_username'),
]
