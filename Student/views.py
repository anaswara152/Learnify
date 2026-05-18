from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.contrib import messages
from django.contrib.auth.models import User,Group
from SiteAdmin.models import Subject,Fee
from Parent.models import Parent_Reg,Mark_marks,Notification
from Teacher.models import*
from Common.models import ReviewRemark

# Create your views here.
def studenthome(request):
   return render(request,'student/student_home.html')

def student_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        parent_username = request.POST['parent_name']
        class_level = request.POST['class_level']
        gender = request.POST['gender']
        subjects = request.POST.getlist('subjects')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Student username already exists!")
            return redirect('student_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('student_register')

        try:
            parent = Parent_Reg.objects.get(user__username=parent_username)
        except Parent_Reg.DoesNotExist:
            messages.error(request, "Parent does not exist!")
            return redirect('student_register')

        suser = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        student = Student_Reg.objects.create(
            user=suser,
            parent=parent,
            class_level=class_level,
            gender=gender
        )

        student.subjects.set(subjects)

        group, created = Group.objects.get_or_create(name='STUDENT')
        group.user_set.add(suser)

        messages.success(request, "Registration successful!")
        return redirect('student_register')

    s = Subject.objects.all()
    return render(request, 'common/student_registration.html', {'subject': s})


def student_live_classes(request):
    student = get_object_or_404(Student_Reg, user=request.user)
    classes = LiveClass.objects.filter(class_level=student.class_level)
    return render(request, 'student/live_classes.html', {'classes': classes})


def view_recorded_classes(request):
    student = get_object_or_404(Student_Reg, user=request.user)

    classes = RecordedClass.objects.filter(class_level=student.class_level)
    return render(request, 'student/view_recordedclass.html', {'classes': classes})

def View_notes(request):
    student = get_object_or_404(Student_Reg, user=request.user)

    notes = Notes.objects.filter(class_level=student.class_level)
    return render(request, 'student/viewnotes.html', {'notes': notes})

def view_homeworks(request):
    student = get_object_or_404(Student_Reg, user=request.user)
    homeworks = Homework.objects.filter(class_level=student.class_level)
    return render(request, 'student/view_homeworks.html', {'homeworks': homeworks})

def submit_homework(request, id):
    homework = Homework.objects.get(id=id)

    if request.method == "POST":
        HomeworkSubmission.objects.create(
            homework=homework,
            student=request.user,
            answer_file=request.FILES['answer']
        )
        return redirect('view_homeworks')

    return render(request, 'student/submit_homework.html', {'homework': homework})

def view_attendance_for_students(request):
    student = get_object_or_404(Student_Reg, user=request.user)
    subjects = student.subjects.all()  

    selected_subject_id = request.GET.get('subject')
    attendance_records = []

    if selected_subject_id:
        subject = get_object_or_404(Subject, id=selected_subject_id)
        attendance_records = Attendance.objects.filter(
            student=student.user,
            subject=subject
        ).order_by('date')

    return render(request, 'student/view_attendance.html', { 'subjects': subjects,
        'selected_subject_id': selected_subject_id,
        'attendance_records': attendance_records})

def student_view_marks(request):
    student = get_object_or_404(Student_Reg, user=request.user)


    marks = Mark_marks.objects.filter(student=student).select_related('subject', 'teacher', 'parent')

    return render(request, 'student/student_view_marks.html', {
        'marks': marks
    })


def select_teacher(request):
    student = Student_Reg.objects.get(user=request.user)
    teachers = Teacher_Reg.objects.filter(subjects__in=student.subjects.all(), status='approved').distinct()
    return render(request, 'student/select_teacher.html', {'teachers': teachers})

def student_teacher_chat(request):
    student = Student_Reg.objects.get(user=request.user)
    teacher_id = request.session.get('chat_teacher_id')

    if not teacher_id:
        return redirect('select_teacher')

    teacher = Teacher_Reg.objects.get(id=teacher_id)
    messages = StudentTeacherMessage.objects.filter(student=student, teacher=teacher).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            StudentTeacherMessage.objects.create(
                student=student,
                teacher=teacher,
                sender=request.user,
                content=content
            )
        return redirect('student_teacher_chat')

    return render(request, 'student/chat.html', {'messages': messages, 'teacher': teacher})

def start_chat(request):
    teacher_id = request.GET.get('teacher')
    request.session['chat_teacher_id'] = teacher_id
    return redirect('student_teacher_chat')



def student_fees(request):
    student = Student_Reg.objects.get(user=request.user)
    fees = Fee.objects.filter(student=student).order_by('-due_date')
    return render(request, 'student/student_fees.html', {'fees': fees})

def student_add_review(request):
    student = Student_Reg.objects.get(user=request.user)

    if request.method == 'POST':
        ReviewRemark.objects.create(
            created_by=request.user,
            student=student,   
            review=request.POST.get('review'),
            remark=request.POST.get('remark'),
            review_status='pending'
        )
        return redirect('studenthome')

    return render(request, 'student/add_review.html')

def student_view_review_remark(request):
    student = Student_Reg.objects.get(user=request.user)

    records = ReviewRemark.objects.filter(
        student=student
    ).order_by('-created_at')

    return render(request, 'student/view_review_remark.html', {
        'records': records
    })


def student_notifications(request):
    notes = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'student/notifications.html', {'notes': notes})