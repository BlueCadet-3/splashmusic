from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Lesson, Photo
from .forms import LessonForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'splash-music'

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
        # Teachers index is showing students index
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
  # We need to make student detail
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

def add_photo(request, profile_id):
  # photo-file will be the "name" attribute on the <input type="file"> used to upload the file
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for s3 / but keep the images extension
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something went wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      Photo.objects.create(url=url, profile_id=profile_id)
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', profile_id=profile_id)

def delete_photo(request, profile_id):
  Photo.objects.get(profile_id=profile_id).delete()
  return redirect('detail', profile_id=profile_id)

def teachers_index(request):
  teachers = Profile.objects.all()
  return render(request, 'teachers/index.html', { 'teachers': teachers })

class LessonUpdate(LoginRequiredMixin, UpdateView):
  model = Lesson
  fields = ['date', 'time', 'instrument', 'description', 'video']

class LessonDelete(LoginRequiredMixin, DeleteView):
  model = Lesson

  # def get_redirect_url(self):
  #   return f"/teachers/{self.user.id}"
  
  success_url = '/teachers'

class TeacherUpdate(LoginRequiredMixin,UpdateView):
  model = Profile
  fields = ['first_name', 'last_name', 'location', 'bio']
