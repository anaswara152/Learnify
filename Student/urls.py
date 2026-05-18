from django.urls import path
from Student import views

urlpatterns=[
    path('student_register',views.student_register,name='student_register'),
    path('studenthome',views.studenthome,name='studenthome'),
    path('student_live_classes',views.student_live_classes,name='student_live_classes'),
    path('view_recorded_classes',views.view_recorded_classes,name='view_recorded_classes'),
    path('View_notes',views.View_notes,name='View_notes'),
    path('view_homeworks',views.view_homeworks,name='view_homeworks'),
    path('submit_homework/<int:id>',views.submit_homework,name='submit_homework'),
    path('view_attendance_for_student',views.view_attendance_for_students,name='view_attendance_for_students'),
    path('student_view_marks',views.student_view_marks,name='student_view_marks'),
    path('student_teacher_chat',views.student_teacher_chat,name='student_teacher_chat'),
    path('start_chat',views.start_chat,name='start_chat'),
    path('select_teacher',views.select_teacher,name='select_teacher'),
    path('student_fees',views.student_fees,name='student_fees'),
    path('student_add_review',views.student_add_review,name='student_add_review'),
    path('student_view_review_remark',views.student_view_review_remark,name='student_view_review_remark'),
    path('student_notifications',views.student_notifications,name='student_notifications')
]