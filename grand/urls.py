from django.urls import path
from .views import AuthLoginView, AuthCallbackView, faculty_list, home,supervisor_login, faculty_detail, student_files, score_file, landing_page, contact, student_profile, logout_view,criteria,upload_file


urlpatterns = [
    path('', landing_page),
    path('supervisor/login/', supervisor_login, name='supervisor-login'),
    path('faculty-fiels/', faculty_list, name="faculty_list"),
    path('faculty/<str:name>/', faculty_detail, name='faculty_detail'),
    path('student-files/<int:pk>/', student_files, name="student_files"),
    path('score-file/<int:pk>/', score_file, name='score_file'),

    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('logout/', logout_view, name='logout'),
    path('criteria/', criteria, name='criteria'),
    path('profile/<int:student_id>/', student_profile, name='profile'),
    path('upload/<int:criteria_id>/', upload_file, name='upload_file'),

    path('auth/', AuthLoginView.as_view(), name='oauth_login'),
    path('callback/', AuthCallbackView.as_view(), name='oauth_callback'),
]
