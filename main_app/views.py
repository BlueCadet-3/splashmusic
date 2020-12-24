from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


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
    if 'is_teacher' in form_data:
      del form_data['is_teacher']
    del form_data['location']
    del form_data['bio']
    form = UserCreationForm(form_data)
    if form.is_valid():
      try:
        # This will add the user to the database
        user = form.save()
        Profile.objects.create(is_teacher=is_teacher, location=location, bio=bio, user=user)
        # This is how we log a user in via code
        login(request, user)
        return redirect('home')
      except Exception as err: 
        print(err)
        error_message = 'Invalid sign up - try again'
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  return render(request, 'registration/signup.html', {'error_message': error_message})