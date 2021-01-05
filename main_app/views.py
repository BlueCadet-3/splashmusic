from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Lesson
from .forms import LessonForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form_data = request.POST.copy()
    is_teacher = request.POST.get('is_teacher', False) and True
    location = request.POST.get('location')
    bio = request.POST.get('bio')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if 'is_teacher' in form_data:
      del form_data['is_teacher']
      del form_data['location']
      del form_data['bio']
    form = UserCreationForm(form_data)
    if form.is_valid():
      try:
        # This will add the user to the database
        user = form.save()
        Profile.objects.create(
          first_name=first_name, 
          last_name=last_name, 
          is_teacher=is_teacher, 
          location=location, 
          bio=bio, user=user
        )
        # This is how we log a user in via code
        login(request, user)
        return redirect('index')
      except Exception as err: 
        print(err)
        error_message = 'Invalid sign up - try again'
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  return render(request, 'registration/signup.html', {'error_message': error_message})
def profiles_detail(request, profile_id):
  teacher = Profile.objects.get(id=profile_id)
  lesson_form = LessonForm()
  return render(request, 'teachers/detail.html', {
    'teacher': teacher,
    'lesson_form': lesson_form
  })

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm

@login_required
def add_lesson(request, profile_id):
  form = LessonForm(request.POST)
  if form.is_valid():
    new_lesson = form.save(commit=False)
    new_lesson.profile_id = profile_id
    new_lesson.save()
  return redirect('detail', profile_id=profile_id)

def teachers_index(request):
  teachers = Profile.objects.all()
  return render(request, 'teachers/index.html', { 'teachers': teachers })

class LessonUpdate(LoginRequiredMixin, UpdateView):
  model = Lesson
  fields = ['date', 'time', 'instrument', 'description']

class LessonDelete(LoginRequiredMixin, DeleteView):
  model = Lesson
  success_url = '/'


