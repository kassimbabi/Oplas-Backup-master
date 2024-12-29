from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
# from ckeditor.fields import RichTextField//

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('teacher', 'teacher'),
        ('student', 'student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    display_fields = ['username', 'email', 'phoneNumber', 'role', 'is_active']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Genders(models.Model):
    GenderName = models.CharField(max_length=100, verbose_name='Gender Name')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['GenderName','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.GenderName
    
    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'

class WebImages(models.Model):
    ImageTitle = models.CharField(max_length=100, verbose_name='Image Title')
    Image = models.ImageField(upload_to="web-images", verbose_name='Upload Image')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['ImageTitle','Image','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.ImageTitle
    
    class Meta:
        verbose_name = 'Web Image'
        verbose_name_plural = 'Web Images'

class Statuses(models.Model):
    StatusName = models.CharField(max_length=100, verbose_name='Status Name')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['StatusName','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.StatusName
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

class EducationLevels(models.Model):
    LevelName = models.CharField(max_length=100, verbose_name='Level Name')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['LevelName','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.LevelName
    
    class Meta:
        verbose_name = 'Education Level'
        verbose_name_plural = 'Education Levels'

class Teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', verbose_name='User')
    firstName = models.CharField(max_length=100, default='John', verbose_name='First Name')
    middleName = models.CharField(max_length=100, default='Michael', verbose_name='Middle Name')
    lastName = models.CharField(max_length=100, default='Doe', verbose_name='Last Name')
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE, verbose_name='Gender', default=1)  # Assuming ID 1 exists
    dob = models.DateField(verbose_name='Date of Birth', default=date(1990, 1, 1))
    educationLevel = models.ForeignKey(EducationLevels, on_delete=models.CASCADE, verbose_name='Education Level', default=1)  # Assuming ID 1 exists
    address = models.CharField(max_length=100, default='123 Main St, Anytown', verbose_name='Address')
    phoneNumber = models.CharField(max_length=100, default='+1234567890', verbose_name='Phone Number')
    emailAddress = models.CharField(max_length=100, default='john.doe@example.com', verbose_name='Email Address')
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, verbose_name='Status')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['firstName','middleName','lastName', 'gender','dob','educationLevel','address','phoneNumber','createdDate','modifiedDate']

    def __str__(self):
        return f"{self.firstName} {self.middleName} {self.lastName}"
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers' 

class SchoolLevels(models.Model):
    LevelName = models.CharField(max_length=100, verbose_name='Level Name')
    level_order = models.IntegerField(unique=True, verbose_name='Level Order')  # Add this field
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['LevelName','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.LevelName
    
    class Meta:
        verbose_name = 'School Level'
        verbose_name_plural = 'School Levels'

class SchoolClases(models.Model):
    ClassName = models.CharField(max_length=100, verbose_name='Class Name')
    SchoolLevel = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='School Level')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['ClassName','SchoolLevel','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.ClassName
    
    class Meta:
        verbose_name = 'School Class'
        verbose_name_plural = 'School Clases'


class Subjects(models.Model):
    SubjectName = models.CharField(max_length=100, verbose_name='Subject Name')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['SubjectName', 'CreatedDate','ModifiedDate']

    def __str__(self):
        return self.SubjectName
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class AssignToClasses(models.Model):
    Teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name='Teacher Name')
    School = models.ForeignKey(SchoolClases, on_delete=models.CASCADE, verbose_name='Class Name')  # Assuming a SchoolClases model for class levels
    Subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')  # Assuming a Subjects model
    Status = models.ForeignKey(Statuses, on_delete=models.CASCADE, verbose_name='Status')  # Assuming a Statuses model for active/inactive status
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['Teacher','School','Subject','Status','CreatedDate','ModifiedDate']

    # def __str__(self):
    #     return self.Teacher
    
    class Meta:
        verbose_name = 'Assign To Class'
        verbose_name_plural = 'Assign To Classes'

class WhoPosts(models.Model):
    PostedBy = models.CharField(max_length=100, verbose_name='Posted by')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['PostedBy','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.PostedBy
    
    class Meta:
        verbose_name = 'Who Post'
        verbose_name_plural = 'Who Posts'


class Questions(models.Model):
    QuestionName = models.TextField(verbose_name='Question Name')
    QuestionBy = models.ForeignKey(WhoPosts, on_delete=models.CASCADE, verbose_name='Question By')
    LevelName = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='Level Name')
    SubjectName = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')
    IsApproved = models.BooleanField(verbose_name='Is Approved')
    ApprovedBy = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name='Approved By')
    views = models.PositiveIntegerField(default=0)
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['QuestionName','QuestionBy','LevelName','SubjectName','IsApproved','ApprovedBy','CreatedDate','ModifiedDate']

    def increment_views(self):
        self.views += 1
        self.save()
    def __str__(self):
        return self.QuestionName
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answers(models.Model):
    QuestionName = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE, verbose_name='Question Name')
    AnswerBy = models.ForeignKey(WhoPosts, on_delete=models.CASCADE, verbose_name='Answer By')
    Answer = models.TextField(verbose_name='Answer')
    IsApproved = models.BooleanField(verbose_name='Is Approved')
    ApprovedBy = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name='Approved By')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['QuestionName','Answer','IsApproved','ApprovedBy','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.Answer

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

class Students(models.Model):
    studentID = models.CharField(max_length=100, primary_key=True, verbose_name='Student ID')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', verbose_name='User')
    firstName = models.CharField(max_length=100, verbose_name='First Name')
    middleName = models.CharField(max_length=100, verbose_name='Middle Name')
    lastName = models.CharField(max_length=100, verbose_name='Last Name')
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE, verbose_name='Gender')
    dob = models.DateField(verbose_name='Date of Birth')
    schoolLevel = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='School Level')
    className = models.ForeignKey(SchoolClases, on_delete=models.CASCADE, verbose_name='School Class')
    address = models.CharField(max_length=100, verbose_name='Address')
    academicYear = models.IntegerField(verbose_name='Academic Year')
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, verbose_name='Status')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['firstName','middleName','lastName','gender','address','createdDate','modifiedDate',]

    def __str__(self):
        return f"{self.firstName} {self.middleName} {self.lastName}"
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students' 


class Books(models.Model):
    BookName = models.CharField(max_length=100, verbose_name='Book Name')
    SubjectName = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')
    LevelName = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='Level Name')
    UploadFile = models.FileField(upload_to="books", max_length=500, null=True, verbose_name='Upload File')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['BookName','SubjectName','LevelName','UploadFile','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.BookName
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books' 

class Papers(models.Model):
    PaperName = models.CharField(max_length=100, verbose_name='Paper Name')
    SubjectName = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')
    LevelName = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='Level Name')
    UploadFile = models.ImageField(upload_to="papers", max_length=500, null=True, verbose_name='Upload File')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['PaperName','SubjectName','LevelName','UploadFile','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.PaperName
    
    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'


class Notes(models.Model):
    NotesName = models.CharField(max_length=100, verbose_name='Notes Name')
    SubjectName = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')
    LevelName = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='Level Name')
    UploadFile = models.ImageField(upload_to="notes", max_length=500, null=True, verbose_name='Upload File')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['NotesName','SubjectName','LevelName','UploadFile','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.NotesName
    
    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'
        


class Comments(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='Question', related_name='comments')
    commentText = models.TextField()
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True, blank=True) 
    teacherReply = models.TextField(null=True, blank=True)
    replyDate = models.DateTimeField(null=True, blank=True)
    isApproved = models.BooleanField(default=False)  
    createdDate = models.DateTimeField(auto_now_add=True)

    display_fields = ['question', 'commentText', 'student', 'teacher', 'createdDate', 'isApproved']

    def __str__(self):
        return f"Comment by {self.student} on {self.question}"

    class Meta:
        ordering = ['-createdDate']




class Videos(models.Model):
    VideosName = models.CharField(max_length=100, verbose_name='Videos Name')
    SubjectName = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name='Subject Name')
    LevelName = models.ForeignKey(SchoolLevels, on_delete=models.CASCADE, verbose_name='Level Name')
    UploadFile = models.FileField(upload_to="Videos", max_length=500, null=True, verbose_name='Upload File')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['VideosName','SubjectName','LevelName','UploadFile','CreatedDate','ModifiedDate']
    
class AskQuestion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions", limit_choices_to={'role': 'student'})
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name="asked_questions")
    class_name = models.ForeignKey(SchoolClases, on_delete=models.CASCADE, related_name="asked_questions")
    assignment = models.ForeignKey(AssignToClasses, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    is_answered = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_fields = ['student','assignment','question_text']

    def increment_views(self):
        self.views += 1
        self.save()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Question by {self.student} for {self.assignment.Subject} in {self.assignment.School}"

    
class AnswerQuestion(models.Model):
    question_ask = models.ForeignKey(
        AskQuestion, 
        on_delete=models.CASCADE, 
        related_name="answers"
    )
    answer_text = models.TextField()
    answered_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'teacher'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_fields = ['question_ask', 'answer_text', 'answered_by']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Answer to {self.question_ask}"

# class AnswerQuestion(models.Model):
#     question_ask = models.OneToOneField(AskQuestion, on_delete=models.CASCADE, related_name="answers")
#     answer_text = models.TextField()
#     answered_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     display_fields = ['question_ask','answer_text','answered_by']
#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Answer to {self.question_ask}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    ask_question = models.ForeignKey(AskQuestion, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)  # Link to AskQuestion
    answer_question = models.ForeignKey(AnswerQuestion, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    display_fields = ['user', 'message', 'is_read', 'ask_question']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"

    @staticmethod
    def send_answer_notification(answer):
        """
        Sends a notification to the student when their question has been answered.
        """
        student = answer.question_ask.student
        question_text = answer.question_ask.question_text
        teacher_name = answer.answered_by.get_full_name() or answer.answered_by.username
        message = f"Your question '{question_text}' has been answered by {teacher_name}."
        
        # Create a notification linked to both the question and the answer
        Notification.objects.create(
            user=student,
            message=message,
            ask_question=answer.question_ask,
            answer_question=answer  # Link to the answer
        )






        
