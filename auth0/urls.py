from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('login_teacher', views.login_teacher, name='login_teacher'),
    path('login_student', views.login_student, name='login_student'),
    path('capture_face', views.capture_face, name='capture_face'),
    path('verify_face', views.verify_face, name='verify_face'),
]
