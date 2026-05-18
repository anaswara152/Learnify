from django.urls import path
from SiteAdmin import views

urlpatterns=[
    path('adminhome',views.adminhome,name='adminhome'),
    path('viewteachers',views.viewteachers,name='viewteachers'),
    path('approve_teachers/<int:id>',views.approve_teachers,name='approve_teachers'),
    path('reject_teachers/<int:id>',views.reject_teachers,name='reject_teachers'),
    path('block_teachers/<int:id>',views.block_teachers,name='block_teachers'),
    path('viewpendingteachers',views.viewpendingteachers,name='viewpendingteachers'),
    path('teacher_deatils/<int:id>',views.teacher_deatils,name='teacher_deatils'),
    path('unblock_teachers/<int:id>',views.unblock_teachers,name='unblock_teachers'),
    path('add_fee',views.add_fee,name='add_fee'),
    path('view_fees_admin',views.view_fees_admin,name='view_fees_admin'),
    path('edit_fee/<int:id>',views.edit_fee,name='edit_fee'),
    path('delete_fee/<int:id>',views.delete_fee,name='delete_fee'),
    path('view_paid_fees_admin',views.view_paid_fees_admin,name='view_paid_fees_admin'),
    path('add_teacher_salary',views.add_teacher_salary,name='add_teacher_salary')    ,
    path('view_teacher_salary_admin',views.view_teacher_salary_admin,name='view_teacher_salary_admin'),
    path('blockedteachers',views.blockedteachers,name='blockedteachers'),
    path('block_students/<int:id>',views.block_students,name='block_students'),
    path('view_bloked_students',views.view_bloked_students,name='view_bloked_students'),
    path('unblock_students/<int:id>',views.unblock_students,name='unblock_students'),
    path('mark_teacher_attendance',views.mark_teacher_attendance,name='mark_teacher_attendance'),
    path('admin_view_reviews_remarks',views.admin_view_reviews_remarks,name='admin_view_reviews_remarks'),
    path('admin_update_review_remark/<int:id>',views.admin_update_review_remark,name='admin_update_review_remark')
]