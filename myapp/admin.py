from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'user_profile')
    search_fields = ('email', 'first_name', 'last_name', 'phone',)
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    ordering = ('email',)
    filter_horizontal = ()
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'user_profile', 'password1', 'password2'),
        }),
    )

@admin.register(Quizes)
class AdminQuiz(admin.ModelAdmin):
    list_display = ('quiz_name', 'image', 'objectives', 'eligibility', 'start_time', 'completed', 'end_time', 'total_score', 'obtained_score', 'slug', 'is_popular', 'is_challenging')
    list_per_page = 30
    search_fields = ['quiz_name', 'objectives', 'eligibility', 'slug']
    
@admin.register(Questions)
class AdminQuestions(admin.ModelAdmin):
    list_display = ('quiz_name', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'slug', )
    list_per_page = 30
    search_fields = ('quiz_name', 'question', 'option1', 'option2', 'option3', 'option4', 'slug')
    
@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_per_page = 30
    search_fields = ('name', 'email', 'subject', 'message')
    
@admin.register(Games)
class AdminGames(admin.ModelAdmin):
    list_display = ('game_name', 'image', 'url', 'description' )
    list_per_page = 30
    search_fields = ['game_name']

@admin.register(Lectures)
class AdminLectures(admin.ModelAdmin):
    list_display = ('teacher', 'lecture_name', 'description', 'pdf', 'last_date', )
    list_per_page = 30
    search_fields = ['teacher', 'lecture_name']
    