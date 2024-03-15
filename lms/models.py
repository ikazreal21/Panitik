from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models



class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False, verbose_name='Student')

class Section(models.Model):
    section_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.section_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50, null=True, blank=True)
    schedule = models.CharField(max_length=50, null=True, blank=True)
    faculty = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subject_name
    
class SubjectMeeting(models.Model):
    START_END = (
        ("1", "6:00AM"),
        ("2", "7:00AM"),
        ("3", "8:00AM"),
        ("4", "9:00AM"),
        ("5", "10:00AM"),
        ("6", "11:00AM"),
        ("7", "12:00PM"),
        ("8", "1:00PM"),
        ("9", "2:00PM"),
        ("10", "3:00PM"),
        ("11", "4:00PM"),
        ("12", "5:00PM"),
    )

    MODE = (
        ("1", "Online"),
        ("2", "Face to Face"),
    )

    PLATFORM = (
        ("1", "Google Meet"),
        ("2", "Zoom"),
        ("3", "Microsoft Teams"),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    start_schedule = models.CharField(max_length=2, choices=START_END, null=True, blank=True)
    end_schedule = models.CharField(max_length=2, choices=START_END, null=True, blank=True)
    mode = models.CharField(max_length=2, choices=MODE, null=True, blank=True)
    room = models.CharField(max_length=50, null=True, blank=True)
    platform = models.CharField(max_length=2, choices=PLATFORM, null=True, blank=True)
    
    class Meta:  
        verbose_name_plural = 'Subject Meetings'

    def __str__(self):
        return f'{self.subject} - {self.section}'
    
class SubjectMaterials(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    file_materials = models.FileField(upload_to="uploads/materials", null=True, blank=True)

    
    class Meta:  
        verbose_name_plural = 'Subject Materials'

    def __str__(self):
        return f'{self.title}'

class SubjectActivities(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    file_activities = models.FileField(upload_to="uploads/activities", null=True, blank=True)


    class Meta:  
        verbose_name_plural = 'Subject Activities'

    def __str__(self):
        return f'{self.title}'

# class SubjectAttendace(models.Model):

#     pass

# Student
class StudentDetails(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    bdate = models.DateField(null=True, blank=True)
    placebirth = models.CharField(max_length=50, null=True, blank=True)
    # is_available = models.BooleanField(default=False)
    rndid = models.CharField(
        max_length=100, default=uuid.uuid4, editable=False, null=True, blank=True
    )
    profile_pic = models.ImageField(upload_to="uploads/profile_pics", null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    lrn = models.CharField(max_length=50, null=True, blank=True)

    class Meta:  
        verbose_name_plural = 'Student Details'

    def date(self):
        # locale.setlocale(locale.LC_ALL, 'en-US')
        return self.bdate.strftime("%B %d, %Y")
        
    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class StudentSubjectCourse(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:  
        verbose_name_plural = 'Student Subject Course'

    def __str__(self):
        return f'{self.student} - {self.subject}'



class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_added",)