# yourapp/urls.py
from django.urls import path
from .views import OAuthAuthorizationView, OAuthCallbackView

urlpatterns = [
    path('login/', OAuthAuthorizationView.as_view(), name='login'),
    path('callback/', OAuthCallbackView.as_view(), name='callback'),
]
