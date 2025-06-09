from django.urls import path
from .views import AuthLoginView, AuthCallbackView, home, landing_page, contact, logout_view


urlpatterns = [
    path('', landing_page),
    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('logout/', logout_view, name='logout'),

    path('auth/', AuthLoginView.as_view(), name='oauth_login'),
    path('callback/', AuthCallbackView.as_view(), name='oauth_callback'),
]
