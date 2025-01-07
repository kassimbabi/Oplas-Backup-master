from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from base.models import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import csv
from django.contrib import messages
from datetime import datetime
import logging
from django.db.models import Q
from django.urls import reverse
from .utils import assign_teacher_to_comment



        

def loginAuthentication(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            user = None
            print(f"Authentication error: {e}")  

        if user is not None:
            auth_login(request, user)

            if hasattr(user, 'role'):
                if user.role == 'admin':
                    return redirect('dashboard')
                elif user.role == 'teacher':
                    return redirect('dashboard')
                elif user.role == 'student':
                    return redirect('home')

            else:
                return redirect('home')

        else:
            context = {
                'error': 'Invalid username or password',
            }
            return render(request, 'base/home.html', context)

    return render(request, 'base/home.html') 

def logoutUser(request):
    
    auth_logout(request) 
    
    return redirect('home')

def BackendProfile(request):    
    sitename = "MY PROFILE | OPLAS TANZANIA"
    page_name = 'BackendProfile' 
    
    user = request.user
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        
        user.username = username
        user.email = email
        user.phoneNumber = phoneNumber
        user.save()
        
        messages.success(request, 'Your profile was successfully updated!') 
        return redirect('backend_profile')
        
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'profiles':user,
    }
    
    return render(request, 'base/backend-profile.html', context)

def changePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                
                update_session_auth_hash(request, user) 
                messages.success(request, 'Your password was successfully updated!')
                return redirect('backend_profile')
            else:
                messages.error(request, 'Old password is incorrect.')
        else:
            messages.error(request, 'New password and confirm password do not match.')

    return render(request, 'base/backend-profile.html')   

    
def Home(request):    
    sitename = "HOME | OPLAS TANZANIA"
    page_name = 'Home'
    
    status = request.GET.get('status', '')  

    
    selected_subject = request.GET.get('subject', '')  

    
    questions = Questions.objects.all()

  
    if status == 'answered':
        questions = questions.filter(answers__isnull=False) 
    elif status == 'unanswered':
        questions = questions.filter(answers__isnull=True) 

    
    if selected_subject:
        questions = questions.filter(SubjectName_id=selected_subject)

  
    paginator = Paginator(questions, 5)  
    page_number = request.GET.get('page')
    questions_page = paginator.get_page(page_number)

  
    subjects = Subjects.objects.all()

    context = {
        'sitename': sitename,
        'page_name': page_name,
        'questions': questions_page,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'status': status,
    }
    
    return render(request, 'base/home.html', context)

def About(request):    
    sitename = "ABOUT US | OPLAS TANZANIA"
    page_name = 'About'    
    context = {
        'sitename': sitename,
        'page_name': page_name,
    }
    
    return render(request, 'base/about-us.html', context)

def Contact(request):    
    sitename = "CONTACT US | OPLAS TANZANIA"
    page_name = 'Contact'    
    context = {
        'sitename': sitename,
        'page_name': page_name,
    }
    
    return render(request, 'base/contact-us.html', context)

def ViewAnswers(request, pk):    
    sitename = "ANSWERS | OPLAS TANZANIA"
    page_name = 'Home' 



    questions = Questions.objects.get(id = pk)

    content_type = ContentType.objects.get_for_model(Questions)

    comment_count = Comments.objects.filter(content_type=content_type, object_id=pk).count()

    comments = Comments.objects.filter(
        content_type=content_type,
        object_id=questions.id
    )
         # Set up pagination
    paginator = Paginator(comments, 5)  # Show 10 students per page
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    viewed_questions = request.session.get('viewed_questions', [])
    
    if questions.id not in viewed_questions:
        questions.increment_views() 
        viewed_questions.append(questions.id)  
        request.session['viewed_questions'] = viewed_questions 

    context = {
        'sitename': sitename,
        'page_name': page_name,
        'questions': questions,
        'comments': comments,
        'comment_count': comment_count,
    }
    
    return render(request, 'base/view-answers.html', context)

def AskedQestions(request):    
    sitename = "ASKED QUESTIONS | OPLAS TANZANIA"
    page_name = 'Home'

    try:
        if not request.user.is_authenticated:
            return redirect('home')  

        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home') 
    
    student_level_order = student.schoolLevel.level_order


    ask_questions = AskQuestion.objects.filter(
    LevelName__level_order__lte=student_level_order
)

    # Set up pagination
    paginator = Paginator(ask_questions, 5)  # Show 10 students per page
    page_number = request.GET.get('page')
    try:
        ask_questions = paginator.page(page_number)
    except PageNotAnInteger:
        ask_questions = paginator.page(1)
    except EmptyPage:
        ask_questions = paginator.page(paginator.num_pages)

    context = {
        'sitename': sitename,
        'page_name': page_name,
        'ask_questions': ask_questions,
    }
    
    return render(request, 'base/asked-questions.html', context)

def ViewAskedQestions(request, pk):    
    sitename = "ASKED QUESTIONS | OPLAS TANZANIA"
    page_name = 'Home' 

    ask_questions = AskQuestion.objects.get(id = pk)  
    
 
    content_type = ContentType.objects.get_for_model(AskQuestion)

    comment_count = Comments.objects.filter(content_type=content_type, object_id=pk).count()

    comments = Comments.objects.filter(
        content_type=content_type,
        object_id=ask_questions.id
    )

     # Set up pagination
    paginator = Paginator(comments, 5)  # Show 10 students per page
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'sitename': sitename,
        'page_name': page_name,
        'ask_questions': ask_questions,
        'comments':comments,
        'comment_count': comment_count,
     
    }
    
    return render(request, 'base/view-asked-questions.html', context)


# QUESTIONS VIEWS
@login_required(login_url='home')
def questions_class_level(request):
    sitename = "Class Levels | Oplas Tanzania"
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home')  
    
    student_level_order = student.schoolLevel.level_order

  
    levels_for_student = SchoolLevels.objects.filter(
        level_order__lte=student_level_order
    )
    
 
    context = {
        'sitename': sitename, 
        'class_levels': levels_for_student, 
        'student': student
    }
    
    return render(request, 'base/questions-class-levels.html', context)


@login_required(login_url='home')
def questions_subject_categories(request, class_level_id):
    sitename = "Subject Categories | Oplas Tanzania"
    class_level = SchoolLevels.objects.get(id=class_level_id) 
    subjects = Subjects.objects.all()
    

    
    context = {
        'sitename': sitename,
        'subjects': subjects,
        'class_level': class_level,
}
    
    return render(request, 'base/questions_subject_categories.html', context)

@login_required(login_url='home')
def questions_view(request, subject_id, class_level_id):    
    sitename = "QUESTIONS | OPLAS TANZANIA"
    page_name = 'Resources'  
    subject = Subjects.objects.get(id=subject_id)
    class_level = SchoolLevels.objects.get(id=class_level_id)
    questions = Questions.objects.filter(SubjectName=subject, LevelName=class_level)
    
    
    # Set up pagination
    paginator = Paginator(questions, 12)  
    page_number = request.GET.get('page')
    try:
        questions = paginator.page(page_number)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)


    context = {
        'sitename': sitename,
        'page_name': page_name,
        'questions': questions,
        'subject': subject,
        'class_level': class_level,
}
    
    return render(request, 'base/questions-resources.html', context)




# NOTES VIEWS
@login_required(login_url='home')
def notes_class_level(request):
    sitename = "Class Levels | Oplas Tanzania"
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home')  
    
    student_level_order = student.schoolLevel.level_order

  
    levels_for_student = SchoolLevels.objects.filter(
        level_order__lte=student_level_order
    )
    
 
    context = {
        'sitename': sitename, 
        'class_levels': levels_for_student, 
        'student': student,
        
    }
    
    return render(request, 'base/notes-class-levels.html', context)


@login_required(login_url='home')
def notes_subject_categories(request, class_level_id):
    sitename = "Subject Categories | Oplas Tanzania"
    class_level = SchoolLevels.objects.get(id=class_level_id) 
    subjects = Subjects.objects.all()  
    
    context = {
        'sitename': sitename,
        'subjects': subjects,
        'class_level': class_level,  
    }
    
    return render(request, 'base/notes_subject_categories.html', context)
@login_required(login_url='home')
def notes_view(request, subject_id, class_level_id):    
    sitename = "NOTES | OPLAS TANZANIA"
    page_name = 'Resources'    
    subject = Subjects.objects.get(id=subject_id)
    class_level = SchoolLevels.objects.get(id=class_level_id)
    notes = Notes.objects.filter(SubjectName=subject, LevelName=class_level)
    
    # Set up pagination
    paginator = Paginator(notes, 12)  
    page_number = request.GET.get('page')
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
        
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'notes': notes,
        'subject': subject, 
        'class_level': class_level,  
    }
    return render(request, 'base/notes-resources.html', context)

# PAPERS VIEWS
@login_required(login_url='home')
def papers_class_level(request):
    sitename = "Class Levels | Oplas Tanzania"
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home')  
    
    student_level_order = student.schoolLevel.level_order

  
    levels_for_student = SchoolLevels.objects.filter(
        level_order__lte=student_level_order
    )
    
 
    context = {
        'sitename': sitename, 
        'class_levels': levels_for_student, 
        'student': student
    }
    
    return render(request, 'base/papers-class-levels.html', context)


@login_required(login_url='home')
def papers_subject_categories(request, class_level_id):
    sitename = "Subject Categories | Oplas Tanzania"
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subjects = Subjects.objects.all()
    
    context = {
        'sitename': sitename,
        'subjects': subjects,
        'class_level': class_level,
}

    return render(request, 'base/papers_subject_categories.html', context)
@login_required(login_url='home')
def papers_view(request, subject_id, class_level_id):    
    sitename = "PREVIOUS PAPERS | OPLAS TANZANIA"
    page_name = 'Resources'    
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subject = Subjects.objects.get(id=subject_id)
    papers = Papers.objects.filter(SubjectName=subject, LevelName=class_level)
    
     # Set up pagination
    paginator = Paginator(papers, 12)  
    page_number = request.GET.get('page')
    try:
        papers = paginator.page(page_number)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)
    
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'papers': papers,
        'class_level': class_level,
        'subject': subject
}
    
    return render(request, 'base/papers-resources.html', context)

# BOOKS VIEWS
@login_required(login_url='home')
def books_class_level(request):
    sitename = "Class Levels | Oplas Tanzania"
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home')  
    
    student_level_order = student.schoolLevel.level_order

  
    levels_for_student = SchoolLevels.objects.filter(
        level_order__lte=student_level_order
    )
    
 
    context = {
        'sitename': sitename, 
        'class_levels': levels_for_student, 
        'student': student
    }
    
    return render(request, 'base/books-class-levels.html', context)


@login_required(login_url='home')
def books_subject_categories(request, class_level_id):
    sitename = "Subject Categories | Oplas Tanzania"
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subjects = Subjects.objects.all()
    
    context = {
        'sitename': sitename,
        'subjects': subjects,
        'class_level': class_level,
}

    return render(request, 'base/books_subject_categories.html', context)
@login_required(login_url='home')
def books_view(request, subject_id, class_level_id):    
    sitename = "BOOKS | OPLAS TANZANIA"
    page_name = 'Resources'    
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subject = Subjects.objects.get(id=subject_id)
    books = Books.objects.filter(SubjectName=subject, LevelName=class_level)
    
    # Pagination setup
 
    paginator = Paginator(books, 12) 

    page_number = request.GET.get('page', 1)  
    books_page = paginator.get_page(page_number)
    
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'books': books_page,
        'class_level': class_level,
        'subject': subject
}
    
    return render(request, 'base/books-resources.html', context)


# VIDEOS VIEWS
@login_required(login_url='home')
def videos_class_level(request):
    sitename = "Class Levels | Oplas Tanzania"
    try:
        student = Students.objects.get(user=request.user)
    except Students.DoesNotExist:
        return redirect('home')  
    
    student_level_order = student.schoolLevel.level_order

  
    levels_for_student = SchoolLevels.objects.filter(
        level_order__lte=student_level_order
    )
    
 
    context = {
        'sitename': sitename, 
        'class_levels': levels_for_student, 
        'student': student
    }
    
    return render(request, 'base/videos-class-levels.html', context)


@login_required(login_url='home')
def videos_subject_categories(request, class_level_id):
    sitename = "Subject Categories | Oplas Tanzania"
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subjects = Subjects.objects.all()
    
    context = {
        'sitename': sitename,
        'subjects': subjects,
        'class_level': class_level,
}

    return render(request, 'base/videos_subject_categories.html', context)
@login_required(login_url='home')
def videos_view(request, subject_id, class_level_id):    
    sitename = "VIDEOS | OPLAS TANZANIA"
    page_name = 'Resources'    
    class_level = SchoolLevels.objects.get(id=class_level_id)
    subject = Subjects.objects.get(id=subject_id)
    videos = Videos.objects.filter(SubjectName=subject, LevelName=class_level)
    
    # Set up pagination
    paginator = Paginator(videos, 6)  
    page_number = request.GET.get('page')
    try:
        videos = paginator.page(page_number)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'videos': videos,
        'class_level': class_level,
        'subject': subject
}
    
    return render(request, 'base/videos-resources.html', context)
@login_required(login_url='home')
def Dashboard(request):    
    sitename = "DASHBOARD | OPLAS TANZANIA"
    page_name = 'Dashboard'    
    context = {
        'sitename': sitename,
        'page_name': page_name,
    }
    
    return render(request, 'base/dashboard.html', context)

# @login_required(login_url='home')
# def manage_teachers(request):
#     # Set up context variables for rendering
#     sitename = "Teachers | OPLAS TANZANIA"
#     page_name = "Teachers"
#     icon = "fa fa-dashboard"
    
#     # Fetch all teacher-related data
#     teachers = Teachers.objects.all()
#     genders = Genders.objects.all()
#     education_levels = EducationLevels.objects.all()
#     statuses = Statuses.objects.all()

#     # Handle search query
#     query = request.GET.get('q', '')
#     if query:
#         teachers = Teachers.objects.filter(
#             Q(firstName__icontains=query) |
#             Q(middleName__icontains=query) |
#             Q(lastName__icontains=query) |
#             Q(emailAddress__icontains=query)
#         )
#     else:
#         teachers = Teachers.objects.all()

#     # Handle form submission for CSV file upload
#     if request.method == 'POST':
#         if 'csv_file' in request.FILES:
#             csv_file = request.FILES['csv_file']
#             try:
#                 # Decode and read the CSV file
#                 decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
#                 reader = csv.DictReader(decoded_file)

#                 # Initialize a list to keep track of errors
#                 errors = []

#                 # Process each row in the CSV
#                 for row in reader:
#                     try:
#                         # Fetch foreign key objects based on the CSV data
#                         gender = Genders.objects.get(pk=row['gender'])
#                         educationLevel = EducationLevels.objects.get(pk=row['educationLevel'])
#                         status = Statuses.objects.get(pk=row['status'])

#                         # Parse and validate the date in DD/MM/YYYY format
#                         try:
#                             dob = datetime.strptime(row['dob'], '%d/%m/%Y').date()
#                         except ValueError:
#                             raise ValueError(f"Invalid date format for DOB: {row['dob']}. It must be in DD/MM/YYYY format.")

#                         # Create a new user
#                         user = User.objects.create_user(
#                             username=row['emailAddress'],
#                             password=row['lastName'],  # Use a secure method to generate passwords in production
#                             email=row['emailAddress'],
#                             first_name = row['firstName'],
#                             last_name =row['lastName'],
#                             role='teacher'
#                         )

#                         # Create a new teacher record
#                         Teachers.objects.create(
#                             user=user,
#                             firstName=row['firstName'],
#                             middleName=row['middleName'],
#                             lastName=row['lastName'],
#                             gender=gender,
#                             dob=dob,
#                             educationLevel=educationLevel,
#                             address=row['address'],
#                             phoneNumber=row['phoneNumber'],
#                             emailAddress=row['emailAddress'],
#                             status=status,
#                         )

#                         # Success message for each added teacher
#                         messages.success(request, f"Teacher '{row['firstName']}' added successfully.")
#                         # return redirect('teachers')

#                     except Exception as e:
#                         # Collect error messages for each row that fails
#                         error_message = f"Error processing teacher: {row.get('firstName', 'Unknown')}. Error: {e}"
#                         errors.append(error_message)
#                         print(error_message)

#                 # If there were errors, display them to the user
#                 if errors:
#                     messages.error(request, "Some teachers could not be processed:\n" + "\n".join(errors))

#             except Exception as e:
#                 # Handle errors related to reading the CSV file
#                 print(f"Error reading the CSV file: {e}")
#                 messages.error(request, "Failed to read the CSV file. Please ensure it's formatted correctly.")
#         else:
#             # Handle the case where no CSV file was uploaded
#             messages.error(request, "No CSV file uploaded. Please try again.")
#         return redirect('teachers')
    
#     # Set up pagination
#     paginator = Paginator(teachers, 10)  # Show 10 teachers per page
#     page_number = request.GET.get('page')
#     try:
#         teachers = paginator.page(page_number)
#     except PageNotAnInteger:
#         teachers = paginator.page(1)
#     except EmptyPage:
#         teachers = paginator.page(paginator.num_pages)

#     # Prepare context for rendering the template
#     context = {
#         'sitename': sitename,
#         'page_name': page_name,
#         'icon': icon,
#         'teachers': teachers,
#         'genders': genders,
#         'education_levels': education_levels,
#         'statuses': statuses,
#         'query': query,
#     }

 
#     return render(request, 'base/teachers.html', context)


def manage_teachers(request):
    # Set up context variables for rendering
    sitename = "Teachers | OPLAS TANZANIA"
    page_name = "Teachers"
    icon = "fa fa-dashboard"

    # Fetch all teacher-related data
    teachers = Teachers.objects.all()
    genders = Genders.objects.all()
    education_levels = EducationLevels.objects.all()
    statuses = Statuses.objects.all()

    # Handle search query
    query = request.GET.get('q', '')
    if query:
        teachers = Teachers.objects.filter(
            Q(firstName__icontains=query) |
            Q(middleName__icontains=query) |
            Q(lastName__icontains=query) |
            Q(emailAddress__icontains=query)
        )

    # Set up pagination
    paginator = Paginator(teachers, 10)  # Show 10 teachers per page
    page_number = request.GET.get('page')
    try:
        teachers = paginator.page(page_number)
    except PageNotAnInteger:
        teachers = paginator.page(1)
    except EmptyPage:
        teachers = paginator.page(paginator.num_pages)

    # Prepare context for rendering the template
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'icon': icon,
        'teachers': teachers,
        'genders': genders,
        'education_levels': education_levels,
        'statuses': statuses,
        'query': query,
    }

    return render(request, 'base/teachers.html', context)


def upload_teachers(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        try:
            decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
            reader = csv.DictReader(decoded_file)

            errors = []  

            for row in reader:
                try:
                    gender = Genders.objects.get(pk=row['gender'])
                    education_level = EducationLevels.objects.get(pk=row['educationLevel'])
                    status = Statuses.objects.get(pk=row['status'])

                    
                    dob = datetime.strptime(row['dob'], '%d/%m/%Y').date()

                    user = User.objects.create_user(
                        username=row['emailAddress'],
                        password=row['lastName'],  
                        email=row['emailAddress'],
                        first_name=row['firstName'],
                        last_name=row['lastName'],
                        role='teacher'
                    )

                    Teachers.objects.create(
                        user=user,
                        firstName=row['firstName'],
                        middleName=row['middleName'],
                        lastName=row['lastName'],
                        gender=gender,
                        dob=dob,
                        educationLevel=education_level,
                        address=row['address'],
                        phoneNumber=row['phoneNumber'],
                        emailAddress=row['emailAddress'],
                        status=status,
                    )

                    messages.success(request, f"Teacher '{row['firstName']}' added successfully.")

                except Exception as e:
                    error_message = f"Error processing teacher: {row.get('firstName', 'Unknown')}. Error: {e}"
                    errors.append(error_message)

            if errors:
                messages.error(request, "Some teachers could not be processed:\n" + "\n".join(errors))

        except Exception as e:
            
            messages.error(request, f"Failed to process the CSV file: {e}")
    else:
        messages.error(request, "No valid CSV file uploaded. Please try again.")

    return redirect('teachers')  


@login_required(login_url='home')
def AddTeachers(request):    

    sitename = "TEACHERS | OPLAS TANZANIA"
    page_name = 'Teachers' 
    
    if request.method == 'POST':
        username = request.POST.get('email_address')
        password = request.POST.get('last_name')
        email = request.POST.get('email_address')

        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender_id= request.POST.get('gender')
        dob = request.POST.get('dob')
        education_level_id = request.POST.get('education_level')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email_address = request.POST.get('email_address')
        status_id = request.POST.get('status')
        


        if not username or not password or not email:
            
            return render(request, 'teachers/teachers.html', {'error': 'Please fill out all required fields'})
        
        if gender_id and education_level_id and status_id:
            
            gender = Genders.objects.get(pk=gender_id)
            education_level = EducationLevels.objects.get(pk=education_level_id)
            status = Statuses.objects.get(pk=status_id)

        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name = first_name,
            last_name = last_name,
            email=email,
            role='teacher'
        )

       
        teacher = Teachers.objects.create(
            user=user,  
            firstName=first_name,
            middleName=middle_name,
            lastName=last_name,
            gender=gender,
            dob=dob,
            educationLevel=education_level,
            address=address,
            phoneNumber=phone_number,
            emailAddress=email_address,
            status=status,
        )

        return redirect('teachers')  
       
    context = {
        'sitename': sitename,
        'page_name': page_name,
    }
    
    return render(request, 'base/teachers.html', context)

@login_required(login_url='home')
def edit_teacher(request, teacher_id):
    teacher = Teachers.objects.get(pk=teacher_id)
    user = User.objects.get(username=teacher.emailAddress) 

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        middleName = request.POST.get('middleName')
        lastName = request.POST.get('lastName')
        gender_id = request.POST.get('gender')
        dob = request.POST.get('dob')
        educationLevel_id = request.POST.get('educationLevel')
        address = request.POST.get('address')
        phoneNumber = request.POST.get('phoneNumber')
        emailAddress = request.POST.get('emailAddress')
        status_id = request.POST.get('status')
        
        gender = Genders.objects.get(pk=gender_id)
        educationLevel = EducationLevels.objects.get(pk=educationLevel_id)
        status = Statuses.objects.get(pk=status_id)

        teacher.firstName = firstName
        teacher.middleName = middleName
        teacher.lastName = lastName
        teacher.gender = gender
        teacher.dob = dob
        teacher.educationLevel = educationLevel
        teacher.address = address
        teacher.phoneNumber = phoneNumber
        teacher.emailAddress = emailAddress
        teacher.status = status
        teacher.save()

        user.username = emailAddress  
        user.email = emailAddress
        user.first_name = firstName 
        user.last_name = lastName   
        user.set_password(lastName)  
        user.save()

        messages.success(request, 'Teacher updated successfully')
        return redirect('teachers')
    else:
        context = {
            'teacher': teacher,
            'genders': Genders.objects.all(),
            'education_levels': EducationLevels.objects.all(),
            'statuses': Statuses.objects.all()
        }
        return render(request, 'base/teachers.html', context)

    
@login_required(login_url='home')    
def delete_teacher(request, teacher_id):
    
    current_page = request.GET.get('page', 1)

    book = Teachers.objects.get( id=teacher_id)
    book.delete()

    query = request.GET.get('query', '')  
    return redirect(f"{reverse('teachers')}?page={current_page}&query={query}")



# Function to handle managing  students starting here

@login_required(login_url='home')
def manage_students(request):
    sitename = "STUDENTS | OPLAS TANZANIA"
    page_name = 'Students'
    students = Students.objects.all()
    genders = Genders.objects.all()
    school_levels = SchoolLevels.objects.all()
    statuses = Statuses.objects.all()
    school_classes = SchoolClases.objects.all()
    
    # Preload all classes to filter client-side
    all_classes = list(SchoolClases.objects.values('id', 'ClassName', 'SchoolLevel_id'))
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        students = Students.objects.filter(
            Q(firstName__icontains=query) |
            Q(middleName__icontains=query) |
            Q(lastName__icontains=query) |
            Q(studentID__icontains=query)
        )
    else:
        students = Students.objects.all()
    
    # Set up pagination
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'students': students,
        'genders': genders,
        'school_levels': school_levels,
        'statuses': statuses,
        'all_classes': all_classes,
        'school_classes': school_classes,
    }
    
    return render(request, 'base/students.html', context)




@login_required(login_url='home')
def register_student(request):
    sitename = "Students | OPLAS TANZANIA"
    page_name = "Students"
    icon = "fa fa-dashboard"

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            try:
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_file)

                errors = []

                for row in reader:
                    try:
                        gender = Genders.objects.get(pk=row['gender'])
                        schoolLevel = SchoolLevels.objects.get(pk=row['schoolLevel'])
                        className = SchoolClases.objects.get(pk=row['className'])  
                        status = Statuses.objects.get(pk=row['status'])

                        try:
                            dob = datetime.strptime(row['dob'], '%d/%m/%Y').date()
                        except ValueError:
                            raise ValueError(f"Invalid date format for DOB: {row['dob']}. It must be in DD/MM/YYYY format.")


                        user = User.objects.create_user(
                            username=row['studentID'],
                            password=row['lastName'], 
                            first_name=row['firstName'],
                            last_name=row['lastName'],
                            role='student',
                        )

                        Students.objects.create(
                            user=user,
                            studentID=row['studentID'],
                            firstName=row['firstName'],
                            middleName=row['middleName'],
                            lastName=row['lastName'],
                            gender=gender,
                            dob=dob,
                            schoolLevel=schoolLevel,
                            className=className,  
                            address=row['address'],
                            academicYear=row['academicYear'],
                            status=status,
                        )

                        messages.success(request, f"Student '{row['firstName']}' added successfully.")

                    except Exception as e:
                        error_message = f"Error processing student: {row.get('firstName', 'Unknown')}. Error: {e}"
                        errors.append(error_message)
                        print(error_message)

                if errors:
                    messages.error(request, "Some students could not be processed:\n" + "\n".join(errors))

                return redirect('students')

            except Exception as e:
                print(f"Error reading the CSV file: {e}")
                messages.error(request, "Failed to read the CSV file. Please ensure it's formatted correctly.")
        else:
            studentID = request.POST.get('studentID')
            firstName = request.POST.get('firstName')
            middleName = request.POST.get('middleName')
            lastName = request.POST.get('lastName')
            dob = request.POST.get('dob')
            gender_id = request.POST.get('gender')
            schoolLevel_id = request.POST.get('schoolLevel')
            className_id  = request.POST.get('className')
            address = request.POST.get('address')
            academicYear = request.POST.get('academicYear')
            status_id  = request.POST.get('status')
            
            
            gender = Genders.objects.get(id = gender_id )
            schoolLevel = SchoolLevels.objects.get(id = schoolLevel_id )
            className = SchoolClases.objects.get(id = className_id )
            status = Statuses.objects.get(id = status_id )
            
            user = User.objects.create_user(
                username = studentID,
                password = lastName,
                first_name = firstName,
                last_name = lastName, 
                role = 'student',
            )
            
            student = Students(
                user = user,
                studentID = studentID,
                firstName = firstName,
                middleName = middleName,
                lastName = lastName,
                dob = dob,
                gender = gender,
                schoolLevel = schoolLevel,
                className = className,
                address = address,
                academicYear = academicYear,
                status = status,
            )
            
            student.save()
            return redirect('students')

    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'icon': icon,
    }

    return render(request, 'base/students.html', context)


@login_required(login_url='home')
def edit_student(request, pk):
    student = Students.objects.get(id=pk)
    user = User.objects.get(username=student.user.username)  

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        middleName = request.POST.get('middleName')
        lastName = request.POST.get('lastName')
        gender_id = request.POST.get('gender')
        dob = request.POST.get('dob')
        schoolLevel_id = request.POST.get('schoolLevel')
        className_id = request.POST.get('className')
        address = request.POST.get('address')
        academicYear = request.POST.get('academicYear')
        status_id = request.POST.get('status')

        gender = Genders.objects.get(pk=gender_id)
        schoolLevel = SchoolLevels.objects.get(pk=schoolLevel_id)
        className = SchoolClases.objects.get(pk=className_id)
        status = Statuses.objects.get(pk=status_id)

        student.firstName = firstName
        student.middleName = middleName
        student.lastName = lastName
        student.gender = gender
        student.dob = dob
        student.schoolLevel = schoolLevel
        student.className = className
        student.address = address
        student.academicYear = academicYear
        student.status = status
        student.save()


        user.first_name = firstName 
        user.last_name = lastName   
        user.set_password(lastName) 

        user.save()

        messages.success(request, 'Student updated successfully')
        return redirect('students')  
    else:
        context = {
            'student': student,
            'genders': Genders.objects.all(),
            'school_levels': SchoolLevels.objects.all(),
            'school_classes': SchoolClases.objects.all(),
            'statuses': Statuses.objects.all(),
        }
        return render(request, 'base/students.html', context)



# Function to handle deleting a student
@login_required(login_url='home')
def delete_student(request, pk):
    current_page = request.GET.get('page', 1)

    student = Students.objects.get(id=pk)
    student.delete()

    query = request.GET.get('query', '')  
    return redirect(f"{reverse('students')}?page={current_page}&query={query}")
# Function to handle managing  students ending here


@login_required(login_url='home')
def BackendAssign(request):
    sitename = "ASSIGN CLASS | OPLAS TANZANIA "
    page_name = "Asssign"
    assignments = AssignToClasses.objects.all()
    teachers = Teachers.objects.all()
    schools = SchoolClases.objects.all()
    subjects = Subjects.objects.all()
    statuses = Statuses.objects.all()

    # Handle search query
    query = request.GET.get('q', '')
    if query:
        assignments = AssignToClasses.objects.filter(
            Q(Teacher__firstName__icontains=query) |
            Q(Teacher__lastName__icontains=query) |
            Q(School__ClassName__icontains=query) |  
            Q(Subject__SubjectName__icontains=query)   
        )
    else:
        assignments = AssignToClasses.objects.all()
    
           # Set up pagination
    paginator = Paginator(assignments, 10)  
    page_number = request.GET.get('page')
    try:
        assignments = paginator.page(page_number)
    except PageNotAnInteger:
        assignments = paginator.page(1)
    except EmptyPage:
        assignments = paginator.page(paginator.num_pages)

    context = {
        'sitename': sitename,
        'page_name': page_name,
        'assignments' : assignments,
        'teachers': teachers,
        'schools': schools,
        'subjects': subjects,
        'statuses': statuses,
    }
    return render (request , 'base/assign-to-class.html', context)

def filter_subjects(request):
    class_id = request.GET.get('class_id')
    assigned_subjects = AssignToClasses.objects.filter(School_id=class_id).values_list('Subject_id', flat=True)
    available_subjects = Subjects.objects.exclude(id__in=assigned_subjects)
    
    subjects_data = list(available_subjects.values('id', 'SubjectName'))  # 'SubjectName' matches your model field
    return JsonResponse({'subjects': subjects_data})  # Remove the trailing comma



def assign_to_class_create(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('Teacher')
        school_id = request.POST.get('School')
        subject_id = request.POST.get('Subject')
        status_id = request.POST.get('Status')

        teacher = Teachers.objects.get(id=teacher_id)
        school = SchoolClases.objects.get(id = school_id)
        subjects = Subjects.objects.get(id = subject_id)
        status= Statuses.objects.get(id = status_id)


        if teacher_id and school_id and subject_id and status_id:
            AssignToClasses.objects.create(
                Teacher=teacher,
                School=school,
                Subject=subjects,
                Status=status
            )
            messages.success(request, "Assignment created successfully!")
            return redirect('assing-to-class')
        
        else:
            messages.error(request, "All fields are required!")
        
        return redirect('assing-to-class')


def assign_to_class_update(request, pk):
    assignment = AssignToClasses.objects.get(pk=pk)

    if request.method == 'POST':
        teacher_id = request.POST.get('Teacher')
        school_id = request.POST.get('School')
        subject_id = request.POST.get('Subject')
        status_id = request.POST.get('Status')
        

        if teacher_id and school_id and subject_id and status_id:
            assignment.Teacher_id = teacher_id
            assignment.School_id = school_id
            assignment.Subject_id = subject_id
            assignment.Status_id = status_id
            assignment.save()
            messages.success(request, "Assignment updated successfully!")
        else:
            messages.error(request, "All fields are required!")

        return redirect('assing-to-class')
    

def assign_to_class_delete(request, pk):
    current_page = request.GET.get('page', 1)
    query = request.GET.get('query', '')

    assignment = AssignToClasses.objects.get(pk=pk)
    assignment.delete()

    messages.success(request, "Assignment deleted successfully!")
    return redirect(f"{reverse('assing-to-class')}?page={current_page}&query={query}")


# Function to handle managing questions starting from here
@login_required(login_url='home')
def BackendQuestions(request):    
    sitename = "QUESTIONS | OPLAS TANZANIA"
    page_name = 'BackendQuestions'
    questions = Questions.objects.all()
    who_posts = Teachers.objects.all()
    teachers = Teachers.objects.all()
    
    teacher_id = request.user.teacher.id 

    subjects = Subjects.objects.filter(
    id__in=AssignToClasses.objects.filter(Teacher_id=teacher_id).values_list('Subject_id', flat=True)
)
  
    levels = SchoolLevels.objects.filter(
    id__in=AssignToClasses.objects.filter(Teacher_id=teacher_id).values_list('School__SchoolLevel_id', flat=True)
)
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        questions = Questions.objects.filter(
            Q(QuestionName__icontains=query) |
            Q(QuestionBy__PostedBy__icontains=query) | 
            Q(LevelName__LevelName__icontains=query) |   
            Q(SubjectName__SubjectName__icontains=query) |  
            Q(ApprovedBy__lastName__icontains=query)  
        )
    else:
        questions = Questions.objects.all()
    
           # Set up pagination
    paginator = Paginator(questions, 10)  
    page_number = request.GET.get('page')
    try:
        questions = paginator.page(page_number)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
        
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'questions': questions,
        'subjects': subjects,
        'levels': levels,
        'who_posts': who_posts,
        'teachers': teachers,
        'query': query
    }
    
    return render(request, 'base/backend-questions.html', context)


# Set up logging for debugging
logger = logging.getLogger(__name__)

@login_required(login_url='home')
def AddQuestions(request):
    sitename = "Questions | OPLAS TANZANIA"
    page_name = "Questions"
    icon = "fa fa-dashboard"

    # Handle form submission for CSV file upload
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            try:
                # Decode and read the CSV file
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_file)

                # Initialize a list to keep track of errors
                errors = []

                # Process each row in the CSV
                for row in reader:
                    try:
                        # Extract fields from the CSV row
                        question_name = row.get('QuestionName', '').strip()
                        level_name_id = row.get('LevelName', '').strip()
                        subject_name_id = row.get('SubjectName', '').strip()

                        # Validate that all required fields are present
                        if not question_name:
                            raise ValueError("Question Name is required and cannot be empty.")
                        if not level_name_id:
                            raise ValueError("Level Name is required and cannot be empty.")
                        if not subject_name_id:
                            raise ValueError("Subject Name is required and cannot be empty.")

                        # Fetch foreign key objects based on the CSV data
                        level_name = SchoolLevels.objects.get(pk=level_name_id)
                        subject_name = Subjects.objects.get(pk=subject_name_id)
                        question_by = request.user.teacher  # Assuming the user is the "QuestionBy"
                        approved_by = request.user.teacher  # Assuming the user is also "ApprovedBy"

                        # Create a new question record
                        question = Questions(
                            QuestionName=question_name,
                            QuestionBy=question_by,
                            LevelName=level_name,
                            SubjectName=subject_name,
                            IsApproved=True,  # Default to True
                            ApprovedBy=approved_by
                        )
                        question.save()

                        # Success message
                        messages.success(request, f"Question '{question_name}' added successfully.")

                    except Exception as e:
                        # Collect error messages for each row that fails
                        error_message = f"Error processing question: {row.get('QuestionName', 'Unknown')}. Error: {e}"
                        errors.append(error_message)

                # If there were errors, display them to the user
                if errors:
                    messages.error(request, "Some questions could not be processed:\n" + "\n".join(errors))

                # Redirect after processing all rows
                return redirect('backend_questions')

            except Exception as e:
                # Handle errors related to reading the CSV file
                messages.error(request, "Failed to read the CSV file. Please ensure it's formatted correctly.")
                return redirect('backend_questions')

        else:
            # Handle form submission when no CSV file is uploaded
            question_name = request.POST.get('questionName')
            level_name_id = request.POST.get('levelName')
            subject_name_id = request.POST.get('subjectName')

            try:
                # Fetch foreign key objects based on the form data
                level_name = SchoolLevels.objects.get(id=level_name_id)
                subject_name = Subjects.objects.get(id=subject_name_id)
                question_by = request.user.teacher  # Assuming the user is the "QuestionBy"
                approved_by = request.user.teacher  # Assuming the user is also "ApprovedBy"

                # Create a new question record
                question = Questions(
                    QuestionName=question_name,
                    QuestionBy=question_by,
                    LevelName=level_name,
                    SubjectName=subject_name,
                    IsApproved=True,  # Default to True
                    ApprovedBy=approved_by
                )
                question.save()
                messages.success(request, f"Question '{question_name}' added successfully.")

            except Exception as e:
                messages.error(request, f"Error adding question: {e}")

            return redirect('backend_questions')

    else:
        # Handle the case where no CSV file was uploaded
        messages.error(request, "No CSV file uploaded. Please try again.")
        return redirect('backend_questions')

    # # Prepare context for rendering the template
    # context = {
    #     'sitename': sitename,
    #     'page_name': page_name,
    #     'icon': icon,
    #     'questions': Questions.objects.all(),
    # }

    # # Render the questions page
    # return render(request, 'backend/questions.html', context)



# Edit question view
@login_required(login_url='home')
def edit_question(request, pk):
    question = Questions.objects.get( pk=pk)
    
    if request.method == 'POST':          
        QuestionName = request.POST.get('questionName')  
        LevelName_id = request.POST.get('levelName')  
        SubjectName_id = request.POST.get('subjectName') 

        IsApproved = 'True'  
        ApprovedBy = request.user.teacher 
        QuestionBy = request.user.teacher
        
        LevelName = SchoolLevels.objects.get(id=LevelName_id)
        SubjectName = Subjects.objects.get(id=SubjectName_id)
        
        
        question.QuestionName = QuestionName
        question.QuestionBy = QuestionBy
        question.LevelName = LevelName
        question.SubjectName = SubjectName
        question.IsApproved = IsApproved
        question.ApprovedBy = ApprovedBy

      
        question.save()
        
     
        messages.success(request, 'Question updated successfully.')
        
      
        return redirect('backend_questions')
    
   
    return render(request, 'teachers/equestions.html', {'question': question})

# Delete question view
@login_required(login_url='home')
def delete_question(request, pk):
    current_page = request.GET.get('page', 1)

    question = Questions.objects.get(pk=pk)
    question.delete()

    query = request.GET.get('query', '') 
    return redirect(f"{reverse('backend_questions')}?page={current_page}&query={query}")
# Function to handle managing questions ending here



# Function to handle managing notes starting from here
@login_required(login_url='home')
def BackendNotes(request):    
    sitename = "NOTES | OPLAS TANZANIA"
    page_name = 'BackendNotes'   
    notes = Notes.objects.all()
    subjects =  Subjects.objects.all()
    levels = SchoolLevels.objects.all()
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        notes = Notes.objects.filter(
            Q(NotesName__icontains=query) |
            Q(SubjectName__SubjectName__icontains=query) |
            Q(LevelName__LevelName__icontains=query)
        )
    else:
        notes = Notes.objects.all()
        
        
    # Set up pagination
    paginator = Paginator(notes, 10)  
    page_number = request.GET.get('page')
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'notes': notes,
        'subjects': subjects,
        'levels': levels
    }
    
    return render(request, 'base/backend-notes.html', context)
@login_required(login_url='home')
def notes_upload(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES and 'pdf_files' in request.FILES:
            csv_file = request.FILES['csv_file']
            pdf_files = request.FILES.getlist('pdf_files')

            try:
                # Read and decode the CSV file
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)

                # Normalize headers by stripping whitespace
                headers = [header.strip() for header in reader.fieldnames]
                if 'PDFName' not in headers:
                    return render(request, 'base/backend-notes.html', {'errors': ["CSV does not contain 'PDFName' column."]})

                # Create a dictionary of PDF files keyed by their names
                pdf_dict = {pdf.name.strip(): pdf for pdf in pdf_files}

                errors = []
                successful_notes = []

                # Iterate through each row in the CSV
                for row in reader:
                    # Normalize row keys
                    normalized_row = {key.strip(): value for key, value in row.items()}

                    pdf_name = normalized_row.get('PDFName')
                    if not pdf_name:
                        errors.append("Row does not contain 'PDFName'.")
                        continue  # Skip this iteration

                    # Attempt to retrieve the corresponding PDF file
                    pdf_file = pdf_dict.get(pdf_name.strip())

                    # Attempt to get ForeignKey instances
                    subject_name = normalized_row.get('SubjectName')
                    level_name = normalized_row.get('LevelName')

                    # Fetch the Subject instance
                    try:
                        subject_instance = Subjects.objects.get(id=subject_name.strip())
                    except Subjects.DoesNotExist:
                        errors.append(f"Subject with ID '{subject_name}' not found.")
                        continue  # Skip to the next row if the subject is not found

                    # Fetch the Level instance
                    try:
                        level_instance = SchoolLevels.objects.get(id=level_name.strip())
                    except SchoolLevels.DoesNotExist:
                        errors.append(f"Level with ID '{level_name}' not found.")
                        continue  # Skip to the next row if the level is not found

                    # Create a new note record
                    note = Notes(
                        NotesName=normalized_row['NotesName'].strip(),
                        SubjectName=subject_instance,
                        LevelName=level_instance,
                    )

                    # Attach the PDF file if it exists
                    if pdf_file:
                        note.UploadFile.save(pdf_file.name, pdf_file)
                        note.save()  # Save the note record here
                        successful_notes.append(note.NotesName)  # Track successful saves
                    else:
                        errors.append(f"PDF file '{pdf_name}' not found for notes '{normalized_row['NotesName']}'.")

                # Check if there are any errors or successful saves
                if errors:
                    return render(request, 'base/backend-notes.html', {'errors': errors})
                elif successful_notes:
                    return redirect('backend_notes')  # Redirect to the index page on success

            except Exception as e:
                # Handle exceptions and log them if necessary
                print("Error:", str(e))
                return render(request, 'base/backend-notes.html', {'errors': [str(e)]})

    # Render the upload form for GET requests or after processing the POST request
    return redirect('backend_notes')


@login_required(login_url='home')
def edit_notes(request, pk):
    note = Notes.objects.get(pk=pk)
    
    if request.method == 'POST':
        notes_name = request.POST.get('NotesName')
        subject_id = request.POST.get('SubjectName')
        level_id = request.POST.get('LevelName')
        upload_file = request.FILES.get('UploadFile')

        if notes_name and subject_id and level_id:
            subject = Subjects.objects.get(pk=subject_id)
            level = SchoolLevels.objects.get(pk=level_id)
            
            note.NotesName = notes_name
            note.SubjectName = subject
            note.LevelName = level
            if upload_file:
                note.UploadFile = upload_file
            note.save()
            messages.success(request, 'Notes updated successfully.')
            return redirect('backend_notes')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('backend_notes')

@login_required(login_url='home')
def delete_notes(request, pk):
    current_page = request.GET.get('page', 1)

    note = Notes.objects.get(id=pk)
    note.delete()
    messages.success(request, 'Notes deleted successfully.')

    query = request.GET.get('query', '') 
    return redirect(f"{reverse('backend_notes')}?page={current_page}&query={query}")
# Function to handle managing notes ending here



# Function to handle managing books starting from here
@login_required(login_url='home')
def BackendBooks(request):
        
    sitename = "BOOKS | OPLAS TANZANIA"
    page_name = 'BackendBooks'  
    
    books = Books.objects.all()
    subjects =  Subjects.objects.all()
    levels = SchoolLevels.objects.all()
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        books = Books.objects.filter(
            Q(BookName__icontains=query) |
            Q(SubjectName__SubjectName__icontains=query) |
            Q(LevelName__LevelName__icontains=query) 

        )
    else:
        books = Books.objects.all()
    
    query = request.GET.get('q')
    if query:
        books = Books.objects.filter(
            Q(BookName__icontains=query) |
            Q(SubjectName__SubjectName__icontains=query) |
            Q(LevelName__LevelName__icontains=query)
        )
    else:
        books = Books.objects.all()
        
    # Pagination setup
 
    paginator = Paginator(books, 10) 

    page_number = request.GET.get('page', 1)  
    books_page = paginator.get_page(page_number) 
    
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'books': books_page,
        'subjects': subjects,
        'levels': levels,
    }
    
    return render(request, 'base/backend-books.html', context)

@login_required(login_url='home')
def books_upload(request):

    if request.method == 'POST':
        if 'csv_file' in request.FILES and 'pdf_files' in request.FILES:
            csv_file = request.FILES['csv_file']
            pdf_files = request.FILES.getlist('pdf_files')

            try:
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)

                headers = [header.strip() for header in reader.fieldnames]
                if 'PDFName' not in headers:
                    return render(request, 'base/backend-books.html', {'errors': ["CSV does not contain 'PDFName' column."]})
                
                pdf_dict = {pdf.name.strip(): pdf for pdf in pdf_files}

                errors = []
                successful_books = []

                for row in reader:
                    normalized_row = {key.strip(): value for key, value in row.items()}

                    pdf_name = normalized_row.get('PDFName')
                    if not pdf_name:
                        errors.append("Row does not contain 'PDFName'.")
                        continue  

                    pdf_file = pdf_dict.get(pdf_name.strip())

                    subject_name = normalized_row.get('SubjectName')
                    level_name = normalized_row.get('LevelName')

                    try:
                        subject_instance = Subjects.objects.get(id=subject_name.strip())  
                    except Subjects.DoesNotExist:
                        errors.append(f"Subject with ID '{subject_name}' not found.")
                        continue  

                    try:
                        level_instance = SchoolLevels.objects.get(id=level_name.strip())  
                    except SchoolLevels.DoesNotExist:
                        errors.append(f"Level with ID '{level_name}' not found.")
                        continue 

                    book = Books(
                        BookName=normalized_row['BookName'].strip(),
                        SubjectName=subject_instance,
                        LevelName=level_instance,
                    )

                    if pdf_file:
                        book.UploadFile.save(pdf_file.name, pdf_file)
                        book.save()  
                        successful_books.append(book.BookName)
                    else:
                        errors.append(f"PDF file '{pdf_name}' not found for book '{normalized_row['BookName']}'.")

                if errors:
                    return render(request, 'base/backend-books.html', {'errors': errors})
                elif successful_books:
                    return redirect('BackendBooks')  

            except Exception as e:

                print("Error:", str(e))  
                return render(request, 'base/backend-books.html', {'errors': [str(e)]})

    return redirect('BackendBooks')


@login_required(login_url='home')
def edit_book(request, pk):
    book = Books.objects.get(pk=pk)
    
    if request.method == 'POST':
        book_name = request.POST.get('BookName')
        subject_id = request.POST.get('SubjectName')
        level_id = request.POST.get('LevelName')
        upload_file = request.FILES.get('UploadFile')

        if book_name and subject_id and level_id:
            subject = Subjects.objects.get(pk=subject_id)
            level = SchoolLevels.objects.get(pk=level_id)
            
            book.BookName = book_name
            book.SubjectName = subject
            book.LevelName = level
            if upload_file:
                book.UploadFile = upload_file
            book.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('backend_books')
        else:
            messages.error(request, 'Please fill in all required fields.')

    subjects = Subjects.objects.all()
    levels = SchoolLevels.objects.all()
    
    context = {
        'book': book,
        'subjects': subjects,
        'levels': levels
    }
    return redirect('backend_books')



@login_required(login_url='home')
def delete_book(request, book_id):
    
    current_page = request.GET.get('page', 1)
  
    book = Books.objects.get(id=book_id)
    book.delete()

   
    query = request.GET.get('query', '') 
    return redirect(f"{reverse('backend_books')}?page={current_page}&query={query}")

# Function to handle managing books ending here



# Function to handle managing papers starting from here
@login_required(login_url='home')
def BackendPapers(request):    
    sitename = "PREVIOUS PAPERS | OPLAS TANZANIA"
    page_name = 'BackendPapers' 
    subjects = Subjects.objects.all()
    levels = SchoolLevels.objects.all()
    papers = Papers.objects.all() 
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        papers = Papers.objects.filter(
            Q(PaperName__icontains=query) |
            Q(SubjectName__SubjectName__icontains=query) |
            Q(LevelName__LevelName__icontains=query)
        )
    else:
        papers = Papers.objects.all()
    
         # Set up pagination
    paginator = Paginator(papers, 10)  
    page_number = request.GET.get('page')
    try:
        papers = paginator.page(page_number)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)
    
      
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'papers': papers,
        'subjects': subjects,
        'levels': levels,
    }
    
    return render(request, 'base/backend-papers.html', context)



# Configure logging
logger = logging.getLogger(__name__)
@login_required(login_url='home')
def papers_upload(request):

    if request.method == 'POST':
        if 'csv_file' in request.FILES and 'pdf_files' in request.FILES:
            csv_file = request.FILES['csv_file']
            pdf_files = request.FILES.getlist('pdf_files')
            logger.debug("Uploaded PDF files: %s", [pdf.name for pdf in pdf_files])

            try:
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)
                headers = [header.strip() for header in reader.fieldnames]
                required_headers = ['PaperName', 'SubjectName', 'LevelName', 'PDFName']

                for header in required_headers:
                    if header not in headers:
                        return render(request, 'backend-papers.html', {'errors': [f"CSV does not contain '{header}' column."]})

                pdf_dict = {pdf.name.strip(): pdf for pdf in pdf_files}
                errors = []
                successful_papers = []

                for row in reader:
                    normalized_row = {key.strip(): value.strip() for key, value in row.items()}
                    paper_name = normalized_row.get('PaperName')
                    subject_id = normalized_row.get('SubjectName')
                    level_id = normalized_row.get('LevelName')
                    pdf_name = normalized_row.get('PDFName')

                    # Fetch instances
                    try:
                        subject_instance = Subjects.objects.get(id=subject_id)
                        level_instance = SchoolLevels.objects.get(id=level_id)
                    except Subjects.DoesNotExist:
                        errors.append(f"Subject with ID '{subject_id}' not found.")
                        continue
                    except SchoolLevels.DoesNotExist:
                        errors.append(f"Level with ID '{level_id}' not found.")
                        continue

                    # Create Paper entry
                    paper = Papers(
                        PaperName=paper_name,
                        SubjectName=subject_instance,
                        LevelName=level_instance,
                    )

                    pdf_file = pdf_dict.get(pdf_name)
                    if pdf_file and pdf_file.name.endswith('.pdf'):
                        paper.UploadFile.save(pdf_file.name, pdf_file)
                        paper.save()
                        successful_papers.append(paper.PaperName)
                    else:
                        errors.append(f"PDF file '{pdf_name}' not found or is not a PDF for paper '{paper_name}'.")

                if errors:
                    logger.error("Errors encountered: %s", errors)
                    return render(request, 'backend-papers.html', {'errors': errors})
                elif successful_papers:
                    success_message = f"Successfully uploaded papers: {', '.join(successful_papers)}."
                    logger.info(success_message)
                    return redirect('backend_papers')

            except Exception as e:
                logger.exception("Error during processing: %s", str(e))
                return render(request, 'base/backend-papers.html', {'errors': [str(e)]})

    return redirect('backend_papers')


@login_required(login_url='home')
def edit_paper(request, pk):
    paper = Papers.objects.get( id=pk)  # Fetch the paper to edit
    subjects = Subjects.objects.all()
    levels = SchoolLevels.objects.all()

    if request.method == 'POST':
        paper_name = request.POST.get('PaperName')
        subject_id = request.POST.get('SubjectName')
        level_id = request.POST.get('LevelName')
        upload_file = request.FILES.get('UploadFile')

        if paper_name and subject_id and level_id:
            subject =Subjects.objects.get (id=subject_id)
            level = SchoolLevels.objects.get(id=level_id)

            paper.PaperName = paper_name
            paper.SubjectName = subject
            paper.LevelName = level
            if upload_file:
                paper.UploadFile = upload_file
            paper.save()
            messages.success(request, 'Paper updated successfully.')
            return redirect('backend_papers') 
        else:
            messages.error(request, 'Please fill in all required fields.')

    context = {
        'paper': paper,
        'subjects': subjects,
        'levels': levels
    }
    return redirect('backend_papers') 




@login_required(login_url='home')
def delete_paper(request, pk):
    current_page = request.GET.get('page', 1)

    paper = Papers.objects.get(pk=pk)
    paper.delete()
    messages.success(request, 'Paper deleted successfully.')

    query = request.GET.get('query', '') 
    return redirect(f"{reverse('backend_papers')}?page={current_page}&query={query}")

# Function to handle managing papers ending here

@login_required(login_url='home')
def BackendVideoLessons(request):    
    sitename = "VIDEO LESSONS | OPLAS TANZANIA"
    page_name = 'BackendVideo' 
     
    videos = Videos.objects.all()
    subjects =  Subjects.objects.all()
    levels = SchoolLevels.objects.all()
    
    # Handle search query
    query = request.GET.get('q', '')
    if query:
        videos = Videos.objects.filter(
            Q(VideosName__icontains=query) |
            Q(LevelName__LevelName__icontains=query) |
            Q(SubjectName__SubjectName__icontains=query)
        )
    else:
        videos = Videos.objects.all()
    
    # Set up pagination
    paginator = Paginator(videos, 10)  
    page_number = request.GET.get('page')
    try:
        videos = paginator.page(page_number)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
      
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'videos': videos,
        'subjects': subjects,
        'levels': levels,
    }
    
    return render(request, 'base/backend-video.html', context)



@login_required(login_url='home')
def videos_upload(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES and 'video_files' in request.FILES:
            csv_file = request.FILES['csv_file']
            video_files = request.FILES.getlist('video_files')

            try:
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)

                headers = [header.strip() for header in reader.fieldnames]
                if 'VideosName' not in headers or 'FileName' not in headers:
                    return render(request, 'base/backend-video.html', {'errors': ["CSV must contain 'VideosName' and 'FileName' columns."]})

                
                video_dict = {video.name.strip(): video for video in video_files}

                errors = []
                successful_videos = []

                
                for row in reader:
                 
                    normalized_row = {key.strip(): value for key, value in row.items()}

                    video_name = normalized_row.get('VideosName')
                    file_name = normalized_row.get('FileName')
                    if not video_name or not file_name:
                        errors.append("Row is missing 'VideosName' or 'FileName'.")
                        continue  

                    
                    video_file = video_dict.get(file_name.strip())
                    if not video_file:
                        errors.append(f"Video file '{file_name}' not found for video '{video_name}'.")
                        continue  

                   
                    subject_name = normalized_row.get('SubjectName')
                    level_name = normalized_row.get('LevelName')

                   
                    try:
                        subject_instance = Subjects.objects.get(id=subject_name.strip())
                    except Subjects.DoesNotExist:
                        errors.append(f"Subject with ID '{subject_name}' not found.")
                        continue  

                   
                    try:
                        level_instance = SchoolLevels.objects.get(id=level_name.strip())
                    except SchoolLevels.DoesNotExist:
                        errors.append(f"Level with ID '{level_name}' not found.")
                        continue  

                    
                    video = Videos(
                        VideosName=video_name.strip(),
                        SubjectName=subject_instance,
                        LevelName=level_instance,
                    )
                    video.UploadFile.save(video_file.name, video_file)
                    video.save()  
                    successful_videos.append(video.VideosName)  

               
                if errors:
                    return render(request, 'base/backend-videos.html', {'errors': errors})
                elif successful_videos:
                    return redirect('backend_video')  

            except Exception as e:
                
                print("Error:", str(e))
                return redirect('backend_video')


    return redirect('backend_video')
@login_required(login_url='home')
def edit_video(request, pk):
    video = Videos.objects.get(id=pk)
    if request.method == 'POST':
        videosName = request.POST.get('VideosName')
        subjectName_id = request.POST.get('SubjectName')
        levelName_id = request.POST.get('LevelName')
        upload_file = request.FILES.get('UploadFile')
        
        
        subjectName = Subjects.objects.get(pk=subjectName_id)
        levelName = SchoolLevels.objects.get(pk=levelName_id)
        
        video.VideosName = videosName
        video.SubjectName = subjectName
        video.LevelName = levelName
        
        if upload_file:
            video.UploadFile = upload_file       
        
        video.save()
        
        return redirect('backend_video')
    return render(request, 'base/edit-video.html', {'video': video})


@login_required(login_url='home')
def delete_video(request, pk):
    current_page = request.GET.get('page', 1)

    video = Videos.objects.get(id=pk)
    video.delete()
    messages.success(request, "Video successfully deleted.")

    query = request.GET.get('query', '')
    return redirect(f"{reverse('backend_video')}?page={current_page}&query={query}")

@login_required(login_url='home')
def BackendAnswers(request):    
    sitename = "ANSWERS | OPLAS TANZANIA"
    page_name = 'BackendAnswers'  
    
    answers = Answers.objects.all()
    questions = Questions.objects.all()
    who_posts = WhoPosts.objects.all()
    teachers = Teachers.objects.all()
    
     # Handle search query
    query = request.GET.get('q', '')
    if query:
        answers = Answers.objects.filter(
            Q(Answer__icontains=query) |
            Q(AnswerBy__PostedBy__icontains=query) |
            Q(QuestionName__QuestionName__icontains=query) |
            Q(ApprovedBy__lastName__icontains=query) |
            Q(ApprovedBy__firstName__icontains=query) |
            Q(ApprovedBy__middleName__icontains=query)
        )
    else:
        answers = Answers.objects.all()
    
     # Set up pagination
    paginator = Paginator(answers, 10)  
    page_number = request.GET.get('page')
    try:
        answers = paginator.page(page_number)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)
    
      
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'answers': answers,
        'questions': questions,
        'who_posts': who_posts,
        'teachers': teachers,
    }
    
    return render(request, 'base/backend-answers.html', context)


@login_required(login_url='home')
def answers_upload(request):

    if request.method == 'POST':

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']

            try:
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)
                headers = [header.strip() for header in reader.fieldnames]
                required_headers = ['QuestionID', 'AnswerText', 'AnswerBy', 'IsApproved', 'ApprovedBy']

       
                missing_headers = [header for header in required_headers if header not in headers]
                if missing_headers:
                    error_message = f"CSV does not contain the following required columns: {', '.join(missing_headers)}."
                    messages.error(request, error_message)
                    return render(request, 'base/backend-answers.html', {'errors': [error_message]})

                errors = []
                successful_answers = []

            
                for row in reader:
                    normalized_row = {key.strip(): value.strip() for key, value in row.items()}
                    question_id = normalized_row.get('QuestionID')
                    answer_text = normalized_row.get('AnswerText')
                    answer_by_id = normalized_row.get('AnswerBy')
                    is_approved = normalized_row.get('IsApproved', 'false').lower() == 'true'
                    approved_by_id = normalized_row.get('ApprovedBy')

        
                    try:
                        question_instance = Questions.objects.get(id=question_id)
                        answer_by_instance = WhoPosts.objects.get(id=answer_by_id)
                        approved_by_instance = Teachers.objects.get(id=approved_by_id)
                    except Questions.DoesNotExist:
                        errors.append(f"Question with ID '{question_id}' not found.")
                        messages.warning(request, errors[-1])
                        continue
                    except WhoPosts.DoesNotExist:
                        errors.append(f"User with ID '{answer_by_id}' not found.")
                        messages.warning(request, errors[-1])
                        continue
                    except Teachers.DoesNotExist:
                        errors.append(f"Teacher with ID '{approved_by_id}' not found.")
                        messages.warning(request, errors[-1])
                        continue

                    answer = Answers(
                        QuestionName=question_instance,
                        AnswerBy=answer_by_instance,
                        Answer=answer_text,
                        IsApproved=is_approved,
                        ApprovedBy=approved_by_instance
                    )
                    answer.save()
                    successful_answers.append(answer.Answer)

               
                if errors:
                    messages.error(request, "Errors encountered during CSV processing.")
                    return render(request, 'base/backend-answers.html', {'errors': errors})
                elif successful_answers:
                    success_message = f"Successfully uploaded answers: {', '.join(successful_answers)}."
                    messages.success(request, success_message)
                    return redirect('backend_answers')

            except Exception as e:
                messages.error(request, f"Error during processing: {str(e)}")
                return render(request, 'base/backend-answers.html', {'errors': [str(e)]})

        elif 'QuestionName' in request.POST:
            question_id = request.POST.get('QuestionName')
            answer = request.POST.get('answer')
            answer_by_id = request.POST.get('answerBy')
            is_approved_str = request.POST.get('isApproved')
            is_approved = is_approved_str == 'True'
            approved_by_id = request.POST.get('approvedBy')

            try:
                question_instance = Questions.objects.get(id=question_id)
                answer_by_instance = WhoPosts.objects.get(id=answer_by_id)
                approved_by_instance = Teachers.objects.get(id=approved_by_id)
            except Questions.DoesNotExist:
                messages.warning(request, f"Question with ID '{question_id}' not found.")
                return redirect('backend_answers')
            except WhoPosts.DoesNotExist:
                messages.warning(request, f"User with ID '{answer_by_id}' not found.")
                return redirect('backend_answers')
            except Teachers.DoesNotExist:
                messages.warning(request, f"Teacher with ID '{approved_by_id}' not found.")
                return redirect('backend_answers')

  
            answer = Answers(
                QuestionName=question_instance,
                AnswerBy=answer_by_instance,
                Answer=answer,
                IsApproved=is_approved,
                ApprovedBy=approved_by_instance
            )
            answer.save()
            messages.success(request, "Answer successfully submitted.")
            return redirect('backend_answers')

    return render(request, 'base/backend-answers.html')  


@login_required(login_url='home')
def edit_answers(request, pk):
  
    answer = Answers.objects.get(id=pk)

    if request.method == 'POST':
       
        answer_text = request.POST.get('answer')
        questionName_id = request.POST.get('questionName')
        answerBy_id = request.POST.get('answerBy')
        isApproved = request.POST.get('isApproved') == 'true'
        approvedBy_id = request.POST.get('approvedBy')
        
        
        questionName = Questions.objects.get(id=questionName_id)
        answerBy = WhoPosts.objects.get(id=answerBy_id)
        approvedBy = Teachers.objects.get(id=approvedBy_id)

        
        answer.Answer = answer_text  
        answer.QuestionName = questionName  
        answer.AnswerBy = answerBy
        answer.IsApproved = isApproved  
        answer.ApprovedBy = approvedBy  
        

        answer.save()
        

        messages.success(request, "Answer successfully updated.")
        

        return redirect('backend_answers')
    
@login_required(login_url='home')
def delete_answers(request, pk):
    current_page = request.GET.get('page', 1)
    query = request.GET.get('query', '')  

    answer = Answers.objects.get(id=pk)
    answer.delete()
    messages.success(request, "Answer successfully deleted.")

    return redirect(f"{reverse('backend_answers')}?page={current_page}&query={query}")

@login_required(login_url='home')
def add_comments(request, question_id):
    sitename = "Comments | Oplas Tanzania"
    page_name = 'Comments'

    question = Questions.objects.get(id=question_id)
    student = request.user.student
    
    # viewed_questions = request.session.get('viewed_questions', [])
    
    # if question.id not in viewed_questions:
    #     question.increment_views() 
    #     viewed_questions.append(question.id)  
    #     request.session['viewed_questions'] = viewed_questions  

    if request.method == 'POST':
        comment_text = request.POST.get('commentText')
        
        
        teacher = assign_teacher_to_comment(question, student)

        if teacher:
 
            comment = Comments.objects.create(
            content_type=ContentType.objects.get_for_model(Questions),
            object_id=question.id,
            commentText=comment_text,
            student=student,
            teacher=teacher

           ) 
        return redirect('view_answers', pk= question.id)
         


def add_askQustion_comments(request, ask_question_id):
    sitename = "Comments | Oplas Tanzania"
    page_name = 'Comments'

    question = AskQuestion.objects.get(id=ask_question_id)
    student = request.user.student
     

    if request.method == 'POST':
        comment_text = request.POST.get('commentText')
        
        
        teacher = assign_teacher_to_comment(question, student)

        if teacher:
            
            comment = Comments.objects.create(
            content_type=ContentType.objects.get_for_model(AskQuestion),
            object_id=question.id,
            commentText=comment_text,
            student=student,
            teacher=teacher

           ) 
        return redirect('view_asked_questions', pk= question.id)


@login_required(login_url='home')
def backend_comments(request):
    sitename = "Comments | Oplas Tanzania"
    page_name = 'Comments'
    comments = Comments.objects.all()
    
     # Handle search query
    query = request.GET.get('q', '')
    if query:
        comments = Comments.objects.filter(
            Q(commentText__icontains=query) |
            Q(isApproved__icontains=query) |
            Q(student__firstName__icontains=query) |
            Q(student__middleName__icontains=query) |
            Q(student__lastName__icontains=query) |
            Q(question__QuestionName__icontains=query)
        )
    else:
        comments = Comments.objects.all()
    
     # Set up pagination
    paginator = Paginator(comments, 10)  
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
        
    context = {
        'sitename': sitename,
        'page_name': page_name,
        'comments': comments,
    }
    return render(request, 'base/backend-comments.html', context)


@login_required(login_url='home')
def approve_comment(request, comment_id):
    current_page = request.GET.get('page', 1)  
    query = request.GET.get('query', '')  

    try:
        comment = Comments.objects.get(id=comment_id)
        
        if request.user.role == 'teacher': 
            comment.isApproved = True
            comment.save()
            messages.success(request, "Comment approved successfully.")
        else:
            messages.error(request, "You are not authorized to approve comments.")
    
    except Comments.DoesNotExist:
        messages.error(request, "Comment not found.")
    
    return redirect(f"{reverse('backend-comments')}?page={current_page}&query={query}")




@login_required(login_url='home')
def delete_comments(request, pk):
    current_page = request.GET.get('page', 1)
    query = request.GET.get('query', '')  

  
    comment = Comments.objects.get(id=pk)
    comment.delete()
    messages.success(request, "Comment successfully deleted.")

    return redirect(f"{reverse('backend-comments')}?page={current_page}&query={query}")

@login_required(login_url='home')
@login_required(login_url='home')
def ask_question(request):
    if request.method == 'POST':

        subject_id = request.POST.get('subject')
        question_text = request.POST.get('message')

        if not subject_id or not question_text:
            messages.error(request, "Subject or question text cannot be empty.")
            return redirect('home')

        try:
            subject = Subjects.objects.get(id=subject_id)
        except Subjects.DoesNotExist:
            messages.error(request, "The selected subject does not exist.")
            return redirect('home')

        try:
            student_class = request.user.student.className
        except ObjectDoesNotExist:
            messages.error(request, "You are not associated with any class.")
            return redirect('home')

        try:
            level_name = student_class.SchoolLevel  
        except AttributeError:
            messages.error(request, "The class is not associated with a valid level.")
            return redirect('home')

        assignment = AssignToClasses.objects.filter(
            School=student_class,
            Subject=subject
        ).first()


        if not assignment:
            messages.error(request, "No teacher is assigned to this subject for your class.")
            return redirect('home')

        ask_question = AskQuestion.objects.create(
            student=request.user,
            SubjectName=subject,
            LevelName=level_name,
            class_name=student_class,
            assignment=assignment,
            question_text=question_text,
            is_answered=False
        )

        Notification.objects.create(
            user=assignment.Teacher.user,
            ask_question=ask_question,
            message=f"New question received for {subject.SubjectName} from {request.user.student.firstName} {request.user.student.middleName} {request.user.student.lastName}",
        )

        messages.success(request, "Your question has been sent to the teacher.")
        return redirect('asked_questions')

    return render(request, 'error.html')




@login_required(login_url='home')
def ask_question_detail(request, pk):
    sitename = "Asked Questions | Oplas Tanzania"
    page_name = 'Questions'
    
    try:
        question = AskQuestion.objects.get(id = pk,assignment__Teacher__user=request.user)
    except AskQuestion.DoesNotExist:

        question = None
    
    context = {
        sitename: sitename,
        page_name: page_name,
        'question': question
}
    return render(request, 'base/ask-questions-view.html', context)


@login_required(login_url='home')
def answer_question(request, pk):

    if request.user.role != 'teacher':
        return redirect('home')


    question =AskQuestion.objects.get( id=pk)

    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')


        answer = AnswerQuestion.objects.create(
            question_ask=question,
            answer_text=answer_text,
            answered_by=request.user
        )

        question.is_answered = True
        question.save()

        Notification.send_answer_notification(answer)

        messages.success(request, "You have successfully answered the question.")
        return redirect(reverse('ask-question-list', args=[question.id]))



@login_required(login_url='home')
def answer_question_detail(request, pk):
    sitename = "Asked Questions | Oplas Tanzania"
    page_name = 'Questions'
    
    questions = AskQuestion.objects.all()
    
    try:
        ansewer = AnswerQuestion.objects.get(id = pk)
    except AnswerQuestion.DoesNotExist:

        ansewer = None
    
    context = {
        sitename: sitename,
        page_name: page_name,
        'ansewer': ansewer,
        'questions': questions
}
    return render(request, 'base/answer-questions-view.html', context)

#==============> Itabidi kuwe na full detail za asked questions , nani katuma, class gani na ni subject gani, muda aliotuma 
#==============> namna gani nzuri ya ku display maswali moja moja kwa kutumia id yake au yote kwa pamoja then ndio muda wa kujibu tutumie id kuselect swali la kujibu   
#==============> Second option to put id direct on notifications when teacher open specific notification for question , opened it with question id so there is no question lists but there is notifications lists
#==============> CHAT ROOM AND ASK QUESTION
 
#==============> comment has errors user no object student exists
#==============> PROBLEM video extend card , video loading is too much


#==============> 24 for subject assigned allowed to send asked question but other year failed "No teacher assigned"
#==============> submit empty student id or str instaed of number, csv submit without file
#==============>  answerby and questionby should be teacher instance not whoposts instance

#==============> comments approve should only display related to teacher
#==============> csv for adding question should remove unnecessary fields
#==============> assign to teachers
#==============> views, likes and notifications count
#==============> Error pages 500 and 404
#==============> Response messages for every action 
#==============> notifications should be disappear after question being answered
#==============>  comments should be approved first before posted
#==============>  Icons and footer should be considered
#==============> update password for students
#==============> add first and last name for teachers and students on csv upload
#==============> if subject already assign to teacher should not appeared on lists
#==============> no teacher object we look on solution either admin not have previlages of view questions or solve it
#==============> UNIQUE constraint failed: base_user.username repeat studentID
#==============> The given username must be set when submit empty studentID
#==============> Validate each field submission to avoid errors
#==============> Errors on add students or teacher not prevent user from being added so may cause conflict when student or teacher added again



