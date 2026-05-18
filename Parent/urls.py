from django.urls import path
from Parent import views

urlpatterns=[
    path('parents_register',views.parents_register,name='parents_register'),
    path('parenthome',views.parenthome,name='parenthome'),
    path('viewstudentsfor_parents',views.viewstudentsfor_parents,name='viewstudentsfor_parents'),
    path('approve_student/<int:id>',views.approve_student,name='approve_student'),
    path('remove_students/<int:id>',views.remove_students,name='remove_students'),
    path('view_students_attendance',views.view_students_attendance,name='view_students_attendance'),
    path('enter_marks',views.enter_marks,name='enter_marks'),
    path('view_marks',views.view_marks,name='view_marks'),
    path('parent_edit_marks/<int:id>',views.parent_edit_marks,name='parent_edit_marks'),
    path('parent_delete_marks/<int:id>',views.parent_delete_marks,name='parent_delete_marks'),
    path('parent_teacher_chat',views.parent_teacher_chat,name='parent_teacher_chat'),
    path('parent_select_teacher',views.parent_select_teacher,name='parent_select_teacher'),
    path('view_child_fees',views.view_child_fees,name='view_child_fees'),
    path('pay_fee/<int:id>',views.pay_fee,name='pay_fee'),
    path('parent_add_remark',views.parent_add_remark,name='parent_add_remark'),
    path('parent_view_reviews_remarks',views.parent_view_reviews_remarks,name='parent_view_reviews_remarks'),
    path('parent_notifications',views.parent_notifications,name='parent_notifications')

]