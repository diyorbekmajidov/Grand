from django.urls import path, include
from .views import home, AuthCallbackView, AuthLoginView

urlpatterns = [
    path('', home),
    path('auth/', AuthLoginView.as_view()),
    path('callback/', AuthCallbackView.as_view())
]