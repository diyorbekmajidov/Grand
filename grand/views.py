from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .client import oAuth2Client
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.cache import cache
from .models import Student, Criteria, StudentFiles
from .forms import StudentFilesForm, StudentFileForm
import requests, os
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from django.contrib import messages
from django.contrib.auth import logout

def landing_page(request):
    return render(request, 'homepage.html')

def home(request):
    student_hemis_id = cache.get('student_hemis_id')
    if not student_hemis_id:
        return redirect('/auth/')
    student = Student.objects.get(student_id_number=student_hemis_id)
    return render(request, 'index.html', context={'student':student})


def student_settings(request):
    pass

def logout_view(request):
    cache.delete('student_hemis_id')
    cache.delete('hemis_access_token')
    logout(request)

    return redirect('/')

def criteria(request):
    if request.method == 'GET':
        student_hemis_id = cache.get('student_hemis_id')
        if not student_hemis_id:
            return redirect('/auth/')
        criterias = Criteria.objects.all()
        return render(request, 'criteria.html', {'criterias':criterias})
    return render(request, 'criteria.htmlt')

def upload_file(request, criteria_id):
    criteria = get_object_or_404(Criteria, pk=criteria_id)
    student_hemis_id = cache.get('student_hemis_id')
    if not student_hemis_id:
        return redirect('/auth/')
    student = Student.objects.get(student_id_number = student_hemis_id)
    

    if request.method == 'POST':
        form = StudentFilesForm(request.POST or None, request.FILES or None, student=student, criteria=criteria)

        if form.is_valid():
            student_file = form.save(commit=False)
            student_file.criteria = criteria
            student_file.student = student
            student_file.save()
            return redirect('/criteria/')
    else:
        form = StudentFilesForm()

    return render(request, 'upload_file.html', {'form': form, 'criteria': criteria})


def student_profile(request, student_id):
    student_hemis_id = cache.get('student_hemis_id')
    
    if not student_hemis_id:
        return redirect('/auth/')
    
    # student_id argumentini ishlating, lekin siz cache dan ham olayapsiz,
    # agar kerak bo'lsa, student_id ni tekshiring
    student = get_object_or_404(Student, student_id_number=student_id)
    
    files = StudentFiles.objects.filter(student=student)
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')

        file_obj = get_object_or_404(StudentFiles, id=file_id, student=student)

        if action == 'edit':
            form = StudentFileForm(request.POST, request.FILES, instance=file_obj)
            if form.is_valid():
                form.save()
                return redirect('profile', student_id=student.student_id_number)

        elif action == 'delete':
            file_obj.delete()
            return redirect('profile', student_id=student.student_id_number)

    return render(request, 'profile.html', {
        'student': student,
        'files': files,
        'form': StudentFileForm(),
    })


def contact(request):
    student_hemis_id = cache.get('student_hemis_id')
    if not student_hemis_id:
        return redirect('/auth/')
    return render(request, 'help-center.html')



def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        return ContentFile(response.content, name=filename)
    return None


class AuthLoginView(View):
    def get(self, request):
        client = oAuth2Client(
            client_id = settings.CLIENT_ID,
            client_secret = settings.CLIENT_SECRET,
            redirect_uri = settings.REDIRECT_URI,
            authorize_url = settings.AUTHORIZE_URL,
            token_url = settings.ACCESS_TOKEN_URL,
            resource_owner_url = settings.RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()

        return HttpResponseRedirect(authorization_url)


class AuthCallbackView(View):
    def get(self, request):

        code = request.GET.get('code')
        if code is None: return JsonResponse({'error': 'code is missing!'})

        client = oAuth2Client(
            client_id = settings.CLIENT_ID,
            client_secret = settings.CLIENT_SECRET,
            redirect_uri = settings.REDIRECT_URI,
            authorize_url = settings.AUTHORIZE_URL,
            token_url = settings.ACCESS_TOKEN_URL,
            resource_owner_url = settings.RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(code)

        full_info = {}
        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)
            full_info['details'] = user_details
            full_info['token'] = access_token
            student_gpa = user_details['data']['avg_gpa']
            
            
            if float(student_gpa)<3.50:
                messages.error(request, "Sizning GPA balingiz yetarli emas. Kamida 3.5 bo‘lishi kerak.")
                return redirect('/')
            
            cache.set('hemis_access_token', access_token, timeout=1800)
            cache.set('student_hemis_id', user_details['student_id_number'], timeout=1800)
            
            if not Student.objects.filter(student_id_number=user_details["student_id_number"]).exists():
                student = Student.objects.create(
                    student_name = user_details['name'],
                    phone_number = user_details['phone'],
                    student_id_number = user_details['student_id_number'],
                    email = user_details['email'],
                    passport_number = user_details['passport_number'],
                    birth_date = user_details['birth_date'],
                    groups = user_details.get('groups', []),
                    studentStatus = user_details['data']['studentStatus']['name'],
                    paymentForm = user_details['data']['paymentForm']['name'],
                    faculty = user_details['data']['faculty']['name'],
                    level = user_details['data']['level']['name'],
                    avg_gpa = user_details['data']['avg_gpa']
                )
                image_file = download_image_from_url(user_details['picture'])
                if image_file:
                    student.student_imeg.save(image_file.name, image_file, save=False)
                    student.save()
            return redirect('/home/')
        else:
            return JsonResponse(
                {
                    'status': False,
                    'error': 'Failed to obtain access token'
                },
                status=400
            )