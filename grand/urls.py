from django.urls import path
from .views import AuthLoginView, AuthCallbackView, home, landing_page


urlpatterns = [
    path('', landing_page),
    path('home/', home, name='home'),

    path('auth/', AuthLoginView.as_view(), name='oauth_login'),
    path('callback/', AuthCallbackView.as_view(), name='oauth_callback'),
]
