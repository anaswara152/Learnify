from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.contrib import messages
from django.contrib.auth.models import User,Group
from Student.models import Student_Reg
from Teacher.models import Attendance
from SiteAdmin.models import Fee
from Common.models import ReviewRemark
# Create your views here.
def parenthome(request):
   return render(request,'parent/parent_home.html')

def parents_register(request):
    if request.method =='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        address=request.POST['address']
        phone=request.POST['phone']
        occupation =request.POST['occupation']
        gender=request.POST['gender']
        if User.objects.filter(username=username).exists():
           messages.error(request, "Username already exists!")
           return redirect('parents_register')
        if User.objects.filter(email=email).exists():
          messages.error(request, "Email already exists!")
          return redirect('parents_register')
        puser=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        puser.save()
        parents=Parent_Reg.objects.create(user=puser,address=address,phone=phone,occupation=occupation,gender=gender)
        parents.save()
        parents_obj,created=Group.objects.get_or_create(name='PARENTS')
        parents_obj.user_set.add(puser)
        messages.success(request,'Registration successfull')
    return render(request,'common/parents_registration.html')    



def viewstudentsfor_parents(request):
   parent=get_object_or_404(Parent_Reg,user=request.user)
   student=Student_Reg.objects.filter(parent_id=parent)
   return render(request,'parent/view_student.html',{'s':student})



def approve_student(request,id):
     Student_Reg.objects.filter(id=id).update(status='approved')
     return redirect('viewstudentsfor_parents')

def remove_students(request,id):
    Student_Reg.objects.filter(id=id).update(status='removed')
    return redirect('viewstudentsfor_parents')

def view_students_attendance(request):
    parent = get_object_or_404(Parent_Reg, user=request.user)
    students = Student_Reg.objects.filter(parent_id=parent, status='approved')
    selected_student_id = request.GET.get('student')
    attendance_data = []
    if selected_student_id:
        student = get_object_or_404(Student_Reg,id=selected_student_id,parent_id=parent)
        records = Attendance.objects.filter(student=student.user)
        attendance_data.append({'student': student,'records': records})
    return render(request, 'parent/view_attendance.html', {
        'students': students,
        'attendance_data': attendance_data,
        'selected_student_id': selected_student_id
    })





def enter_marks(request):
    parent = Parent_Reg.objects.get(user=request.user)
    subjects = Subject.objects.all()

    selected_subject_id = request.GET.get('subject')
    selected_class_level = request.GET.get('class_level')

    students = Student_Reg.objects.none()
    class_levels = range(1, 13)

    if selected_subject_id and selected_class_level:
        students = Student_Reg.objects.filter(
            parent=parent,
            status='approved',
            class_level=selected_class_level
        )

    if request.method == 'POST':
        subject = Subject.objects.get(id=request.POST['subject'])
        class_level = request.POST['class_level']
        total_marks = request.POST['total_marks']

        teacher = Teacher_Reg.objects.filter(
            subjects=subject,
            status='approved'
        ).first()   

        for key, value in request.POST.items():
            if key.startswith('marks_'):
                student_id = key.split('_')[1]
                student = Student_Reg.objects.get(id=student_id)

                Mark_marks.objects.create(
                    student=student,
                    parent=parent,
                    teacher=teacher,   
                    subject=subject,
                    marks_obtained=value,
                    total_marks=total_marks,
                    class_level=class_level
                )
                messages.success(request,'Added')

        return redirect('view_marks')

    return render(request, 'parent/enter_marks.html', {
        'subjects': subjects,
        'students': students,
        'selected_subject_id': selected_subject_id,
        'selected_class_level': selected_class_level,
        'class_levels': class_levels
    })


def view_marks(request):
    parent = get_object_or_404(Parent_Reg, user=request.user)

    marks = Mark_marks.objects.filter(parent=parent).select_related(
        'student__user', 'subject'
    )

    return render(request, 'parent/view_marks.html', {
        'marks': marks
    })


def parent_edit_marks(request, id):
    parent = get_object_or_404(Parent_Reg, user=request.user)

    mark = get_object_or_404(
        Mark_marks,
        id=id,
        parent=parent   
    )

    if request.method == 'POST':
        mark.marks_obtained = request.POST['marks_obtained']
        mark.total_marks = request.POST['total_marks']
        mark.save()
        messages.success(request,'updated successfully..')
        return redirect('view_marks')

    return render(request, 'parent/edit_marks.html', {
        'mark': mark
    })


def parent_delete_marks(request, id):
    parent = get_object_or_404(Parent_Reg, user=request.user)

    mark = get_object_or_404(
        Mark_marks,
        id=id,
        parent=parent   
    )

    mark.delete()
    return redirect('view_marks')



def parent_select_teacher(request):
    parent = Parent_Reg.objects.get(user=request.user)
    
 
    children = Student_Reg.objects.filter(parent=parent)
    subjects = Subject.objects.filter(student_reg__in=children).distinct()
    teachers = Teacher_Reg.objects.filter(subjects__in=subjects, status='approved').distinct()

    return render(request, 'parent/parent_select_teacher.html', {
        'teachers': teachers
    })


def parent_teacher_chat(request):
    parent = Parent_Reg.objects.get(user=request.user)
    teacher_id = request.GET.get('teacher')

    if not teacher_id:
        return redirect('parent_select_teacher')  

    teacher = get_object_or_404(Teacher_Reg, id=teacher_id)

    messages = ParentTeacherMessage.objects.filter(
        parent=parent,
        teacher=teacher
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        ParentTeacherMessage.objects.create(
            parent=parent,
            teacher=teacher,
            sender=request.user,
            content=content
        )
        return redirect(f'/parent_teacher_chat?teacher={teacher.id}')

    return render(request, 'parent/parent_teacher_chat.html', {
        'teacher': teacher,
        'messages': messages
    })




def view_child_fees(request):
    parent = Parent_Reg.objects.get(user=request.user)
    students = Student_Reg.objects.filter(parent=parent)
    fees = Fee.objects.filter(student__in=students)

    return render(request, 'parent/parent_fees.html', {'fees': fees})


def pay_fee(request, id):
    fee = get_object_or_404(Fee, id=id)
    parent = Parent_Reg.objects.get(user=request.user)
    student = fee.student
    if request.method == 'POST':
        card_holder_name = request.POST.get('card_holder_name')
        card_number = request.POST.get('card_number')
        amount = request.POST.get('amount')

        Payment.objects.create(
            parent=parent,
            student=fee.student,
            fee=fee,
            amount_paid=amount,
            card_holder_name=card_holder_name,
            card_number=card_number
        )

        fee.status = 'paid'
        fee.save()
        messages.success(request,'payment successfull..')
        Notification.objects.create(
            user=parent.user,
            message=f"Fee payment of ₹{amount} for {student.user.first_name} was successful."
        )

        Notification.objects.create(
            user=student.user,
            message=f"Your fee of ₹{amount} has been paid by your parent."
        )

        return redirect('view_child_fees')


        

    return render(request, 'parent/pay_fee.html', {'fee': fee})


def parent_add_remark(request):
    parent = Parent_Reg.objects.get(user=request.user)
    students = Student_Reg.objects.filter(parent=parent)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        remark = request.POST.get('remark')

        student = Student_Reg.objects.get(id=student_id) 

        ReviewRemark.objects.create(
            created_by=request.user,
            student=student,         
            remark=remark,
            remark_status='pending'
        )
        return redirect('parenthome')

    return render(request, 'parent/add_remark.html', {
        'students': students
    })

def parent_view_reviews_remarks(request):
    parent = Parent_Reg.objects.get(user=request.user)

    students = Student_Reg.objects.filter(parent=parent)

    records = ReviewRemark.objects.filter(
        student__in=students
    ).select_related('student').order_by('-created_at')

    return render(request, 'parent/parent_view_reviews_remarks.html', {
        'records': records
    })



def parent_notifications(request):
    notes = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'parent/notifications.html', {'notes': notes})