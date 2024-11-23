from django.urls import path
from . import views

urlpatterns = [
    path('<int:teacher_id>/', views.dashboard, name='teacher_dashboard'),
    path('<int:teacher_id>/exams', views.exams, name='teacher_exams'),
    path('<int:teacher_id>/questions', views.questions, name='teacher_questions'),
    path('<int:teacher_id>/results', views.results, name='teacher_results'),

    # exams
    path('<int:teacher_id>/exams/all', views.exam_list, name='teacher_exam_list'),
    path('<int:teacher_id>/exams/create/', views.exam_create, name='teacher_exam_create'),
    path('<int:teacher_id>/exams/update/<int:pk>/', views.exam_update, name='teacher_exam_update'),
    path('<int:teacher_id>/exams/delete/<int:pk>/', views.exam_delete, name='teacher_exam_delete'),
    path('<int:teacher_id>/exams/detail/<int:pk>/', views.exam_detail, name='teacher_exam_detail'),
    path('<int:teacher_id>/exams/assign2class', views.exam_assign2class, name='teacher_assign_exam2class'),

    # questions
    path('<int:teacher_id>/questions/select_exam_to_create_question', views.select_exam_to_create_question, name='select_exam_to_create_question'),
    path('<int:teacher_id>/questions/select_exam_to_list_question', views.select_exam_to_list_question, name='select_exam_to_list_question'),
    path('<int:teacher_id>/questions/<int:exam_id>/all', views.question_list, name='teacher_question_list'),
    path('<int:teacher_id>/questions/<int:exam_id>/create/', views.question_create, name='teacher_question_create'),
    path('<int:teacher_id>/questions/detail/<int:question_id>/', views.question_detail, name='teacher_question_detail'),
    path('<int:teacher_id>/questions/<int:question_id>/update/', views.question_update, name='teacher_question_update'),
    path('<int:teacher_id>/questions/<int:question_id>/delete/', views.question_delete, name='teacher_question_delete'),

    # results
    path('<int:teacher_id>/results/courses', views.results_list_courses, name='results_list_courses'),
    path('<int:teacher_id>/results/class/<int:class_id>/course/<int:course_id>', views.list_course_exams, name='list_course_exams'),
    path('<int:teacher_id>/results/exam/<int:exam_id>', views.course_exam_result, name='course_exam_result')
]
