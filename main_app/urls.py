from django.urls import path
from . import views

urlpatterns = [
  path('about/', views.about, name='about'),
  path('', views.teachers_index, name='index'),
  path('accounts/signup/', views.signup, name="signup"),
  path('teachers/<int:profile_id>/', views.profiles_detail, name='detail'), 
  path('teachers/<int:profile_id>/add_lesson/', views.add_lesson, name='add_lesson'),
  path('teachers/<int:pk>/update/', views.LessonUpdate.as_view(), name='lessons_update'),
  path('teachers/<int:pk>/delete/', views.LessonDelete.as_view(), name='lessons_delete'),
  
]
