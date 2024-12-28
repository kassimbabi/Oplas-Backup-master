from .models import *

def subject_context(request):
    subjects_context = Subjects.objects.all()
    return {'subjects_context': subjects_context}


def notifications_context(request):
    notifications = None
    
  
    if request.user.is_authenticated:
        try:
            notifications = request.user.notifications.all()
            
            unread_notifications = notifications.filter(is_read=False)
            if unread_notifications.exists():
                unread_notifications.update(is_read=True)
        
        except Notification.DoesNotExist:
            notifications = None
            
    return {'notifications': notifications}

def SubjectImage(request):
    subject_image = WebImages.objects.filter(ImageTitle='Subject').first()
    return {'subject_image': subject_image}

def NotesImage(request):
    notes_image = WebImages.objects.filter(ImageTitle='Notes').first()
    return {'notes_image': notes_image}

def BooksImage(request):
    book_image = WebImages.objects.filter(ImageTitle='Books').first()
    return {'book_image': book_image}

def PaperImage(request):
    paper_image = WebImages.objects.filter(ImageTitle='Paper').first()
    return {'paper_image': paper_image}

def RightAds(request):
    ads = WebImages.objects.filter(ImageTitle='Ads').first()
    return {'ads': ads}

def CarouselImages(request):
    carousel_images = WebImages.objects.filter(ImageTitle='Carousel').order_by('-id')
    return {'carousel_images': carousel_images}



# def question_context(request):
#     question_id = None
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         # Retrieve the question ID from the request path or session
#         question_id = request.session.get('question_id', None)

#         # Alternatively, if you have the question ID in the URL params or request object
#         if not question_id and 'question_id' in request.GET:
#             question_id = request.GET.get('question_id')

#         # Check if the question exists for the logged-in user's assignments
#         if question_id:
#             try:
#                 question = AskQuestion.objects.get(id=question_id, assignment__Teacher__user=request.user)
#                 question_id = question.id
#             except AskQuestion.DoesNotExist:
#                 question_id = None

#     return {'question_id': question_id}
