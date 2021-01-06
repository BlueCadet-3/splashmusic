from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('teachers/', views.teachers_index, name='index'),
  path('accounts/signup/', views.signup, name="signup"),
  path('teachers/<int:profile_id>/', views.profiles_detail, name='detail'), 
  path('teachers/<int:profile_id>/add_lesson/', views.add_lesson, name='add_lesson'),
  path('teachers/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'),
  # path('teachers/<int:profile_id>/delete_photo/', views.DeletePhoto.as_view(), name='delete_photo'),
  path('teachers/<int:profile_id>/delete_photo/', views.delete_photo, name='delete_photo'),
  path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lessons_update'),
  path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lessons_delete'),
  path('teachers/<int:pk>/update/', views.TeacherUpdate.as_view(), name='teachers_update'),
]
