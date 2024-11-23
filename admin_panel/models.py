from django.db import models

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
    )

    text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPE_CHOICES)
    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)
    correct_option = models.CharField(max_length=200, blank=True, null=True)
    expected_truth_value = models.BooleanField(blank=True, null=True)

class Answer(models.Model):
    option = models.CharField(max_length=200, null=True)
    truth = models.BooleanField(null=True)

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)
    exams = models.ManyToManyField(Exam, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    face_image = models.BinaryField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    class_id = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    classes = models.ManyToManyField(Class, blank=True)
    
    def __str__(self):
        return self.name

class ClassCourseTeacher(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_id.name} - {self.course_id.name} - {self.teacher_id.name}"

class StudentClass(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)

class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)

class TeacherExam(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)

class ClassCourseExam(models.Model):
    _class = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)

class CourseExams(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)

class StudentExamQuestionAnswer(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)

class StudentExamAttempted(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    attempted = models.BooleanField()

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)

