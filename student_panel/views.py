from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Class, Exam, Student, StudentExamAttempted, ExamQuestion, Question, StudentExamQuestionAnswer, Answer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.class_id == None:
        _class = None
    else:
        _class = get_object_or_404(Class, pk=student.class_id.pk)
    
    if _class is None:
        total = {
            'exams': 0,
        }
    else:
        total = {
            'exams': _class.exams.count(),
        }
    return render(request, 'student_dashboard/dashboard.html', {'student': student, 'total': total})

def student_exams(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    exams = _class.exams.all()
    return render(request, 'student_exams/dashboard.html', {'student': student, 'exams': exams})

def student_exam_detail(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    exam = get_object_or_404(_class.exams, pk=exam_id)
    total_questions = ExamQuestion.objects.filter(exam=exam).count()
    attempted = True if StudentExamAttempted.objects.filter(exam=exam, student=student).exists() else False
    return render(request, 'student_exams/exam_detail.html', {'student': student, 'class': _class, 'exam': exam, 'total_questions': total_questions, 'attempted': attempted})

def student_exam_start(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    exam = get_object_or_404(Exam, pk=exam_id)  # Corrected to use pk for primary key
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    questions = [exam_question.question for exam_question in exam_questions]  # List comprehension for simplicity

    return render(request, 'student_exams/exam_start.html', {
        'student': student,
        'questions': questions,
        'exam': exam
    })


def student_exam_submit(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    exam = get_object_or_404(Exam, pk=exam_id)

    StudentExamAttempted.objects.create(student=student, exam=exam, attempted=True).save()
    
    for key, value in request.POST.items():
        if key.startswith('question_'):
            question_id = key.split('_')[1]
            question = get_object_or_404(Question, pk=question_id)
            
            answer = None
            if question.question_type == 'MCQ':
                match value:
                    case 'option1':
                        answer = Answer.objects.create(option=question.option1)
                    case 'option2':
                        answer = Answer.objects.create(option=question.option2)
                    case 'option3':
                        answer = Answer.objects.create(option=question.option3)
                    case 'option4':
                        answer = Answer.objects.create(option=question.option4)
                    case _:
                        pass
            elif question.question_type == 'TF':
                answer = Answer.objects.create(truth=(value == 'True'))
            
            StudentExamQuestionAnswer.objects.create(
                student=student,
                exam=exam,
                question=question,
                answer=answer
            ).save()
    
    return redirect('student_exams', student_id=student.pk)

def student_results(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student_exam_attempted_s = StudentExamAttempted.objects.filter(student=student, attempted=True)
    exams = [student_exam_attempted.exam for student_exam_attempted in student_exam_attempted_s]
    return render(request, 'student_results/dashboard.html', {
        'student': student,
        'exams': exams,
    })

def student_result_view(request, student_id, exam_id):
    student = get_object_or_404(Student, student_id=student_id)
    exam = get_object_or_404(Exam, exam_id=exam_id)
    all_student_exam_Q_and_A = StudentExamQuestionAnswer.objects.filter(student=student, exam=exam)
    questions = []

    total_correct, total_wrong, total_attempted = 0, 0, 0
    for student_exam_Q_and_A in all_student_exam_Q_and_A:
        qa = student_exam_Q_and_A
        q = qa.question
        a = qa.answer
        
        if q.question_type == 'MCQ':
            if q.correct_option == a.option:
                total_correct += 1
                total_attempted += 1
            else:
                if a.option != None:
                    total_attempted += 1
                    total_wrong += 1
            questions.append({
                'text': q.text,
                'correct_option': q.correct_option,
                'selected_option': a.option,
            })
        else:
            if q.expected_truth_value == a.truth:
                total_correct += 1
                total_attempted += 1
            else:
                if a.truth != None:
                    total_attempted += 1
                    total_wrong += 1
            questions.append({
                'text': q.text,
                'correct_option': q.expected_truth_value,
                'selected_option': a.truth,
            })

    percentage_score = 0 if total_attempted == 0 else (total_correct/total_attempted) * 100

    context = {
        'student': student,
        'exam': exam,
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'percentage_score': percentage_score,
        'questions': questions,
    }
    
    return render(request, 'student_results/result_detail.html', context)


@csrf_exempt
def motion_detected(request, student_id):
    if request.method == 'POST' and request.FILES.get('motion_image'):
        motion_image = request.FILES['motion_image']
        exam_id = request.POST.get('exam_id')
        file_path = os.path.join('motion', f'{student_id}', f'{exam_id}', motion_image.name)
        default_storage.save(file_path, ContentFile(motion_image.read()))
        
        print(f"Motion detected and image saved to {file_path}")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
