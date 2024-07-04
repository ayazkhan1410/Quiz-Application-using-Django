from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from .models import CustomUser as User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    is_popular = Quizes.objects.filter(is_popular=True).order_by('-id').distinct()[:3]
    is_challenging = Quizes.objects.filter(is_challenging=True).order_by('-id').distinct()[:3]
    games = Games.objects.all().order_by('-id')[:3]
    context = {
        'is_popular': is_popular,
        'is_challenging':is_challenging,
        'games':games
    }
    return render(request, 'index.html', context)

def about_us(request):
    return render(request, 'about-us.html')

@login_required(login_url='login')
def quizes(request):
    
    question_obj = Quizes.objects.filter(completed=False).order_by('-id').distinct()
    if request.method == "POST":
        search = request.POST.get('search')
    
        if search:
            question_obj = Quizes.objects.filter(quiz_name__icontains=search)
    try:
        paginated_quiz = Paginator(question_obj, 6)
        page = request.GET.get('page')
        questions = paginated_quiz.get_page(page)
    except PageNotAnInteger:
        questions = paginated_quiz.page(1)
    except EmptyPage:
        questions = paginated_quiz.page(paginated_quiz.num_pages)
        
    context = {
        'questions': questions
    }
    return render(request, 'quizes.html', context)

@login_required(login_url='login')
def games(request):
    games_obj = Games.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
    
        if search:
            games_obj = Games.objects.filter(game_name__icontains=search)
    try:
        paginated_games = Paginator(games_obj, 6)
        page = request.GET.get('page')
        games = paginated_games.get_page(page)
    except PageNotAnInteger:
        games = paginated_games.page(1)
    except EmptyPage:
        games = paginated_games.page(paginated_games.num_pages)
    context = {
        'games': games
    }
    return render(request, 'games.html', context)

@login_required(login_url='login')
def quizes_details(request, slug):
    question_obj = Quizes.objects.filter(slug=slug)
    
    context = {
        'question_obj': question_obj
    }
    return render(request, 'quizes-details.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        contact_obj = Contact.objects.create(
            name = name,
            email = email,
            message = message, 
            subject = subject
        )
        contact_obj.save()
        messages.info(request, 'Message sent successfully')
        return redirect('contact')
    return render(request, 'contact.html')

@login_required(login_url='login')
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quizes, id=quiz_id)
    questions = quiz.questions.all()
    total_score = 0
   
    if request.method == "POST":
        score = 0
        total = questions.count()
        
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option and int(selected_option) == question.answer:
                score += 5
        
        max_score = total * 5
        percentage = (score / max_score) * 100 if max_score != 0 else 0
    
        
        context = {
            'quiz': quiz,
            'score': score,
            'total': total,
            'percentage': percentage
        }
     
        return render(request, 'quiz_result.html', context)
    
    if 'quiz_start_time' not in request.session:
        request.session['quiz_start_time'] = timezone.now().isoformat()
    
    context = {
        'quiz': quiz,
        'questions': questions
    }
    
    return render(request, 'take_quiz.html', context)

def login_page(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        user = authenticate(email = email, password=password)
        
        if user is not None:
            login(request, user)
            if next_page:= request.POST.get('next'):
                return redirect(next_page)
            return redirect('/')
        else:
            messages.info(request, 'invalid Email and Password')
            return redirect('login')
       
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        password = request.POST.get('password')
        speical_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=']
        
        if len(password) < 8 and not any(char in speical_char for char in password):
            messages.error(request, "Password must be atleast 8 characters and must contain special characters")
            return redirect('signup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Account already exists")
            return redirect('signup')
        
        user = authenticate(email = email, password = password, first_name = name)
        if user is None:
            messages.info(request, "invalid Email and Password")
            
        user_obj = User.objects.create(
            first_name = name,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        login(request, user_obj)
        return redirect('/')
            
    return render(request, 'signup.html')

@login_required
def teacher_dashboard(request):
    if not request.user.is_staff:  
        return redirect('home')

    if request.method == 'POST':
        lecture_name = request.POST.get('lecture_name')
        description = request.POST.get('description')
        pdf = request.FILES.get('pdf')
        last_date = request.POST.get('last_date')

        if lecture_name and description and last_date:
            Lectures.objects.create(
                lecture_name=lecture_name,
                description=description,
                pdf=pdf,
                last_date=timezone.datetime.fromisoformat(last_date),
                teacher=request.user
            )
        messages.success(request, 'Lecture added successfully')
        return redirect('teacher-dashboard')

    return render(request, 'teacher-dashboard.html')

@login_required
def lms(request):
    lectures = Lectures.objects.all()                
    return render(request, 'lms.html', {'lectures': lectures})

def logout_user(request):
    logout(request)
    return redirect('/')

    