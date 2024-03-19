from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

@login_required(login_url="login")
def HomePage(request):
    return render(request, "lms/index.html")

@login_required(login_url="login")
def Courses(request):
    # print(request.user.studentdetails.first_name)
    courses = StudentSubjectCourse.objects.filter(student=request.user.studentdetails)
    # print(courses)
    context = {"courses": courses}
    return render(request, "lms/student/student_course.html", context)


@login_required(login_url="login")
def CourseDetails(request, pk):
    course = Subject.objects.get(id=pk)
    section = Section.objects.get(id=request.user.studentdetails.section.id)
    materials = SubjectMeeting.objects.filter(subject=course, section=section)
    messages = Message.objects.filter(room=f"{course.subject_name}{section.section_name}")
    mat_count = materials.count()
    chatroom = f"{course.subject_name}{section.section_name}"
    context = {"course": course , "materials": materials, "mat_count": mat_count, "chatroom": chatroom, "messages": messages.count()}
    return render(request, "lms/student/student_subject_info.html", context)

@login_required(login_url="login")
def CourseMeeting(request, pk):
    section = Section.objects.get(id=request.user.studentdetails.section.id)
    subject = Subject.objects.get(id=pk)
    meeting = SubjectMeeting.objects.filter(subject=subject, section=section)
    context = {"meeting": meeting}
    return render(request, "lms/student/subject_meeting.html", context)

@login_required(login_url="login")
def CourseMaterials(request, pk):
    section = Section.objects.get(id=request.user.studentdetails.section.id)
    subject = Subject.objects.get(id=pk)
    materials = SubjectMaterials.objects.filter(subject=subject, section=section)
    context = {"materials": materials}
    return render(request, "lms/student/subject_materials.html", context)

@login_required(login_url="login")
def CourseActivities(request, pk):
    return render(request, "lms/student/subject_activities.html")

@login_required(login_url="login")
def StudentProfile(request, pk):
    return render(request, "lms/student/student_profile.html")

@login_required(login_url='login')
def Chat(request, room_name):
    # print(room_name)
    username = request.user
    messages = Message.objects.filter(room=room_name)[0:]
    return render(
        request,
        'lms/student/student_chat.html',
        {
            'room_name': room_name,
            'username': username,
            'messages': messages,
        },
    )

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, "lms/login.html")

def Register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")

    context = {"form": form}
    return render(request, "lms/register.html", context)

def Logout(request):
    logout(request)
    return redirect("login")

# Download
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def download(request, document_id):
    document = get_object_or_404(SubjectMaterials, pk=document_id)
    response = HttpResponse(document.file_materials, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
    return response