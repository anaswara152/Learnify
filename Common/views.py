from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib import messages
from Teacher.models import Teacher_Reg
from Parent.models import Parent_Reg
from Student.models import Student_Reg
from .models import*

# Create your views here.


def home(request):
    tutors = Teacher_Reg.objects.filter(status='approved')
    return render(request, 'common/home.html', {
        'tutors': tutors
    })


def login_users(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="TEACHER").exists():
            return redirect('teacherhome')
        elif request.user.groups.filter(name="PARENTS").exists():
            return redirect('parenthome')
        elif request.user.groups.filter(name="STUDENT").exists():
            return redirect('studenthome')
        else:  
            return redirect('adminhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
           
            if user.groups.filter(name="TEACHER").exists():
                teacher = Teacher_Reg.objects.get(user=user)
                if teacher.status == "pending":
                    messages.error(request, "Your account is not approved yet!")
                    return redirect('login_users')
                if teacher.status =='blocked':
                    messages.error(request,'Your account is blocked')
                    return redirect('login_users')
                if teacher.status =='rejected':
                    messages.error(request,'Your account is removed ')
                    return redirect('login_users')
                login(request, user)
                return redirect('teacherhome')

            elif user.groups.filter(name="PARENTS").exists():
                parents = Parent_Reg.objects.get(user=user)
                if parents.status == "pending":
                    messages.error(request, "Your account is not approved yet!")
                    return redirect('login_users')
                elif parents.status=='blocked':
                    messages.error(request,'Your account is blocked by admin')
                    return redirect('login_users')
                elif parents.status == 'rejected':
                    messages.error(request, "Your account is Removed!")
                    return redirect('login_users')
                login(request, user)
                return redirect('parenthome')

            elif user.groups.filter(name="STUDENT").exists():
                student = Student_Reg.objects.get(user=user)
                if student.status == 'blocked':
                        messages.error(
                            request,
                            "Your account blocked by admin please pay the fees"
                        )
                        return redirect('login_users')
                elif student.status == "pending":
                    messages.error(request, "Your account is not approved yet!")
                    return redirect('login_users')
                elif student.status == 'removed':
                    messages.error(request,'Your account removed')
                    return redirect('login_users')
                login(request, user)
                return redirect('studenthome')

            else:  
                login(request, user)
                return redirect('adminhome')
        else:
            messages.error(request, "User credentials are not correct")
            return redirect('login_users')

    return render(request, 'common/login.html')

def logoutuser(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('home')



def forgot_password_for_all(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('forgot_password_for_all')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please login.")
            return redirect('login_users')
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('forgot_password_for_all')

    return render(request, 'common/forgot_password.html')