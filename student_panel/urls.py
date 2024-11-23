from django.urls import path
from . import views

urlpatterns = [
    path('<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('<int:student_id>/exams/', views.student_exams, name='student_exams'),
    path('<int:student_id>/results/', views.student_results, name='student_results'),

    path('<int:student_id>/exams/<int:exam_id>', views.student_exam_detail, name='student_exam_detail'),
    path('<int:student_id>/exams/<int:exam_id>/start', views.student_exam_start, name='student_exam_start'),
    path('<int:student_id>/exams/<int:exam_id>/submit', views.student_exam_submit, name='student_exam_submit'),

    path('<int:student_id>/results/<int:exam_id>', views.student_result_view, name='student_result_view'),

    path('<int:student_id>/motion-detected/', views.motion_detected, name='motion_detected'),
]
