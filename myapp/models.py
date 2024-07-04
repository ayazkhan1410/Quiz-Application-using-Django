from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .helpers import Manager
class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    user_profile = models.ImageField(upload_to='user_profile/', default='user_profile/default.webp')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = Manager()

    def __str__(self) -> str:
        return self.email

class Quizes(models.Model):
    quiz_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='questions/', default='questions/default.webp')
    objectives = models.TextField()
    eligibility = models.TextField()
    total_score = models.IntegerField(default=0)
    obtained_score = models.IntegerField(default=0)
    is_popular = models.BooleanField(default=False)
    is_challenging = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    end_time = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.quiz_name)[:100]  # Ensure slug is within max_length
        super(Quizes, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.quiz_name

class Questions(models.Model):
    quiz_name = models.ForeignKey(Quizes, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option1 = models.CharField(max_length=100, null=True, blank=True)
    option2 = models.CharField(max_length=100, null=True, blank=True)
    option3 = models.CharField(max_length=100, null=True, blank=True)
    option4 = models.CharField(max_length=100, null=True, blank=True)
    answer = models.IntegerField()
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.quiz_name.quiz_name}-{self.question}")[:100]  # Ensure slug is within max_length
        super(Questions, self).save(*args, **kwargs)
          
    def __str__(self) -> str:
        return self.question

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    
    def __str__(self) -> str:
        return self.name

class Games(models.Model):
    
    game_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='game/', default='questions/default.webp')
    url =  models.URLField(max_length=500, blank=True, null=True, help_text="Enter your Game website URL")
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.game_name
    
class Lectures(models.Model):
    
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lectures')
    lecture_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
    last_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.lecture_name or "Unnamed Lecture"