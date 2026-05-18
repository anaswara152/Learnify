from django.urls import path
from Teacher import views

urlpatterns=[
    path('teacher_register',views.teacher_register,name='teacher_register'),
    path('teacher_profile',views.teacher_profile,name='teacher_profile'),
    path('edit_teacher_profile',views.edit_teacher_profile,name='edit_teacher_profile'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('view_parents',views.view_parents,name='view_parents'),
    path('approve_parents/<int:id>',views.approve_parents,name='approve_parents'),
    path('remove_parents/<int:id>',views.remove_parents,name='remove_parents'),
    path('viewstudentsfor_teachers',views.viewstudentsfor_teachers,name='viewstudentsfor_teachers'),
    path('schedule_live_class',views.schedule_live_class,name='schedule_live_class'),
    path('upload_recorded_class',views.upload_recorded_class,name='upload_recorded_class'),
    path('upload_notes',views.upload_notes,name='upload_notes'),
    path('upload_homework',views.upload_homework,name='upload_homework'),
    path('view_hw_submissions',views.view_hw_submissions,name='view_hw_submissions'),
    path('submissionstatus/<int:id>',views.submissionstatus,name='submissionstatus'),
    path('mark_attendance',views.mark_attendance,name='mark_attendance'),
    path('view_attendance',views.view_attendance,name='view_attendance'),
    path('view_pendinngparents',views.view_pendinngparents,name='view_pendinngparents'),
    path('parent_details/<int:id>',views.parent_details,name='parent_details'),
    path('teacher_view_marks',views.teacher_view_marks,name='teacher_view_marks'),
    path('teacher_chat',views.teacher_chat,name='teacher_chat'),
    path('teacher_parent_list',views.teacher_parent_list,name='teacher_parent_list'),
    path('teacher_parent_chat',views.teacher_parent_chat,name='teacher_parent_chat'),
    path('view_fees_teacher',views.view_fees_teacher,name='view_fees_teacher'),
    path('teacher_my_salary',views.teacher_my_salary,name='teacher_my_salary'),
    path('teachers_attendance',views.teachers_attendance,name='teachers_attendance'),
    path('teacher_view_reviews',views.teacher_view_reviews,name='teacher_view_reviews'),
    path('teacher_review_status/<int:id>',views.teacher_review_status,name='teacher_review_status')

]

