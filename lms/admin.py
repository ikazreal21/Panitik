from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.models import Group
from admin_interface.models import Theme

class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'is_active', 'is_staff', 'is_student')
    list_display = ('username', 'id', 'email','is_active', 'is_staff', 'is_student')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_student')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})}
    }
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_student',
                ),
            },
        ),
    )


admin.site.unregister(Group)
# admin.site.unregister(Theme)
admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(SubjectMeeting)
admin.site.register(SubjectMaterials)
admin.site.register(SubjectActivities)
admin.site.register(SumbitActivities)
admin.site.register(SubjectAnnouncement)
admin.site.register(StudentDetails)
admin.site.register(Message)
# admin.site.register(StudentSubjectCourse)
admin.site.register(GradeLevel)
admin.site.register(Announcement)
admin.site.register(FacultyDetails)
# admin.site.register(QuizQuestion)
# admin.site.register(Quiz)
admin.site.register(QuizResult)

admin.site.site_header = "Panitik Admin"
admin.site.site_title = "Panitik Admin Portal"
admin.site.index_title = "Welcome to Panitik Admin Portal"

@admin.register(Quiz)
class Quiz(admin.ModelAdmin):
    readonly_fields = ["quiz_id"]


@admin.register(QuizQuestion)
class QuizQuestion(admin.ModelAdmin):
    readonly_fields = ["quiz_id"]