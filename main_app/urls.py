from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/signup/', views.signup, name="signup"),
  path('teachers/<int:profile_id>/', views.profiles_detail, name='detail'), 
  path('teachers/<int:profile_id>/add_lesson/', views.add_lesson, name='add_lesson'),
]
