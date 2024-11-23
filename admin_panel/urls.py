from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import dashboard, students, teachers, classes, courses, results
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('students', students, name='students'),
    path('teachers', teachers, name='teachers'),
    path('classes', classes, name='classes'),
    path('courses', courses, name='courses'),
    path('results', results, name='results'),
    
    # students
    path('students/all', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/update/<int:pk>/', views.student_update, name='student_update'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/detail/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/assign2class', views.student_assign2class, name='student_assign2class'),
    
    # teachers
    path('teachers/all', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/update/<int:pk>/', views.teacher_update, name='teacher_update'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path('teachers/detail/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/assign2class', views.teacher_assign2class, name='teacher_assign2class'),
    path('teachers/select_teacher/', views.select_teacher, name='select_teacher'),
    path('teachers/select_class/<int:teacher_id>/', views.select_class, name='select_class'),
    path('teachers/assign_course/<int:teacher_id>/<int:class_id>/', views.assign_course, name='assign_course'),
    path('teachers/load_classes', views.load_classes, name='load_classes'),
    path('teachers/assignments/', views.class_course_teacher_list, name='class_course_teacher_list'),

    # classes
    path('classes/all', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/update/<int:pk>/', views.class_update, name='class_update'),
    path('classes/delete/<int:pk>/', views.class_delete, name='class_delete'),
    path('classes/detail/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/assigncourse', views.class_assigncourse, name='class_assigncourse'),

    # courses
    path('courses/all', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/update/<int:pk>/', views.course_update, name='course_update'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('courses/detail/<int:pk>/', views.course_detail, name='course_detail'),

    # results
    path('results/classes', views.admin_results_list_classes, name='admin_results_list_classes'),
    path('results/class/<int:class_id>/courses', views.admin_results_list_courses, name='admin_results_list_courses'),
    path('results/class/<int:class_id>/course/<int:course_id>/exams', views.admin_results_list_exams, name='admin_results_list_exams'),
    path('results/class/<int:class_id>/course/<int:course_id>/exam/<int:exam_id>', views.admin_results_view_exam_detail, name='admin_results_view_exam_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
