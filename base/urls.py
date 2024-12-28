from django.urls import path
from base import views

urlpatterns = [
    # path for login and logout
    path('login/', views.loginAuthentication , name= 'login'),
    path('logout/', views.logoutUser, name='logout'),
    
    
    # path for landing page and static pages
    path("", views.Home, name="home"),
    path("about-us", views.About, name="about"),
    path("contact-us", views.Contact, name="contact"),
    path("view-answers", views.ViewAnswers, name="view_answers"),
    path("asked-questions", views.AskedQestions, name="asked_questions"),
    path("view-asked-questions", views.ViewAskedQestions, name="view_asked_questions"),
    
    
    # path for students views resources
    path("questions-list/<int:subject_id>/<int:class_level_id>/", views.questions_view, name="questions-list"),
    path("notes/<int:subject_id>/<int:class_level_id>/", views.notes_view, name="notes-list"),
    path("papers/<int:subject_id>/<int:class_level_id>/", views.papers_view, name="papers-list"),
    path("books/<int:subject_id>/<int:class_level_id>/", views.books_view, name="books-list"),
    path("videos/<int:subject_id>/<int:class_level_id>/", views.videos_view, name="videos-list"),
    

    # path for classes and levels
    path("classes/levels/questions", views.questions_class_level, name="questions-class-levels"),
    path("classes/levels/notes", views.notes_class_level, name="notes-class-levels"),
    path("classes/levels/papers", views.papers_class_level, name="papers-class-levels"),
    path("classes/levels/books", views.books_class_level, name="books-class-levels"),
    path("classes/levels/videos", views.videos_class_level, name="videos-classes-levels"),

    
    # path for subject categories
    path('notes-subject-categories/<int:class_level_id>/', views.notes_subject_categories, name='notes-subject-categories'),
    path('books-subject-categories/<int:class_level_id>/', views.books_subject_categories, name='books-subject-categories'),
    path('papers-subject-categories/<int:class_level_id>/', views.papers_subject_categories, name='papers-subject-categories'),
    path('questions-subject-categories/<int:class_level_id>/', views.questions_subject_categories, name='questions-subject-categories'),
    path('videos-subject-categories/<int:class_level_id>/', views.videos_subject_categories, name='videos-subject-categories'),


    # path for dashboard (landing page after Admin and Teacher login)
    path("dashboard", views.Dashboard, name="dashboard"),
    
    
    
    # path for manage teachers
    path("teachers", views.manage_teachers, name="teachers"),
    path("add/teacher", views.AddTeachers, name="add-teacher"),
    path('edit/teacher/<int:teacher_id>/', views.edit_teacher, name='edit-teacher'),
    path('delete/teacher/<int:teacher_id>/', views.delete_teacher, name='delete-teacher'),
    
    
    # path for manage students
    path("students", views.manage_students, name="students"),
    path("add/student", views.register_student, name="add-student"),
    path('edit/student/<int:pk>/', views.edit_student, name='edit-student'),
    path('delete/student/<int:pk>/', views.delete_student, name='delete-student'),
    
    
    
    # path for manage questions
    path("backend-questions", views.BackendQuestions, name="backend_questions"),
    path("add/question", views.AddQuestions, name="add-questions"),
    path('edit/question/<int:pk>/', views.edit_question, name='edit-question'),
    path('delete/question/<int:pk>/', views.delete_question, name='delete-question'),
    
    
    # path for manage notes
    path("backend-notes", views.BackendNotes, name="backend_notes"),
    path('notes/upload', views.notes_upload, name='notes-upload'),
    path('edit/notes/<int:pk>/', views.edit_notes, name='edit-notes'),
    path('delete/notes/<int:pk>/', views.delete_notes, name='delete-notes'),
    
    
    
    # path for manage books
    path("backend-books", views.BackendBooks, name="backend_books"),
    path('books/upload', views.books_upload, name='books-upload'),
    path('edit/book/<int:pk>/', views.edit_book, name='edit-book'),
    path('delete/book/<int:book_id>/', views.delete_book, name='delete-book'),
    
    # path for manage previous papers
    path("backend-papers", views.BackendPapers, name="backend_papers"),
    path('papers/upload', views.papers_upload, name='papers-upload'),
    path('edit/paper/<int:pk>/', views.edit_paper, name='edit-paper'),
    path('delete/paper/<int:pk>/', views.delete_paper, name='delete-paper'),
    
    # path for manage videos
    path("video-lessons", views.BackendVideoLessons, name="backend_video"),
    path('videos/upload', views.videos_upload, name='videos-upload'),
    path('edit/video/<int:pk>/', views.edit_video, name='edit-video'),
    path('delete/video/<int:pk>/', views.delete_video, name='delete-video'),
    
    # path for manage answers
    path("answers", views.BackendAnswers, name="backend_answers"),
    path("answers/upload", views.answers_upload, name="answers-upload"),
    path('edit/answers/<int:pk>/', views.edit_answers, name='edit-answers'),
    path('delete/answers/<int:pk>/', views.delete_answers, name='delete-answer'),
    
    # path for manage profile
    path("my-profile", views.BackendProfile, name="backend_profile"),
    path("change/password", views.changePassword, name="change-password"),
    
    # path for manage comments
    path('add/comments/<int:question_id>/', views.add_comments, name='add-comment'),
    path('approve/comment/<int:comment_id>/', views.approve_comment, name='approve-comment'),
    path('backend/comments', views.backend_comments, name='backend-comments'),
    path('delete/comment/<int:pk>/', views.delete_comments, name='delete-comment' ),
    
    # path for manage asking questions
    path('ask/question', views.ask_question, name='ask-question'),
    path('ask/question/deteail/<int:pk>/', views.ask_question_detail, name='ask-question-list'),
    
    
    # path for manage answering questions
    path('answer/question/<int:pk>/', views.answer_question, name='answer-question'),
    path('answer/questions/detail/<int:pk>/', views.answer_question_detail, name='answer-question-list'),
    


]