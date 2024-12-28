from .models import *

def assign_teacher_to_comment(question, student):
  
    """
    This function assigns a teacher to a comment based on the student's class level and the subject of the question. It does this by:

    Retrieving the student's class level and the subject of the question.
    Finding the teacher assigned to that subject and class level (with an active status).
    Returning the assigned teacher, or None if no teacher is found.
    In essence, it maps a student's comment to a teacher based on the student's class level and the question's subject.
    
    """
    class_name = student.className
    

    subject = question.SubjectName

    assignment = AssignToClasses.objects.filter(
        School=class_name,
        Subject=subject,
        Status__StatusName='Active'  
    ).first()
    
    
    teacher = assignment.Teacher if assignment else None
    
    return teacher
