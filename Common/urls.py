from django.urls import path
from Common import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login_users',views.login_users,name='login_users'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('forgot_password_for_all',views.forgot_password_for_all,name='forgot_password_for_all')

]