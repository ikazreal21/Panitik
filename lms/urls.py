from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.LandingPage, name="landing"),
    path("home", views.HomePage, name="home"),
    path("calendar", views.Calendar, name="calendar"),
    path("courses", views.Courses, name="courses"),
    # path("upload/", views.Upload_Image, name="upload_reciept"),
    path("courseinfo/<str:pk>", views.CourseDetails, name="courseinfo"),
    path("meeting/<str:pk>", views.CourseMeeting, name="meeting"),
    path("materials/<str:pk>", views.CourseMaterials, name="materials"),
    path("activities/<str:pk>", views.CourseActivities, name="activities"),
    path("submitactivities/<str:pk>", views.SubmitActivities, name="submitactivities"),
    path("studentdetails/<str:pk>", views.StudentProfile, name="studentdetails"),
    path("editprofile/<str:pk>", views.EditProfile, name="editprofile"),
    path("announcement/<str:pk>", views.CourseAnnouncement, name="announcement"),
    path("chat/<str:room_name>/", views.Chat, name='chat'),
    path("announcement_all/", views.AnnouncementAll, name="announcement-all"),

    # Faculty
    path("faculty/", views.FacultyDashboard, name="faculty"),
    path("faculty_list_activity/<str:subject_id>/<str:section_id>/", views.FacultyListActivity, name="faculty_list_activity"),
    path("faculty_activity/<str:subject_id>/<str:section_id>/", views.FacultyActivity, name="faculty_activity"),


    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    # Download
    path("download/<str:document_id>", views.download, name="download"),
]