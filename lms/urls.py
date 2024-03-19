from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.HomePage, name="home"),
    path("courses", views.Courses, name="courses"),
    # path("upload/", views.Upload_Image, name="upload_reciept"),
    path("courseinfo/<str:pk>", views.CourseDetails, name="courseinfo"),
    path("meeting/<str:pk>", views.CourseMeeting, name="meeting"),
    path("materials/<str:pk>", views.CourseMaterials, name="materials"),
    path("activities/<str:pk>", views.CourseActivities, name="activities"),
    path("studentdetails/<str:pk>", views.StudentProfile, name="studentdetails"),
    path("chat/<str:room_name>/", views.Chat, name='chat'),

    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    # Download
    path("download/<str:document_id>", views.download, name="download"),
]