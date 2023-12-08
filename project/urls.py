from django.urls import path
from . import views

urlpatterns = [
    path('create_class', views.create_class, name='create_class'), 
    path('update_class/<str:pk>/', views.update_cohort, name='update_class'), 
    path('delete_cohort/<str:pk>/', views.delete_cohort, name='delete_cohort'), 
    path('assign_cohort/<str:pk>/', views.assign_cohort, name='assign_cohort'), 
    path('cohort_details/<str:pk>/', views.cohortdetails, name='cohort_details'), 
    # Lesson
    path('lessoncreate/<str:pk>/', views.lessoncreate, name='lessoncreate'), 
    path('lessondelete/<str:pk>/', views.lessondelete, name='lessondelete'), 
    path('lessonedit/<str:pk>/', views.lessonupdate, name='lessonedit'), 
    path('lesson_details/<str:pk>/', views.lesson_details, name='lesson_details'), 
    # Tasks
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

    # Other URL patterns...
]
