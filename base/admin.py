from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


# Register your models here.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phoneNumber', 'is_active', 'is_staff')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm  
    form = CustomUserChangeForm  
    model = User
    list_display = ('username', 'email', 'phoneNumber', 'role', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phoneNumber')}),  
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role Information', {'fields': ('role',)}),  
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phoneNumber', 'password1', 'password2', 'role',),  
        }),
    )


@admin.register(Genders)
class GendersAdmin(admin.ModelAdmin):
    list_display = Genders.display_fields

@admin.register(Statuses)
class StatusesAdmin(admin.ModelAdmin):
    list_display = Statuses.display_fields

@admin.register(EducationLevels)
class EducationLevelsAdmin(admin.ModelAdmin):
    list_display = EducationLevels.display_fields

@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = Teachers.display_fields

@admin.register(SchoolLevels)
class SchoolLevelsAdmin(admin.ModelAdmin):
    list_display = SchoolLevels.display_fields

@admin.register(SchoolClases)
class SchoolClasesAdmin(admin.ModelAdmin):
    list_display = SchoolClases.display_fields

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = Subjects.display_fields


@admin.register(AssignToClasses)
class AssignToClassesAdmin(admin.ModelAdmin):
    list_display = AssignToClasses.display_fields

@admin.register(WhoPosts)
class WhoPostsAdmin(admin.ModelAdmin):
    list_display = WhoPosts.display_fields


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = Questions.display_fields


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = Answers.display_fields


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = Students.display_fields

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = Books.display_fields

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = Notes.display_fields
    
@admin.register(Papers)
class PapersAdmin(admin.ModelAdmin):
    list_display = Papers.display_fields
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = Comments.display_fields
    
@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = Videos.display_fields
    
@admin.register(AskQuestion)
class AskQuestionsAdmin(admin.ModelAdmin):
    list_display = AskQuestion.display_fields
    
@admin.register(AnswerQuestion)
class AnswerQuestionsAdmin(admin.ModelAdmin):
    list_display = AnswerQuestion.display_fields
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = Notification.display_fields

@admin.register(WebImages)
class WebImagesAdmin(admin.ModelAdmin):
    list_display = WebImages.display_fields