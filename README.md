# Exam Monitoring System

## Admin Features:

1. User Management:
   - Create and manage teacher accounts, including:
     .Teacher Information: Name, mobile number, subject (or course), username, and password.
   - Upload student accounts via Excel documents, allowing bulk creation and management of student profiles with unique student IDs and class IDs.
   - Assign students to specific classes in bulk, streamlining the process of class management.
   - Manage student accounts, including resetting passwords and updating personal information.

2. Class and Course Management:
   - Create and manage classes, defining the class name and description.
   - Create and manage courses, defining the course name and description.
   - Assign multiple courses to a single class, facilitating the organization of curriculum.

3. Teacher Assignment:
   - Assign teachers to specific classes and courses. Teachers will only see the classes and courses assigned to them by the admin.

4. Exam and Performance Monitoring:
   - View detailed exam results for all classes, including aggregate performance metrics.
   - Access individual student performance data for each exam, including the number of correct and incorrect answers.
   - Generate reports on exam results and student performance, helping to identify trends and areas for improvement.

5. Face Authentication Management:
   - Oversee the face authentication registration process for students.
   - Monitor logs of face authentication attempts, including timestamps and outcomes (success or failure).
   - Ensure compliance with security and privacy standards for face data.

6. Student Performance and Exam Results:
   - Access and review comprehensive exam results and student performance data.
   - Generate performance reports to identify trends, strengths, and areas for improvement.

## Teacher Features:

1. Class and Exam Management:
   - View only the classes and courses assigned by the admin.
   - Create and schedule exams for assigned classes and courses:
     - Specify the class and course for each exam.
     - Set the exam date and duration.
   - Add questions to exams either manually or by uploading an Excel document, supporting multiple-choice and true/false question formats.

2. Real-Time Monitoring and Evaluation:
   - Monitor student activity in real-time during exams, including tracking which students are currently taking the exam and their progress.
   - Flag and review any suspicious activity, such as potential cheating.
   - Immediately view students' performance after the exam, including the number of correct and incorrect answers for each student.

3. Reporting and Feedback:
   - Provide detailed feedback on student performance, helping students understand their strengths and areas for improvement.
   - Generate and review detailed reports on class performance for each exam, identifying trends and adjusting teaching strategies accordingly.

## Student Features:

1. Authentication and Exam Participation:
   - Log in using their unique student ID and class ID.
   - Register their face during the first login for future face authentication.
   - Use face authentication for subsequent logins to verify identity securely.

2. Exam Interface and Experience:
   - Access scheduled exams through a user-friendly interface.
   - Answer questions presented one at a time, with no option to return to previous questions once answered.
   - Experience shuffled questions and answer choices, ensuring each student's exam is unique.
   - Navigate through the exam using "Next" buttons, with the "Submit" button only appearing after the last question is answered.

3. Performance Review:
   - View their own exam results, including the number of correct and incorrect answers.
   - Access detailed feedback from teachers, helping them to understand their performance.
   - Track their progress over time through a personal performance dashboard.


## Additional System Features:

1. Face Authentication:
   - Ensure secure and reliable face authentication for student logins.
   - Register face data during the first login, linking it to the student’s account for future authentication.
   - Authenticate students using their face before each exam, ensuring the correct student is taking the exam.

## Database Relations
![db](https://github.com/user-attachments/assets/07c4d471-f7fb-4f3e-9fa8-3b4947a063ad)
