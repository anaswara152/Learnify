from django.shortcuts import render,redirect,get_object_or_404
from Teacher.models import Teacher_Reg
from Student.models import Student_Reg
from Parent.models import Payment,Notification
from .models import *
from datetime import date
from django.contrib import messages
from django.db.models.functions import TruncMonth
from Common.models import ReviewRemark



# Create your views here.
def adminhome(request):
    return render(request,'admin/admin_home.html')


def viewteachers(request):
    teacher=Teacher_Reg.objects.filter(status='approved')
    return render(request,'admin/view_teachers.html',{'t':teacher})


def blockedteachers(request):
    teachers=Teacher_Reg.objects.filter(status='blocked')
    return render(request,'admin/blocked_teachers.html',{'teacher':teachers})

def approve_teachers(request,id):
     Teacher_Reg.objects.filter(id=id).update(status='approved')
     
     return redirect('viewteachers')

def reject_teachers(request,id):
    Teacher_Reg.objects.filter(id=id).update(status='rejected')
    return redirect('viewpendingteachers')


def block_teachers(request,id):
    Teacher_Reg.objects.filter(id=id).update(status='blocked')
    return redirect('viewteachers')

def unblock_teachers(request,id):
    Teacher_Reg.objects.filter(id=id).update(status='approved')
    return redirect('viewteachers')


def viewpendingteachers(request):
    pending=Teacher_Reg.objects.filter(status='pending')
    return render(request,'admin/pending_teachers.html',{'p':pending})


def teacher_deatils(request,id):
    details=Teacher_Reg.objects.filter(id=id)
    return render(request,'admin/teacher_details.html',{'d':details})


def add_fee(request):
    students = Student_Reg.objects.filter(status='approved').prefetch_related('subjects')


    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        amount_due = request.POST.get('amount_due')
        due_date = request.POST.get('due_date')

        if not student_id or not subject_id:
            messages.error(request, "Please select student and subject.")
            return redirect('add_fee')

        student = get_object_or_404(Student_Reg, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)

        if Fee.objects.filter(student=student, subject=subject).exists():
            messages.error(request, "Fee already added for this subject.")
            return redirect('add_fee')

        Fee.objects.create(
            student=student,
            subject=subject,
            amount_due=float(amount_due),
            due_date=due_date,
        )

        Notification.objects.create(
            user=student.parent.user,
            message=f"New fee of ₹{amount_due} added for {student.user.first_name} - {subject.subjectname}. Due date: {due_date}"
        )

        Notification.objects.create(
            user=student.user,
            message=f"A new fee of ₹{amount_due} has been added for {subject.subjectname}. Due date: {due_date}"
        )

        messages.success(request, "Subject fee added successfully.")
        return redirect('view_fees_admin')

    return render(request, 'admin/add_fee.html', {
        'students': students,
        
    })

def view_fees_admin(request):
    fees = Fee.objects.select_related('student', 'subject').order_by('-due_date')
    return render(request, 'admin/view_fees_admin.html', {'fees': fees})



def view_bloked_students(request):
    fees = Fee.objects.filter(status='unpaid').select_related('student', 'subject')
    return render(request, 'admin/unpaid_students.html', {'f': fees})


def block_students(request,id):
    student = get_object_or_404(Student_Reg, id=id)
    student.status = 'blocked'
    student.save()

    Notification.objects.create(
        user=student.parent.user,
        message=f"Your child {student.user.first_name} has been blocked due to unpaid fee."
    )

    Notification.objects.create(
        user=student.user,
        message="Your account has been blocked due to unpaid fee. Please inform your parent."
    )
    return redirect('view_bloked_students')

def unblock_students(request,id):
    student = get_object_or_404(Student_Reg, id=id)
    student.status = 'approved'
    student.save()

    Notification.objects.create(
        user=student.parent.user,
        message=f"Your child {student.user.first_name} has been unblocked."
    )

    Notification.objects.create(
        user=student.user,
        message="Your account has been unblocked. You can continue your classes."
    )
    return  redirect('view_bloked_students')

def edit_fee(request, id):
    fee = get_object_or_404(Fee, id=id)
    if request.method == 'POST':
        fee.amount_due = float(request.POST['amount_due'])
        fee.due_date = request.POST['due_date']
        fee.save()
        return redirect('view_fees_admin')

    return render(request, 'admin/edit_fee.html', {'fee': fee})




def delete_fee(request, id):
    fee = get_object_or_404(Fee, id=id)
    fee.delete()
    return redirect('view_fees_admin')



def view_paid_fees_admin(request):
    selected_month = request.GET.get('month')

    payments = Payment.objects.select_related(
        'student',
        'parent',
        'fee'
    ).filter(
        fee__status='paid'
    )

    if selected_month:
        payments = payments.filter(
            payment_date__month=selected_month
        )

    payments = payments.order_by('-payment_date')

    months = Payment.objects.filter(
        fee__status='paid'
    ).annotate(
        month=TruncMonth('payment_date')
    ).values('month').distinct().order_by('-month')

    return render(request, 'admin/view_paid_fees_admin.html', {
        'payments': payments,
        'months': months,
        'selected_month': selected_month
    })


def add_teacher_salary(request):
    teachers = Teacher_Reg.objects.filter(status='approved')

    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        month = request.POST['month']

        teacher = Teacher_Reg.objects.get(id=teacher_id)

        
        if TeacherSalary.objects.filter(
            teacher=teacher,
            month=month
        ).exists():
            messages.error(
                request,
                f"Salary already paid for {teacher.user.first_name} - {month}"
            )
            return redirect('add_teacher_salary')

        TeacherSalary.objects.create(
            teacher=teacher,
            month=month,
            amount=request.POST['amount'],
            payment_mode=request.POST['payment_mode'],
            account_holder_name=request.POST['account_holder_name'],
            account_number=request.POST['account_number'],
            transaction_id=request.POST['transaction_id'],
            status='paid'
        )

        messages.success(request, "Salary paid successfully")
        return redirect('view_teacher_salary_admin')

    return render(request, 'admin/add_teacher_salary.html', {
        'teachers': teachers
    })



def view_teacher_salary_admin(request):
    salaries = TeacherSalary.objects.select_related('teacher').order_by('-created_at')
    return render(request, 'admin/view_teacher_salary.html', {
        'salaries': salaries
    })



def mark_teacher_attendance(request):
    teachers = Teacher_Reg.objects.filter(status='approved')

    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = date.fromisoformat(selected_date)
    else:
        selected_date = date.today()

    attendance_qs = TeacherAttendance.objects.filter(date=selected_date)
    attendance_dict = {
        att.teacher_id: att.status
        for att in attendance_qs
    }

    for teacher in teachers:
        teacher.today_status = attendance_dict.get(teacher.id)

    if request.method == 'POST':
        selected_date = date.fromisoformat(request.POST['date'])

        for teacher in teachers:
            status = request.POST.get(f'status_{teacher.id}')
            if status:
                TeacherAttendance.objects.update_or_create(
                    teacher=teacher,
                    date=selected_date,
                    defaults={'status': status}
                )
        return redirect(f'/mark_teacher_attendance?date={selected_date}')

    return render(request, 'admin/mark_teacher_attendance.html', {
        'teachers': teachers,
        'selected_date': selected_date
    })

def admin_view_reviews_remarks(request):
    records = ReviewRemark.objects.select_related(
        'student',
        'created_by'
    ).order_by('-created_at')

    return render(request, 'admin/admin_view_reviews_remarks.html', {
        'records': records
    })

def admin_update_review_remark(request, id):
    record = get_object_or_404(ReviewRemark, id=id)

    if record.review_status == 'approved' and record.remark_status == 'approved':
        messages.error(request, "This review is already finalized.")
        return redirect('admin_view_reviews_remarks')

    if request.method == 'POST':
        record.review_status = request.POST.get('review_status')
        record.remark_status = request.POST.get('remark_status')
        record.save()

    return redirect('admin_view_reviews_remarks')