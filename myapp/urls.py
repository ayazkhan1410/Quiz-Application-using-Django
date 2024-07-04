from django.urls import path, include
from myapp import views

urlpatterns = [
    
   
    path('', views.index, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('quizes/', views.quizes, name='quizes'),
    path('quizes-details/<str:slug>/', views.quizes_details, name='quizes-details'),
   
    path('contact/', views.contact, name='contact'),
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    
    path('login', views.login_page, name='login'),
    path('signup', views.signup, name='signup'),
    
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('lms/', views.lms, name='lms'),
    path('games', views.games, name='games'),
    
    path('logout', views.logout_user, name='logout'),

]
