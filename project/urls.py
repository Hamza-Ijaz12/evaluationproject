from django.urls import path
from . import views

urlpatterns = [
    # COhorts
    path('create_class', views.create_class, name='create_class'), 
    path('update_class/<str:pk>/', views.update_cohort, name='update_class'), 
    path('delete_cohort/<str:pk>/', views.delete_cohort, name='delete_cohort'), 
    path('assign_cohort/<str:pk>/', views.assign_cohort, name='assign_cohort'), 
    path('cohort_details/<str:pk>/', views.cohortdetails, name='cohort_details'), 
    path('cohorts_list', views.cohortlist, name='cohorts_list'), 

    # Lesson
    path('lessoncreate/<str:pk>/', views.lessoncreate, name='lessoncreate'), 
    path('lessondelete/<str:pk>/', views.lessondelete, name='lessondelete'), 
    path('lessonedit/<str:pk>/', views.lessonupdate, name='lessonedit'), 
    path('lesson_details/<str:pk>/', views.lesson_details, name='lesson_details'), 
    # Tasks
    path('task_list/', views.task_list, name='task_list'),
    path('task_edit/<str:pk>/', views.taskedit, name='task_edit'),
    path('delete_task', views.taskdelete, name='delete_task'),
    path('assign_task1/<str:pk>/', views.taskassignre, name='assign_task1'),
    path('assign_task/<str:pk>/', views.taskassign, name='assign_task'),


    path('task_type1_create/<str:pk>/', views.t1create, name='task_type1_create'), 
    path('task_type1_update/<str:pk>/', views.t1update, name='task1_update'), 

    path('task_type2_create/<str:pk>/', views.t2create, name='task_type2_create'), 
    path('task_type2_update/<str:pk>/', views.t2update, name='task2_update'), 

    path('task_type3_create/<str:pk>/', views.t3create, name='task_type3_create'), 
    path('task_type3_update/<str:pk>/', views.t3update, name='task3_update'),  

    path('task_type4_create/<str:pk>/', views.t4create, name='task_type4_create'),
    path('task_type4_update/<str:pk>/', views.t4update, name='task4_update'), 

    path('task_type5_create/<str:pk>/', views.t5create, name='task_type5_create'),
    path('task_type5_update/<str:pk>/', views.t5update, name='task5_update'), 

    path('task_type6_create/<str:pk>/', views.t6create, name='task_type6_create'),
    path('task_type6_update/<str:pk>/', views.t6update, name='task6_update'), 

    path('task_type7_update/<str:pk>/', views.t7update, name='task7_update'), 
    path('fill_blanks_create/<str:pk>/', views.t7create, name='fill_blanks_create'),

    path('spell_correct_create/<str:pk>/', views.t8create, name='spell_correct_create'), 
    path('task_type8_update/<str:pk>/', views.t8update, name='task8_update'), 

    path('speechQuestion_create/<str:pk>/', views.speechQuestioncreate, name='speechQuestion_create'), 
    path('task_typespeechQuestion_update/<str:pk>/', views.speechQuestionupdate, name='speechQuestion'), 

    path('result/<str:pk>/', views.result, name='result'), 
    
    #Added by Hamza 7-2-24 
    # Teacher task Preview part
    path('preview/<str:pk>/', views.preview, name='preview'),

     path('task_type1_preview/<str:pk>/', views.t1preview, name='task1_preview'), 
     path('task_type2_preview/<str:pk>/', views.t2preview, name='task2_preview'), 
     path('task_type3_preview/<str:pk>/', views.t3preview, name='task3_preview'), 
     path('task_type4_preview/<str:pk>/', views.t4preview, name='task4_preview'), 
     path('task_type5_preview/<str:pk>/', views.t5preview, name='task5_preview'), 
     path('task_type6_preview/<str:pk>/', views.t6preview, name='task6_preview'), 
     path('task_type7_preview/<str:pk>/', views.t7preview, name='task7_preview'), 
     path('task_type8_preview/<str:pk>/', views.t8preview, name='task8_preview'),
    #  Add speech question here for preview and also add template for ita dn update the preview view function 
    #Added by Hamza 7-2-24
     
    # Student part starts
    path('attempt/<str:pk>/', views.attempt, name='attempt'), 

    path('task_type1_attempt/<str:pk>/', views.t1attempt, name='task1_attempt'), 
    path('task_type2_attempt/<str:pk>/', views.t2attempt, name='task2_attempt'), 
    path('task_type3_attempt/<str:pk>/', views.t3attempt, name='task3_attempt'), 
    path('task_type4_attempt/<str:pk>/', views.t4attempt, name='task4_attempt'), 
    path('task_type5_attempt/<str:pk>/', views.t5attempt, name='task5_attempt'), 
    path('task_type6_attempt/<str:pk>/', views.t6attempt, name='task6_attempt'), 
    path('task_type7_attempt/<str:pk>/', views.t7attempt, name='task7_attempt'), 
    path('task_type8_attempt/<str:pk>/', views.t8attempt, name='task8_attempt'), 

    path('task5ajax/', views.t5ajax, name='task5ajax'), 
    path('task_typespeechQuestion_attempt/<str:pk>/', views.speechQuestionattempt, name='speechQuestion_attempt'), 

#Added by Hamza 7-2-24
    # Question Attempt auto
    path('qeustion_attempt/<str:pk>/', views.que_attempt, name='qeustion_attempt'), 
#Added by Hamza 7-2-24

    # Other URL patterns...
    path('questionsRGB', views.questionsRGB, name='questionsRGB'), 
    path('red', views.red, name='red'), 
    path('upload_audio_speech/', views.upload_audio_speech, name='upload_audio_speech'),
]
