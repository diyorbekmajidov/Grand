from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grand.urls')),
    re_path('media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path('^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  

handler404 = 'grand.views.error_404_view'
# handler500 = 'grand.views.error_500_view'
