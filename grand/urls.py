from django.urls import path
from .views import AuthLoginView, AuthCallbackView, home, landing_page, contact, profile, logout_view,criteria,upload_file


urlpatterns = [
    path('', landing_page),
    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('logout/', logout_view, name='logout'),
    path('criteria/', criteria, name='criteria'),
    path('profile/', profile, name='profile'),
    path('upload/<int:criteria_id>/', upload_file, name='upload_file'),

    path('auth/', AuthLoginView.as_view(), name='oauth_login'),
    path('callback/', AuthCallbackView.as_view(), name='oauth_callback'),
]
