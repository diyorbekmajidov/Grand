from django.urls import path
from .views import AuthLoginView, AuthCallbackView, faculty_list, home,export_social_activity_excel, export_all_excel ,supervisor_login,export_social_activity_pdf, download_student_score_pdf, faculty_detail, student_files, score_file, landing_page, contact, student_profile, logout_view,criteria,upload_file


urlpatterns = [
    path('', landing_page),
    path('supervisor/login/', supervisor_login, name='supervisor-login'),
    path('faculty-fiels/', faculty_list, name="faculty_list"),
    path('faculty/<str:name>/', faculty_detail, name='faculty_detail'),
    path('student-files/<int:pk>/', student_files, name="student_files"),
    path('score-file/<int:pk>/', score_file, name='score_file'),
    path('student-file/<int:pk>/download/', download_student_score_pdf, name='download_student_score_pdf'),
    path('export/pdf/social/<int:pk>/', export_social_activity_pdf, name='export_social_pdf'),
    path('export/excel/<int:pk>/', export_social_activity_excel, name='export_excel'),
    path('export/excel/all/', export_all_excel, name="export_all_excal"),



    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('logout/', logout_view, name='logout'),
    path('criteria/', criteria, name='criteria'),
    path('profile/<int:student_id>/', student_profile, name='profile'),
    path('upload/<int:criteria_id>/', upload_file, name='upload_file'),

    path('auth/', AuthLoginView.as_view(), name='oauth_login'),
    path('callback/', AuthCallbackView.as_view(), name='oauth_callback'),
]
