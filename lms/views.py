from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def LandingPage(request):
    return render(request, "lms/landing_page.html")

@login_required(login_url="login")
def HomePage(request):
    if request.user.is_superuser:
        return redirect("admin:index")
    elif not request.user.is_student:
        return redirect("faculty")
    else:
        courses = request.user.studentdetails.section.grade_level.subjects.all()
    
    # print(courses)
    context = {"courses": courses}
    return render(request, "lms/index.html", context)

@login_required(login_url="login")
def Calendar(request):
    return render(request, "lms/student/student_calendar.html")

@login_required(login_url="login")
def Courses(request):
    # print(request.user.studentdetails.first_name)
    courses = request.user.studentdetails.section.grade_level.subjects.all()
    # print(courses)
    context = {"courses": courses}
    return render(request, "lms/student/student_course.html", context)


@login_required(login_url="login")
def CourseDetails(request, pk):
    course = Subject.objects.get(id=pk)
    section = Section.objects.get(id=request.user.studentdetails.section.id)
    materials = SubjectMeeting.objects.filter(subject=course, section=section)
    activity = SubjectActivities.objects.filter(subject=course, section=section)
    mat_count = materials.count()
    chatroom = f"{course.subject_name}{section.section_name}".replace(" ", "")
    messages = Message.objects.filter(room=chatroom)[0:]

    context = {"course": course , "materials": materials, "mat_count": mat_count, "chatroom": chatroom, "messages_count": messages.count(), "activity": activity.count()}
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
    activities = SubjectActivities.objects.filter(subject=pk, is_open=True).order_by('deadline')
    submit = SumbitActivities.objects.filter(student=request.user.studentdetails)
    if len(submit):
        is_submit = True
    else:
        is_submit = False
    context = {"activities": activities, "is_submit": is_submit}
    return render(request, "lms/student/subject_activities.html", context)

@login_required(login_url="login")
def SubmitActivities(request, pk):
    activities = SubjectActivities.objects.get(id=pk, is_open=True)
    context = {"activities": activities}
    if request.method == "POST":
        print(request.FILES["file-input"])
        try:
            file = request.FILES["file-input"]
        except MultiValueDictKeyError:
            file = None
        if file:
            submit = SumbitActivities.objects.create(student=request.user.studentdetails, activity=activities, file_activities=file)
            submit.save()
            messages.success(request, "Activities Submitted Successfully")
            return redirect("activities", pk=pk)
        else:
            messages.error(request, "Please select a file")
    return render(request, "lms/student/submit_activities.html", context)

@login_required(login_url="login")
def CourseAnnouncement(request, pk):
    section = Section.objects.get(id=request.user.studentdetails.section.id)
    subject = Subject.objects.get(id=pk)
    announcement = SubjectAnnouncement.objects.filter(subject=subject, section=section)
    context = {"announcement": announcement}
    return render(request, "lms/student/subject_announcement.html", context)

@login_required(login_url="login")
def StudentProfile(request, pk):
    profile = StudentDetails.objects.get(id=pk)
    context = {"profile": profile}
    return render(request, "lms/student/student_profile.html", context)

@login_required(login_url="login")
def EditProfile(request, pk):
    profile = StudentDetails.objects.get(id=pk)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("studentdetails", pk=pk)
    context = {"form": form, "profile": profile}
    return render(request, "lms/student/edit_profile.html", context)

@login_required(login_url="login")
def AnnouncementAll(request):
    announcement = Announcement.objects.all()
    context = {"announcement": announcement}
    return render(request, "lms/announcement_base.html", context)

@login_required(login_url="login")
def FacultyDashboard(request):
    subjects = Subject.objects.filter(faculty=request.user.facultydetails)
    subject_info = []
    for subject in subjects:
        grade_level = None
        sections = None
        
        # Retrieve the related grade level for the subject
        grade_levels = GradeLevel.objects.filter(subjects=subject).order_by('grade_level')
        for grade_level in grade_levels:
            sections = Section.objects.filter(grade_level=grade_level.id).order_by('section_name')
            for section in sections:
                subject_info.append({
                    'section': {
                        'section': section,
                        'subject': subject,
                        'grade_level': grade_level,
                        },
                })
    print(subject_info)
    context = {"subjects": sorted(subject_info, key=lambda x: x['section']['section'].section_name)}
    return render(request, "lms/prof/dashboard.html", context)


def FacultyListActivity(request, subject_id, section_id):
    activities = SubjectActivities.objects.filter(subject=subject_id, section=section_id)
    print(activities)
    context = {"activities": activities, "subject": subject_id, "section": section_id}
    return render(request, "lms/prof/list_activity.html", context)

def FacultyActivity(request, subject_id, section_id):
    subject = Subject.objects.get(id=subject_id)
    section = Section.objects.get(id=section_id)
    if request.method == "POST":
        form = FacultyActivityForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.subject = subject
            activity.section = section
            activity.save()
            messages.success(request, "Activity Created Successfully")
            return redirect("faculty")
    return render(request, "lms/prof/activity_builder.html")

def FacultyQuiz(request, subject_id, section_id):
    quiz = Quiz.objects.filter(subject=subject_id, section=section_id)
    context = {"quiz": quiz}
    return render(request, "lms/prof/quiz_builder.html", context)

def FacultyQuizOpen(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.is_open:
        quiz.is_open = False
    else:
        quiz.is_open = True
    quiz.save()
    return redirect("faculty_list_quiz",subject_id=quiz.subject.id, section_id=quiz.section.id)

def CreateQuestion(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Question Created Successfully")
            return redirect("faculty")
    return render(request, "lms/prof/create_question.html")

def UploadQuizQuestions(request):
    if request.method == "POST":
        saved = save_excel_to_quiz_questions(request.FILES['file'])
        if saved:
            messages.success(request, "Quiz Questions Uploaded Successfully")
        else:
            messages.error(request, "Error uploading Quiz Questions")
    return render(request, "lms/prof/upload_quiz_questions.html")

def CreateQuiz(request, subject_id, section_id):
    if request.method == "POST":
        topic = request.POST.get("topic")
        quiz_id = uuid.uuid4()
        form = QuizForm(request.POST)
        if form.is_valid():
            saved = save_excel_to_quiz_questions(request.FILES['file_questions'], topic, quiz_id)
            if saved:
                quiz = form.save(commit=False)
                quiz.faculty = request.user
                quiz.subject = Subject.objects.get(id=subject_id)
                quiz.section = Section.objects.get(id=section_id)
                quiz.quiz_id = quiz_id
                quiz.save()
                messages.success(request, "Quiz Questions Uploaded Successfully")
                messages.success(request, "Quiz Created Successfully")
                return redirect("faculty_list_quiz")
            else:
                messages.error(request, "Error uploading Quiz Questions")
                return redirect("create_quiz")
    return render(request, "lms/prof/create_quiz.html")

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
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect("home")
        else:
            return redirect("faculty")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            custominfo = CustomUser.objects.filter(username=user)
            if user.is_superuser:
                return redirect("admin:index")
            if len(custominfo):
                if custominfo[0].is_student:
                    userDet = StudentDetails.objects.filter(user=user)
                    profile_redirect = 'home'
                else:
                    userDet = FacultyDetails.objects.filter(user=user)
                    profile_redirect = 'faculty'
                if user is not None:
                    login(request, user)
                    return redirect(profile_redirect)
                else:
                    messages.error(request, 'Username OR password is incorrect')
            else:
                messages.error(request, 'Username OR password is incorrect')
        else:
            messages.error(request, 'Username OR password is incorrect')

        # if user is not None:
        #     login(request, user)
        #     return redirect("home")
        # else:
        #     messages.info(request, "Username or Password is incorrect")

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
    return redirect("landing")

# Download
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd

def download(request, document_id):
    document = get_object_or_404(SubjectMaterials, pk=document_id)
    response = HttpResponse(document.file_materials, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
    return response

def save_excel_to_quiz_questions(file, topic):
    try:
        # Read the excel file
        df = pd.read_excel(file)

        # Iterate over each row in the dataframe
        for index, row in df.iterrows():
            # Extract the question, options, and correct answer from the row
            question = row['Question']
            option1 = row['Option 1']
            option2 = row['Option 2']
            option3 = row['Option 3']
            option4 = row['Option 4']
            correct_answer = row['Correct Answer']
            # topic = row['Topic']
            subject = row['Subject']

            # Create a new QuizQuestion object and save it to the database
            quiz_question = QuizQuestion.objects.create(
                question=question, 
                choice1=option1, 
                choice2=option2, 
                choice3=option3, 
                choice4=option4, 
                answer=correct_answer, 
                subject=subject, 
                topic=topic
                )
            quiz_question.save()

        return True
    except Exception as e:
        print(f"Error saving excel file to QuizQuestion table: {str(e)}")
        return False