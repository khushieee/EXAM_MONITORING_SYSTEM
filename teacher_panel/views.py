from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Class, Course, StudentExamAttempted, StudentExamQuestionAnswer, Teacher
from admin_panel.forms import ExamForm, QuestionForm
from admin_panel.models import Exam, ExamQuestion, Question, TeacherExam, ClassCourseTeacher, ClassCourseExam
from teacher_panel.forms import SelectExamForm
from django.contrib import messages

# Dashboard
def dashboard(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    total = {
        'exams': len(TeacherExam.objects.filter(teacher=teacher)),
    }
    return render(request, 'teacher_dashboard/dashboard.html', {'teacher': teacher, 'total': total})

def exams(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_exams/dashboard.html', {'teacher': teacher})

def questions(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_questions/dashboard.html', {'teacher': teacher})

# SECTION: EXAMS
def exam_list(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    teacher_exams = TeacherExam.objects.filter(teacher=teacher)
    exams = []
    for teacher_exam in teacher_exams:
        exams.append(teacher_exam.exam)
    return render(request, 'teacher_exams/exam_list.html', {'teacher': teacher, 'exams': exams})

def exam_detail(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'teacher_exams/exam_detail.html', {'teacher': teacher, 'exam': _exam})

def exam_create(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, teacher=teacher)
        if form.is_valid():
            _exam = form.save()
            teacher_exam = TeacherExam.objects.create(teacher=teacher, exam=_exam)
            teacher_exam.save()
            return redirect('teacher_exam_detail', teacher_id=teacher_id, pk=_exam.pk)
    else:
        form = ExamForm(teacher=teacher)
    return render(request, 'teacher_exams/exam_form.html', {'teacher': teacher, 'form': form})

def exam_update(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=_exam)
        if form.is_valid():
            form.save()
            return redirect('teacher_exam_list', teacher_id=teacher_id)
    else:
        form = ExamForm(instance=_exam)
    return render(request, 'teacher_exams/exam_form.html', {'teacher': teacher, 'form': form, 'exam': _exam})

def exam_delete(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        _exam.delete()
        return redirect('teacher_exam_list', teacher_id=teacher_id)
    return render(request, 'teacher_exams/exam_confirm_delete.html', {'teacher': teacher, 'exam': _exam})

def exam_assign2class(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        exam_id = request.POST.get('exam_id')
        exam_instance = get_object_or_404(Exam, pk=exam_id)
        class_instance = Class.objects.get(pk=class_id)
        class_instance.exams.add(exam_instance.pk)
        ClassCourseExam.objects.create(_class=class_instance, exam=exam_instance, course=exam_instance.course).save()
        return redirect('teacher_exam_list', teacher_id=teacher_id)
    
    classes = teacher.classes.all()
    exams = Exam.objects.all()
    return render(request, 'teacher_exams/exam_assign2class.html', {'teacher': teacher, 'classes': classes, 'exams': exams})

# Questions Section
def select_exam_to_list_question(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = SelectExamForm(request.POST, teacher=teacher)
        if form.is_valid():
            selected_exam = form.cleaned_data['exam']
            return redirect('teacher_question_list', teacher_id=teacher.pk, exam_id=selected_exam.pk)
    else:
        form = SelectExamForm(teacher=teacher)
    return render(request, 'teacher_questions/select_exam.html', {'form': form, 'teacher': teacher})

def question_list(request, teacher_id, exam_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    exam = Exam.objects.get(pk=exam_id)
    exam_questions = ExamQuestion.objects.filter(exam=exam_id)
    questions = [exam_question.question for exam_question in exam_questions]
    return render(request, 'teacher_questions/question_list.html', {'teacher': teacher, 'questions': questions, 'exam': exam})

def select_exam_to_create_question(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = SelectExamForm(request.POST, teacher=teacher)
        if form.is_valid():
            selected_exam = form.cleaned_data['exam']
            return redirect('teacher_question_create', teacher_id=teacher.pk, exam_id=selected_exam.pk)
    else:
        form = SelectExamForm(teacher=teacher)
    return render(request, 'teacher_questions/select_exam.html', {'form': form, 'teacher': teacher})

def question_create(request, teacher_id, exam_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    exam = get_object_or_404(Exam, exam_id=exam_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['text']
            existing_exam_question = ExamQuestion.objects.filter(exam=exam, question__text=question_text).first()
            
            if existing_exam_question:
                messages.error(request, 'A question with the same text already exists in this exam.')
            else:
                question = form.save()
                eq = ExamQuestion.objects.create(exam=exam, question=question)
                eq.save()
                return redirect('teacher_question_detail', teacher_id=teacher.pk, question_id=question.pk)
            
    else:
        form = QuestionForm()

    return render(request, 'teacher_questions/question_form.html', {'teacher': teacher, 'form': form})

def question_detail(request, teacher_id, question_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    question = Question.objects.get(pk=question_id)
    return render(request, 'teacher_questions/question_detail.html', {'teacher': teacher, 'question': question})

def question_update(request, teacher_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('teacher_question_detail', teacher_id=teacher.pk, question_id=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'teacher_questions/question_form.html', {'teacher': teacher, 'form': form, 'question': question, 'update': True})

def question_delete(request, teacher_id, question_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    question = get_object_or_404(Question, pk=question_id)

    teacher_exams = TeacherExam.objects.filter(teacher=teacher)
    exam = None

    for teacher_exam in teacher_exams:
        tmp_exam = teacher_exam.exam
        if ExamQuestion.objects.filter(exam=tmp_exam, question=question).exists():
            exam = tmp_exam
            break

    if request.method == 'POST':
        question.delete()
        return redirect('teacher_question_list', teacher_id=teacher.pk, exam_id=exam.pk)

    return render(request, 'teacher_questions/question_confirm_delete.html', {'teacher': teacher, 'question': question, 'exam': exam})

# Results
def results(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_results/dashboard.html', {
        'teacher': teacher,
    })

def results_list_courses(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    ccts = ClassCourseTeacher.objects.filter(teacher_id=teacher)
    class_course_s = []
    for cct in ccts:
        class_course_s.append({
            'class': cct.class_id,
            'course': cct.course_id,
        })
    return render(request, 'teacher_results/list_courses.html', {
        'class_course_s': class_course_s,
        'teacher': teacher,
        })

def list_course_exams(request, teacher_id, class_id, course_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    _class = get_object_or_404(Class, class_id=class_id)
    course = get_object_or_404(Course, course_id=course_id)
    class_course_exams = ClassCourseExam.objects.filter(_class=_class, course=course)
    exams = [class_course_exam.exam for class_course_exam in class_course_exams]
    return render(request, 'teacher_results/list_course_exams.html', {
        'teacher': teacher,
        'course': course,
        'exams': exams,
    })

def course_exam_result(request, teacher_id, exam_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    exam = get_object_or_404(Exam, pk=exam_id)
    seas = StudentExamAttempted.objects.filter(exam=exam, attempted=True)
    total_students = seas.count()
    student_ids = [sea.student for sea in seas]
    students = []
    for student in student_ids:
        total_correct, total_wrong, total_attempted = 0, 0, 0
        all_student_exam_Q_and_A = StudentExamQuestionAnswer.objects.filter(student=student, exam=exam)
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
            else:
                if q.expected_truth_value == a.truth:
                    total_correct += 1
                    total_attempted += 1
                else:
                    if a.truth != None:
                        total_attempted += 1
                        total_wrong += 1
        students.append({
            'student': student,
            'total_correct_answers': total_correct,
            'total_wrong_answers': total_wrong,
            'total_attempted': total_attempted,
            'percentage_score': 0 if total_attempted == 0 else (total_correct/total_attempted) * 100
        })

    return render(request, 'teacher_results/course_exam_result.html', {
        'teacher': teacher,
        'students': students,
        'total_students': total_students,
    })