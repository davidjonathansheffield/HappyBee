from django.urls import path
from rest_framework.authtoken import views

from hb_app.views import *

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('happiness/submit/', SubmitHappinessAPIView.as_view()),
]
