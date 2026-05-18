from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from .models import*
from SiteAdmin.models import*
from django.contrib import messages
from Parent.models import Parent_Reg,Mark_marks,ParentTeacherMessage
from Student.models import Student_Reg,HomeworkSubmission,StudentTeacherMessage
from datetime import date
from Common.models import ReviewRemark
# Create your views here.

def teacherhome(request):
   return render(request,'teacher/teacher_home.html')


def teacher_register(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        gender=request.POST['gender']
        phone=request.POST['phone']
        qualification=request.POST['qualification'] 
        experience=request.POST['experience']
        subjects = request.POST.getlist('subjects')
        id_card=request.FILES['id_card']
        profile_picture = request.FILES.get('profile_picture')
        certificates=request.FILES.get('certificates')
        if User.objects.filter(username=username).exists():
           messages.error(request, "Username already exists!")
           return redirect('teacher_register')
        if User.objects.filter(email=email).exists():
          messages.error(request, "Email already exists!")
          return redirect('teacher_register')
        tuser=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        tuser.save()
        teacher=Teacher_Reg.objects.create(user=tuser,gender=gender,phone=phone,qualification=qualification,experience=experience,id_card=id_card, profile_picture=profile_picture, certificates=certificates)
        teacher.subjects.set(subjects) 
        teacher_obj,created=Group.objects.get_or_create(name='TEACHER')
        teacher_obj.user_set.add(tuser)
        messages.success(request,'Registration successfull')
    s=Subject.objects.all()
    return render(request,'common/teacher_registration.html',{'teachersub':s})

def teacher_profile(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)
    subjects = Subject.objects.all() 

    if request.method == 'POST':
        teacher.gender = request.POST.get('gender', teacher.gender)
        teacher.phone = request.POST.get('phone', teacher.phone)
        teacher.qualification = request.POST.get('qualification', teacher.qualification)
        teacher.experience = request.POST.get('experience', teacher.experience)

        selected_subjects = request.POST.getlist('subjects')
        if selected_subjects:
            teacher.subjects.set(selected_subjects)

        profile_pic = request.FILES.get('profile_picture')
        if profile_pic:
            teacher.profile_picture = profile_pic

        id_card_file = request.FILES.get('id_card')
        if id_card_file:
            teacher.id_card = id_card_file
        certificates=request.FILES.get('certificates')
        if certificates:
            teacher.certificates=certificates
        

        teacher.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('teacher_profile')

    return render(request, 'teacher/edit_teacher_profile.html', {
        'teacher': teacher,
        'subjects': subjects
    })


def view_parents(request):
   parents=Parent_Reg.objects.filter(status='approved')
   return render(request,'teacher/view_parents.html',{'p':parents})


def view_pendinngparents(request):
    pending=Parent_Reg.objects.filter(status='pending')
    return render(request,'teacher/view_pendingparentslist.html',{'pending':pending})

def parent_details(request,id):
    details=Parent_Reg.objects.filter(id=id)
    return render(request,'teacher/parent_details.html',{'d':details})

def approve_parents(request,id):
     Parent_Reg.objects.filter(id=id).update(status='approved')
     return redirect('view_parents')

def remove_parents(request,id):
    Parent_Reg.objects.filter(id=id).update(status='rejected')
    return redirect('view_parents')



def viewstudentsfor_teachers(request):
    teacher=get_object_or_404(Teacher_Reg,user=request.user)
    students_dataforteachers=Student_Reg.objects.filter(subjects__in=teacher.subjects.all(),status='approved').distinct()
    return render(request,'teacher/view_students.html',{'s':students_dataforteachers})


def schedule_live_class(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    if request.method == "POST":
        subject_id = request.POST['subject']
        class_date = request.POST['date']
        class_time = request.POST['time']
        class_level=request.POST['class_level']
        link = request.POST['link']

        subject = get_object_or_404(Subject, id=subject_id)

        LiveClass.objects.create(
            teacher=teacher,       
            subject=subject,       
            class_date=class_date,
            class_time=class_time,
            meeting_link=link,
            class_level=class_level
        )

        return redirect('teacherhome')

    return render(request, 'teacher/schedule_live_class.html', {
        'subjects': teacher.subjects.all()
    })

def upload_recorded_class(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    if request.method == 'POST':
        subject_id = request.POST['subject']
        title = request.POST['title']
        video = request.FILES['video']
        class_level=request.POST['class_level']

        subject = get_object_or_404(Subject, id=subject_id)

        RecordedClass.objects.create(
            teacher=teacher,   
            subject=subject,        
            title=title,
            video=video,
            class_level=class_level
        )
        return redirect('teacherhome')

    return render(request, 'teacher/upload_recordedclass.html',{'subjects': teacher.subjects.all()})

def upload_notes(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    if request.method == "POST":
        subject_id=request.POST['subject']
        title=request.POST['title']
        file=request.FILES['file']
        class_level=request.POST['class_level']
        subject = get_object_or_404(Subject, id=subject_id)
        Notes.objects.create(
            teacher=teacher,
            subject=subject,
            title=title,
            file=file,
            class_level=class_level
        )
        return redirect('teacherhome')

    return render(request, 'teacher/upload_notes.html',{'subjects': teacher.subjects.all()})


def upload_homework(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)
    if request.method == "POST":
        subject_id =request.POST['subject']
        title=request.POST['title']
        description=request.POST['description']
        file=request.FILES['file']
        due_date=request.POST['due_date']
        class_level=request.POST['class_level']
        subject = get_object_or_404(Subject, id=subject_id)
        Homework.objects.create(
            teacher=teacher,
            subject=subject,
            title=title,
            description=description,
            file=file,
            due_date=due_date,
            class_level=class_level
        )
        return redirect('teacherhome')

    return render(request, 'teacher/upload_homework.html',{'subjects': teacher.subjects.all()})



def view_hw_submissions(request):
    teacher=get_object_or_404(Teacher_Reg,user=request.user)
    hw=HomeworkSubmission.objects.filter(homework__subject__in=teacher.subjects.all()).distinct()
    return render(request,'teacher/view_hw_submissions.html',{'hw_submissions':hw})


def submissionstatus(request,id):
    HomeworkSubmission.objects.filter(id=id).update(status='submitted')
    return redirect('view_hw_submissions')



def mark_attendance(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    selected_subject_id = request.GET.get('subject')
    selected_date = request.GET.get('date', date.today())
    selected_class_level = request.GET.get('class_level') 
    

    students = Student_Reg.objects.none()
    class_levels = range(1, 13)

    if selected_subject_id and selected_class_level:
        subject = get_object_or_404(Subject, id=selected_subject_id)
        students = Student_Reg.objects.filter(subjects=subject, status='approved',class_level=selected_class_level)

     
        for student in students:
            record = Attendance.objects.filter(
                student=student.user,
                teacher=teacher.user,
                subject=subject,
                date=selected_date,
                class_level=selected_class_level
                
            ).first()
            student.attendance_status = record.status if record else 'Not Marked'


    if request.method == 'POST':
        subject = get_object_or_404(Subject, id=request.POST['subject'])
        attendance_date = request.POST['date']
        class_level = request.POST['class_level']
        

        students = Student_Reg.objects.filter(subjects=subject, status='approved',class_level=class_level)

        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')

            Attendance.objects.update_or_create(
                student=student.user,
                teacher=teacher.user,
                subject=subject,
                date=attendance_date,
                defaults={'status': status},
                class_level=class_level
            )

        return redirect(f'/mark_attendance?subject={subject.id}&date={attendance_date}')

    return render(request, 'teacher/mark_attendance.html', {
        'teacher': teacher,
        'students': students,
        'subjects': teacher.subjects.all(),
        'selected_subject_id': selected_subject_id,
        'selected_date': selected_date,
        'selected_class_level': selected_class_level,
        'class_levels': class_levels
        
    })

def view_attendance(request):
    attendance = Attendance.objects.filter(teacher=request.user)

    return render(request, 'teacher/view_attendance.html', {
        'attendance': attendance
    })


def teacher_view_marks(request):
    teacher = get_object_or_404(Teacher_Reg, user=request.user)

    selected_class_level = request.GET.get('class_level')
    selected_subject_id = request.GET.get('subject')

    marks = Mark_marks.objects.filter(
        teacher=teacher
    ).select_related('student', 'subject')

    if selected_class_level:
        marks = marks.filter(class_level=selected_class_level)

    if selected_subject_id:
        marks = marks.filter(subject_id=selected_subject_id)

    class_levels = range(1, 13)
    subjects = teacher.subjects.all()

    return render(request, 'teacher/teacher_view_marks.html', {
        'marks': marks,
        'class_levels': class_levels,
        'subjects': subjects,
        'selected_class_level': selected_class_level,
        'selected_subject_id': selected_subject_id
    })


def teacher_chat(request):
    teacher = Teacher_Reg.objects.get(user=request.user)

    students_with_messages = Student_Reg.objects.filter(
        studentteachermessage__teacher=teacher
    ).distinct()

    student_id = request.GET.get('student')
    selected_student = None
    messages = []

    if student_id:
        selected_student = get_object_or_404(Student_Reg, id=student_id)
        messages = StudentTeacherMessage.objects.filter(
            student=selected_student,
            teacher=teacher
        ).order_by('timestamp')

        messages.filter(sender=selected_student.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student_Reg, id=student_id)

        StudentTeacherMessage.objects.create(
            student=student,
            teacher=teacher,
            sender=request.user,
            content=content
        )
        return redirect(f'/teacher_chat?student={student.id}')

    return render(request, 'teacher/teacher_chat.html', {
        'students': students_with_messages,
        'selected_student': selected_student,
        'messages': messages
    })


def teacher_parent_list(request):
    teacher = Teacher_Reg.objects.get(user=request.user)
    
    parent_ids = ParentTeacherMessage.objects.filter(teacher=teacher).values_list('parent', flat=True).distinct()
    parents = Parent_Reg.objects.filter(id__in=parent_ids)

    return render(request, 'teacher/parent_list.html', {
        'parents': parents
    })


def teacher_parent_chat(request):
    teacher = Teacher_Reg.objects.get(user=request.user)
    parent_id = request.GET.get('parent')

    if not parent_id:
        return redirect('teacher_parent_list')

    parent = get_object_or_404(Parent_Reg, id=parent_id)

    messages = ParentTeacherMessage.objects.filter(
        teacher=teacher,
        parent=parent
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        ParentTeacherMessage.objects.create(
            teacher=teacher,
            parent=parent,
            sender=request.user, 
            content=content
        )
        return redirect(f'/teacher_parent_chat?parent={parent.id}')

    return render(request, 'teacher/teacher_parent_chat.html', {
        'parent': parent,
        'messages': messages
    })


def view_fees_teacher(request):
    teacher = Teacher_Reg.objects.get(user=request.user)

    teacher_subjects = teacher.subjects.all()

    students = Student_Reg.objects.filter(
        subjects__in=teacher_subjects
    ).distinct()

    
    fees = Fee.objects.filter(
        student__in=students
    ).select_related('student').order_by('-due_date')

    return render(request, 'teacher/view_fees_teacher.html', {
        'fees': fees
    })


def teacher_my_salary(request):
    teacher = Teacher_Reg.objects.get(user=request.user)

    salaries = TeacherSalary.objects.filter(
        teacher=teacher,
        status='paid'
    ).order_by('-paid_date')

    return render(request, 'teacher/my_salary.html', {
        'salaries': salaries
    })

def teachers_attendance(request):
    teacher = Teacher_Reg.objects.get(user=request.user)

  
    selected_month = request.GET.get('month')

    attendance = TeacherAttendance.objects.filter(teacher=teacher)

    if selected_month:
        year, month = selected_month.split('-')
        attendance = attendance.filter(
            date__year=year,
            date__month=month
        )

    attendance = attendance.order_by('-date')

    return render(request, 'teacher/view_my_attendance.html', {
        'attendance': attendance,
        'selected_month': selected_month
    })

def teacher_view_reviews(request):
    reviews = ReviewRemark.objects.filter(
        review__isnull=False     
    ).select_related('student', 'created_by')\
     .order_by('-created_at')

    return render(request, 'teacher/view_reviews.html', {
        'reviews': reviews
    })

def teacher_review_status(request, id):
    review = get_object_or_404(ReviewRemark, id=id)

    if review.review_status == 'approved':
        return redirect('teacher_view_reviews')

    if request.method == 'POST':
        review.review_status = request.POST.get('review_status')
        review.save()
    return redirect('teacher_view_reviews')



