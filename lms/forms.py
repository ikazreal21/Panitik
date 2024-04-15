from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ValidationError
from .models import *

class DateInput(forms.DateInput):
    input_type = "date"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ActivityForm(ModelForm):
    class Meta:
        model = SumbitActivities
        fields = '__all__'

class AnnouncementForm(ModelForm):
    class Meta:
        model = SubjectAnnouncement
        fields = '__all__'

class MaterialForm(ModelForm):
    class Meta:
        model = SubjectMaterials
        fields = '__all__'

class MeetingForm(ModelForm):
    class Meta:
        model = SubjectMeeting
        fields = '__all__'

class ProfileForm(ModelForm):
    class Meta:
        model = StudentDetails
        fields = ["first_name", "middle_name", "last_name", "gender", "address", "email", "profile_pic"]

    widgets = {"bdate": DateInput()}

class FacultyActivityForm(ModelForm):
    class Meta:
        model = SubjectActivities
        fields = '__all__'

class QuizForm(ModelForm):
    class Meta:
        model = QuizQuestion
        fields = '__all__'