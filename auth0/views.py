from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from admin_panel.models import Class, Student, Teacher
import base64
import pathlib
import shutil
from deepface import DeepFace

def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        request.session['role'] = role
        if role == 'admin':
            return redirect('dashboard')
        if role == 'teacher':
            return redirect('login_teacher')
        if role == 'student':
            return redirect('login_student')
        
    return render(request, 'choose_role.html')

def login_teacher(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            teacher = Teacher.objects.get(name=username)
            if teacher.password == password:
                request.session['teacher_id'] = teacher.pk
                return redirect('teacher_dashboard', teacher_id=teacher.pk)
            else:
                messages.error(request, 'Invalid password.')
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher not found.')
    return render(request, 'login_teacher.html')


def login_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        class_id = request.POST.get('class_id')

        try:
            _class = Class.objects.get(unique_id=class_id)
            student = Student.objects.get(unique_id=student_id)
            if student.class_id_id != _class.pk:
                messages.error(request, 'Incorrect Class ID.')

            request.session['student_id'] = student.pk
            request.session['class_id'] = _class.pk

            if not student.face_image:
                return redirect('capture_face')
            else:
                return redirect('verify_face')

        except Student.DoesNotExist:
            messages.error(request, 'Student Doesn\'t Exist with that ID.')
        except Class.DoesNotExist:
            messages.error(request, 'Incorrect Class ID.')

    return render(request, 'login_student.html')


def capture_face(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        class_id = request.session.get('class_id')
        face_image = request.POST['face_image']
        
        try:
            image_data = base64.b64decode(face_image.split(',')[1])
            all_students = Student.objects.all()

            for existing_student in all_students:
                if existing_student.face_image:
                    path1 = byte_to_png(image_data, 'current_image')
                    path2 = byte_to_png(existing_student.face_image, f'stored_image_{existing_student.pk}')
                    
                    res = DeepFace.verify(img1_path=path1, img2_path=path2)
                    if res['verified']:
                        messages.error(request, 'Student with this face already exists.')
                        cleanup()
                        return redirect('capture_face')

            student = get_object_or_404(Student, pk=student_id, class_id=class_id)
            student.face_image = image_data
            student.save()
            messages.success(request, 'Logged in successfully.')
            cleanup()
            return redirect('student_dashboard', student_id=student_id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            cleanup()

    return render(request, 'capture_face.html')

def byte_to_png(data, name):
    try:
        captured = pathlib.Path('captured')
        if not captured.exists():
            captured.mkdir(parents=True, exist_ok=True)

        face_filename = captured.joinpath(f'{name}.png')
        face_filename_str = str(face_filename)

        with open(face_filename_str, 'wb') as f:
            f.write(data)

        return face_filename_str

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except PermissionError as p_error:
        print(f"Permission error: {p_error}")
    except OSError as os_error:
        print(f"OS error: {os_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cleanup():
    try:
        shutil.rmtree(pathlib.Path('captured'))
    except FileNotFoundError:
        pass

def verify_face(request):
    if request.method == 'POST':
        try:
            face_image = request.POST.get('face_image')
            student_id = request.session.get('student_id')
            class_id = request.session.get('class_id')

            if face_image:
                student = get_object_or_404(Student, pk=student_id, class_id_id=class_id)

                img_data = base64.b64decode(face_image.split(',')[1])
                stored_face_data = student.face_image

                path1 = byte_to_png(img_data, 'current_image')
                path2 = byte_to_png(stored_face_data, 'stored_image')

                res = DeepFace.verify(img1_path=path1, img2_path=path2)
                
                if res['verified']:
                    cleanup()
                    return redirect('student_dashboard', student_id=student_id)
                else:
                    messages.error(request, 'Warning! You do not hold this account. Register yourself first.')
                    cleanup()
            else:
                messages.error(request, 'Please capture your face image.')
                cleanup()

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            cleanup()

    return render(request, 'verify_face.html')
