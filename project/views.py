from django.shortcuts import render,redirect
from .models import *
from project.models import get_user_model
from .forms import *
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import azure.cognitiveservices.speech as speechsdk
import wave
import pygame
import os
import io
import random


# Create your views here.
# Cohort creating
@login_required(login_url='login')
def create_class(request):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        if request.method == 'POST':
            cohort = request.POST.get('class_name')
            cohort = Cohorts.objects.create(
                classname = cohort
            )
            return redirect('home')
    else:
        return redirect('home')


    context = {}
    return render(request,'project/classcreate.html',context)

@login_required(login_url='login')
def cohortlist(request):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        cohorts = Cohorts.objects.all()
        p = Paginator(cohorts,5)
        page_number = request.GET.get('page')
        cohorts = p.get_page(page_number)


    context = {'cohorts':cohorts}
    return render(request,'project/cohorts.html',context)



@login_required(login_url='login')
def update_cohort(request,pk):
    cohort = Cohorts.objects.get(id=pk)

    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        if request.method == 'POST':
            cohort_name = request.POST.get('class_name')
            cohort.classname = cohort_name
            cohort.save() 
    else:
        return redirect('home')


    context = {'cohort':cohort}
    return render(request,'project/classcreate.html',context)

@login_required(login_url='login')
def delete_cohort(request,pk):
    cohort = Cohorts.objects.get(id=pk)

    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        cohort.delete()
    else:
        return redirect('home')

    return redirect('home')




# Cohorts Assigning students
@login_required(login_url='login')
def assign_cohort(request,pk):
    user_role = request.user.role
    

    if user_role == 'teacher' or user_role == 'admin':
        cohort = Cohorts.objects.get(id = pk)


        linked_students_ids = Linking_UC.objects.all().values_list('student_id', flat=True)
        linked_students_id = Linking_UC.objects.filter(cohort=cohort).values_list('student_id', flat=True)
        cohort_students = get_user_model().objects.filter(id__in = linked_students_id)
        students = get_user_model().objects.filter(role = 'student').exclude(id__in = linked_students_ids)

        p = Paginator(cohort_students,10)
        page_number = request.GET.get('page')
        cohort_students = p.get_page(page_number)


        # Handling lessons show for one cohort
        page='ls_show'
        lessons_cohort = Lesson.objects.filter(cohort = cohort)
        cohort_name = Cohorts.objects.get(id=pk)
        


        if request.method == 'POST':
            if request.POST.get('type') == 'assign':
                id = request.POST.get('student_assign')
                student = get_user_model().objects.get(id=id)
                print('student===========',student)
                cohort = Linking_UC.objects.create(
                    cohort = cohort,
                    student = student
                )
            else:
                student_id = request.POST.get('student_id')
                link = Linking_UC.objects.get(student__id =student_id)
                link.delete()

            return redirect(f'/assign_cohort/{pk}/')


    else:
        return redirect('home')
    
    context = {'cohort':cohort,'students':students,'cohort_students':cohort_students,'page':page
               ,'lessons_cohort':lessons_cohort,'cohort_name':cohort_name}
    return render(request,'project/cohortassign.html',context)


# Single Cohort Details
@login_required(login_url='login')
def cohortdetails(request,pk):
    
   
    cohort = Cohorts.objects.get(id=pk)
    lessons = Lesson.objects.filter(cohort=cohort)

    # Handling lessons show for one cohort
    page='ls_show'
    cohort_name = cohort
    lessons_cohort = lessons


    context = {'cohort':cohort,'lessons':lessons,'page':page,'cohort_name':cohort_name,'lessons_cohort':lessons_cohort}
    return render(request,'project/cohortdetails.html',context)

# Lesson Create funtion
@login_required(login_url='login')
def lessoncreate(request,pk):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        cohort = Cohorts.objects.get(id = pk)
        
        if request.method == 'POST':
            lesson_name = request.POST.get('lesson_name')
            lesson = Lesson.objects.create(
                cohort = cohort,
                lesson_name = lesson_name
            )
            return redirect(f'/cohort_details/{pk}')
        
   
        context ={'cohort':cohort}
        return render(request,'project/lessoncreate.html',context)
    else:
        return redirect('home')
    
# Lesson Create funtion
@login_required(login_url='login')
def lessonupdate(request,pk):
    user_role = request.user.role
    lesson = Lesson.objects.get(id=pk)
    if user_role == 'teacher' or user_role == 'admin':
        
        if request.method == 'POST':
            lesson_name = request.POST.get('lesson_name')
            lesson.lesson_name =lesson_name
            lesson.save()

            return redirect('home')
        
   
        
    else:
        return redirect('home')
    context ={'lesson':lesson}
    return render(request,'project/lessoncreate.html',context)

@login_required(login_url='login')
def lessondelete(request,pk):
    user_role = request.user.role
    lesson = Lesson.objects.get(id=pk)
    if user_role == 'teacher' or user_role == 'admin':
        
        lesson.delete()
        return redirect('home')
        
   
        
    else:
        return redirect('home')
    context ={'lesson':lesson}
    return render(request,'project/lessoncreate.html',context)

# Lesson Details
@login_required(login_url='login')
def lesson_details(request,pk):
    # Added by hamza 8-2-24
    # logic for attempting question on the go
    user_role = request.user.role
    if user_role == 'student' and 'tasks_list' in request.session:
        tasks_list = request.session['tasks_list']
        print('in lesson',tasks_list)
        if len(tasks_list)>0:
            firsttask = tasks_list[0]
            taskmodel = firsttask['model_name']
            id = firsttask['task_id']
            tasks_list.pop(0)
            print('after pop',tasks_list)
            print('in lesson',firsttask)
            print('in lesson',taskmodel)
            # Updateing the task_list in sessions
            if len(tasks_list) ==0:
                del request.session['tasks_list']
            else:
                request.session['tasks_list'] = tasks_list
            # redirecting to corresponding task
            # T1 Update handle
            if taskmodel == 'T1':
                return redirect('task1_attempt',pk=id)
            # T2 Update handle
            if taskmodel == 'T2':
                return redirect('task2_attempt',pk=id)
            # T3 Update handle
            if taskmodel == 'T3':
                return redirect('task3_attempt',pk=id)
            # T4 Update handle
            if taskmodel == 'T4':
                return redirect('task4_attempt',pk=id)
            # T5 Update handle
            if taskmodel == 'T5':
                return redirect('task5_attempt',pk=id)
            # T6 Update handle
            if taskmodel == 'T6':
                return redirect('task6_attempt',pk=id)
            # T7 Update handle
            if taskmodel == 'T7':
                return redirect('task7_attempt',pk=id)
            # T8 Update handle
            if taskmodel == 'T8':
                return redirect('task8_attempt',pk=id)
            if taskmodel == 'SpeechQuestion':
                return redirect('speechQuestion_attempt',pk=id)
            
        # added by hamza 8-2-24 end
    


    lesson = Lesson.objects.get(id=pk)
    task_models = [T1, T2, T3, T4, T5, T6, T7, T8, SpeechQuestion]
    print(task_models[-1])
    student_id = request.user.id
    student = get_user_model().objects.get(id=student_id)
    
    # Retrieve tasks for each model and store them in a list of dictionaries
    # all_tasks_with_model = [{'task': model.objects.filter(lesson=lesson), 'model': model.__name__} for model in task_models]
    # getiing tasks with each model and assiging score with every task
    all_task_with_score_and_model = []
    
    for model in task_models:
        print(model,ContentType.objects.get_for_model(model))
        content_type = ContentType.objects.get_for_model(model)
        print("HERE")
        # getiing all score for this model and student
        scores = Score.objects.filter(student=student,content_type=content_type)
        
        scores_dict = {}
        for score in scores:
            # print(score.object_id,'+++++++++++++++++',model,score.score)
            scores_dict[score.object_id] = score.score
            # scores_dict[score.object_id] = "--"

        tasks = model.objects.filter(lesson=lesson)
        for task in tasks:
            score = scores_dict.get(task.id,'--')
            # print("=========",task.id,model,score)
            all_task_with_score_and_model.append({
                'task': task,
                'model': model.__name__,
                'score': score
            })
    
    # Deleting session lessonid
    if 'lessonid' in request.session:
        del request.session['lessonid']
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
    # Redirecting to appropriate task creation form
        if request.method == 'POST':
            
            if request.POST.get('task_type') == 'T1':
                return redirect(f'/task_type1_create/{pk}')
            if request.POST.get('task_type') == 'T2':
                return redirect(f'/task_type2_create/{pk}')
            if request.POST.get('task_type') == 'T3':
                return redirect(f'/task_type3_create/{pk}')
            if request.POST.get('task_type') == 'T4':
                return redirect(f'/task_type4_create/{pk}')
            if request.POST.get('task_type') == 'T5':
                return redirect(f'/task_type5_create/{pk}')
            if request.POST.get('task_type') == 'T6':
                return redirect(f'/task_type6_create/{pk}')
            if request.POST.get('task_type') == 'T7':
                return redirect(f'/fill_blanks_create/{pk}')
            if request.POST.get('task_type') == 'T8':
                return redirect(f'/spell_correct_create/{pk}')
            if request.POST.get('task_type') == 'SpeechQuestion':
                return redirect(f'/speechQuestion_create/{pk}')
    
    # Handling lessons show for one cohort
    page='ls_show'
    cohort_name =Cohorts.objects.get(classname = lesson.cohort)
    lessons_cohort= Lesson.objects.filter(cohort = lesson.cohort)
    context = {'lesson':lesson,'all_tasks':all_task_with_score_and_model,'page':page,'cohort_name':cohort_name,'lessons_cohort':lessons_cohort}
    return render(request,'project/lessondetails.html',context)

# Task Views

# T1 
@login_required(login_url='login')
def t1create(request,pk):
    
    print('============================================')
    form = T1form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T1form(request.POST,request.FILES)
        if form.is_valid():
            task1 = form.save(commit=False)
            task1.lesson = lesson
            task1.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t1.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t1.html',context)

# T1update
# @login_required(login_url='login')
# def t1update(request,id):
   
#     task = T1.objects.get(id=id)
#     form = T1form(instance=task)
#     if request.method == 'POST':
#         form = T1form(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(f'home')
#         else:
#             context = {'form':form}
#             return render(request,'project/t1.html',context)
        
#     context = {'form':form}
#     return render(request,'project/t1.html',context)


# T1  Update
@login_required(login_url='login')
def t1update(request,pk):
    task = T1.objects.get(id=pk)
    form = T1form(instance=task)
    try:
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        
        

        if request.method == 'POST':
            form = T1form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t1.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t1.html',context)
    except:
        if request.method == 'POST':
            form = T1form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t1.html',context)
            
        context = {'form':form}
        return render(request,'project/t1.html',context)
    

# T2 
@login_required(login_url='login')
def t2create(request,pk):
    print('============================================')
    form = T2form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T2form(request.POST,request.FILES)
        if form.is_valid():
            task2 = form.save(commit=False)
            task2.lesson = lesson
            task2.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t2.html',context)
            
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t2.html',context)


# T2  Update
@login_required(login_url='login')
def t2update(request,pk):
    task = T2.objects.get(id=pk)
    form = T2form(instance=task)
    try:
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        

        if request.method == 'POST':
            form = T2form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t2.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t2.html',context)
    except:
        if request.method == 'POST':
            form = T2form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t2.html',context)
            
        context = {'form':form}
        return render(request,'project/t2.html',context)


# T3 
@login_required(login_url='login')
def t3create(request,pk):
    print('============================================')
    form = T3form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T3form(request.POST,request.FILES)
        if form.is_valid():
            task3 = form.save(commit=False)
            task3.lesson = lesson
            task3.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t3.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t3.html',context)


# T3  Update
@login_required(login_url='login')
def t3update(request,pk):
    task = T3.objects.get(id=pk)
    form = T3form(instance=task)
    try:   
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        

        if request.method == 'POST':
            form = T3form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t3.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t3.html',context)
    except:
        if request.method == 'POST':
            form = T3form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t3.html',context)
            
        context = {'form':form}
        return render(request,'project/t3.html',context)



# T4 
@login_required(login_url='login')
def t4create(request,pk):
    
    form = T4form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T4form(request.POST,request.FILES)
        if form.is_valid():
            task4 = form.save(commit=False)
            task4.lesson = lesson
            task4.word1 = task4.word1.lower()
            task4.word2 = task4.word2.lower()
            task4.word3 = task4.word3.lower()
            task4.word4 = task4.word4.lower()
            task4.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t4.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t4.html',context)


# T4  Update
@login_required(login_url='login')
def t4update(request,pk):
    task = T4.objects.get(id=pk)
    form = T4form(instance=task)
    try:
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        

        if request.method == 'POST':
            form = T4form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                task4 = form.save(commit=False)
                task4.word1 = task4.word1.lower()
                task4.word2 = task4.word2.lower()
                task4.word3 = task4.word3.lower()
                task4.word4 = task4.word4.lower()
                task4.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t4.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t4.html',context)
    except:
        if request.method == 'POST':
            form = T4form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                task4 = form.save(commit=False)
                task4.word1 = task4.word1.lower()
                task4.word2 = task4.word2.lower()
                task4.word3 = task4.word3.lower()
                task4.word4 = task4.word4.lower()
                task4.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t4.html',context)
            
        context = {'form':form}
        return render(request,'project/t4.html',context)


# T5 
@login_required(login_url='login')
def t5create(request,pk):
    
    form = T5form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T5form(request.POST,request.FILES)
        if form.is_valid():
            task3 = form.save(commit=False)
            task3.lesson = lesson
            task3.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t5.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t5.html',context)


# T5  Update
@login_required(login_url='login')
def t5update(request,pk):
    task = T5.objects.get(id=pk)
    form = T5form(instance=task)
    try:
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        

        if request.method == 'POST':
            form = T5form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t5.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t5.html',context)
    except:
        if request.method == 'POST':
            form = T5form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t5.html',context)
            
        context = {'form':form}
        return render(request,'project/t5.html',context)

# T6 
@login_required(login_url='login')
def t6create(request,pk):
    
    form = T6form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T6form(request.POST,request.FILES)
        if form.is_valid():
            task3 = form.save(commit=False)
            task3.lesson = lesson
            task3.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t6.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t6.html',context)

# T6  Update
@login_required(login_url='login')
def t6update(request,pk):
    task = T6.objects.get(id=pk)
    form = T6form(instance=task)
    try:
        lessonid = request.session['lessonid']
        lesson = Lesson.objects.get(id = lessonid)
        

        if request.method == 'POST':
            form = T6form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t6.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t6.html',context)
    except:
        if request.method == 'POST':
            form = T6form(request.POST,request.FILES,instance=task)
            if form.is_valid():
                form.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t6.html',context)
            
        context = {'form':form}
        return render(request,'project/t6.html',context)


# T7
@login_required(login_url='login')
def t7create(request,pk):
    form = T7form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T7form(request.POST)
        if form.is_valid():
            task7 = form.save(commit=False)
            task7.lesson = lesson
            task7.answer = task7.answer.lower()
            task7.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t7.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t7.html',context)
# T7
@login_required(login_url='login')
def t7update(request,pk):
    task = T7.objects.get(id=pk)
    form = T7form(instance=task)
    try:
        lessonid = request.session['lessonid']
        
        
        lesson = Lesson.objects.get(id = lessonid)
        if request.method == 'POST':
            form = T7form(request.POST,instance=task)
            if form.is_valid():
                task7 = form.save(commit=False)
                task7.answer = task7.answer.lower()
                task7.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t7.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t7.html',context)
    except:
        if request.method == 'POST':
            form = T7form(request.POST,instance=task)
            if form.is_valid():
                task7 = form.save(commit=False)
                task7.answer = task7.answer.lower()
                task7.save()
                return redirect(f'red')
            else:
                context = {'form':form}
                return render(request,'project/t7.html',context)
            
        context = {'form':form}
        return render(request,'project/t7.html',context)

# T8
@login_required(login_url='login')
def t8create(request,pk):
    form = T8form()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = T8form(request.POST,request.FILES)
        if form.is_valid():
            task8 = form.save(commit=False)
            task8.lesson = lesson
            task8.answer = task8.answer.lower()
            task8.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/t8.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t8.html',context)
# T8
@login_required(login_url='login')
def t8update(request,pk):
    task = T8.objects.get(id=pk)
    form = T8form(instance=task)
    try:
        lessonid = request.session['lessonid']
        
        lesson = Lesson.objects.get(id = lessonid)
        if request.method == 'POST':
            form = T8form(request.POST,instance=task)
            if form.is_valid():
                task8 = form.save(commit=False)
                task8.answer = task8.answer.lower()
                task8.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/t8.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/t8.html',context)
    except:
        if request.method == 'POST':
            form = T8form(request.POST,instance=task)
            if form.is_valid():
                task8 = form.save(commit=False)
                task8.answer = task8.answer.lower()
                task8.save()
                return redirect(f'red/')
            else:
                context = {'form':form}
                return render(request,'project/t8.html',context)
            
        context = {'form':form}
        return render(request,'project/t8.html',context)
    
# S[eech Question]
@login_required(login_url='login')
def speechQuestioncreate(request,pk):
    form = SpeechQuestionform()
    lesson = Lesson.objects.get(id = pk)
    if request.method == 'POST':
        form = SpeechQuestionform(request.POST,request.FILES)
        if form.is_valid():
            taskSpeech = form.save(commit=False)
            taskSpeech.lesson = lesson
            taskSpeech.text_answer = taskSpeech.text_answer.lower()
            taskSpeech.save()
            return redirect(f'/lesson_details/{pk}/')
        else:
            context = {'form':form,'lesson':lesson}
            return render(request,'project/speechQuestion.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/speechQuestion.html',context)
# T8
@login_required(login_url='login')
def speechQuestionupdate(request,pk):
    task = SpeechQuestion.objects.get(id=pk)
    form = SpeechQuestionform(instance=task)
    try:
        lessonid = request.session['lessonid']
        
        lesson = Lesson.objects.get(id = lessonid)
        if request.method == 'POST':
            form = SpeechQuestionform(request.POST,instance=task)
            if form.is_valid():
                taskSpeech = form.save(commit=False)
                taskSpeech.text_answer = taskSpeech.text_answer.lower()
                taskSpeech.save()
                return redirect(f'/lesson_details/{lessonid}/')
            else:
                context = {'form':form,'lesson':lesson}
                return render(request,'project/speechQuestion.html',context)
            
        context = {'form':form,'lesson':lesson}
        return render(request,'project/speechQuestion.html',context)
    except:
        if request.method == 'POST':
            form = SpeechQuestionform(request.POST,instance=task)
            if form.is_valid():
                taskSpeech = form.save(commit=False)
                taskSpeech.text_answer = taskSpeech.text_answer.lower()
                taskSpeech.save()
                return redirect(f'red/')
            else:
                context = {'form':form}
                return render(request,'project/speechQuestion.html',context)
            
        context = {'form':form}
        return render(request,'project/speechQuestion.html',context)


# Task edit View
@login_required(login_url='login')
def taskedit(request,pk):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        request.session['lessonid'] =pk
        lesson = Lesson.objects.get(id=pk)
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            
            # T1 Update handle
            if model == 'T1':
                return redirect('task1_update',pk=id)
            # T2 Update handle
            if model == 'T2':
                return redirect('task2_update',pk=id)
            # T3 Update handle
            if model == 'T3':
                return redirect('task3_update',pk=id)
            # T4 Update handle
            if model == 'T4':
                return redirect('task4_update',pk=id)
            # T5 Update handle
            if model == 'T5':
                return redirect('task5_update',pk=id)
            # T6 Update handle
            if model == 'T6':
                return redirect('task6_update',pk=id)
            # T7 Update handle
            if model == 'T7':
                return redirect('task7_update',pk=id)
            # T8 Update handle
            if model == 'T8':
                return redirect('task8_update',pk=id)
    else:
        return redirect('home')
    
    return redirect('/lesson_details/{pk}/')


# Task delete View
@login_required(login_url='login')
def taskdelete(request):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            
            # T1 Update handle
            if model == 'T1':
                task = T1.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T2 Update handle
            if model == 'T2':
                task = T2.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T3 Update handle
            if model == 'T3':
                task = T3.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T4 Update handle
            if model == 'T4':
                task = T4.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T5 Update handle
            if model == 'T5':
                task = T5.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T6 Update handle
            if model == 'T6':
                task = T6.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T7 Update handle
            if model == 'T7':
                task = T7.objects.get(id=id)
                task.delete()
                return redirect('home')
            # T8 Update handle
            if model == 'T8':
                task = T8.objects.get(id=id)
                task.delete()
                return redirect('home')
                
    else:
        return redirect('home')
    


# Task Assign View
@login_required(login_url='login')
def taskassign(request,pk):
    user_role = request.user.role
    students=[]
    if user_role == 'teacher' or user_role == 'admin':
        id =  request.session['task_id']
        model = request.session['task_model']
        models= {'T1':T1,'T2':T2,'T3':T3,'T4':T4,'T5':T5,'T6':T6,'T7':T7,'T8':T8}
        content_type = ContentType.objects.get_for_model(models[model])

        lesson = Lesson.objects.get(id=pk)
        linked_students_ids = UserTask.objects.filter(content_type=content_type,object_id=id ).values_list('user_id',flat=True)
        # Handling of student list to display who have already been assigned to a task
        cohort = Cohorts.objects.get(classname = lesson.cohort)
        linked_cohort_students_id = Linking_UC.objects.filter(cohort=cohort).values_list('student_id', flat=True)
        cohort_students2 = get_user_model().objects.filter(id__in = linked_cohort_students_id)
        cohort_students3 = get_user_model().objects.filter(role='student',id__in=linked_students_ids)
        p = Paginator(cohort_students3,5)
        page_number = request.GET.get('page')
        cohort_students3 = p.get_page(page_number)
        
        # Handling of the cohort which is already completly assigned
        c_handle = Cohorts.objects.all().exclude(classname = lesson.cohort)
        cohort_used_id = [] 
        for c in c_handle:
            
            cohort_students = Linking_UC.objects.filter(cohort=c).values_list('student_id', flat=True)
            check_len = len(cohort_students)
            
            count = 0
            for i in cohort_students:
                if i in linked_students_ids:
                    count +=1
                    
                if count == check_len:
                    cohort_used_id.append(c.id)

        cohort_students = Linking_UC.objects.filter(cohort=lesson.cohort).values_list('student_id', flat=True)
        # final cohort and studens
        cohorts = Cohorts.objects.all().exclude(classname = lesson.cohort).exclude(id__in = cohort_used_id)
        students = get_user_model().objects.filter(role='student').exclude(id__in=cohort_students).exclude(id__in=linked_students_ids)
        
        # Handling lessons show for one cohort
        page='ls_show'
        cohort_name = Cohorts.objects.get(classname = lesson.cohort)
        lessons_cohort = Lesson.objects.filter(cohort = lesson.cohort)
        

        if request.method == 'POST':
            if request.POST.get('type') == 'id':

                student_id = request.POST.get('student_assign')
                student = get_user_model().objects.get(id=student_id)
                try:
                    already_exist = UserTask.objects.get(user = student,content_type = ContentType.objects.get_for_model(models[model]),
                            object_id = id) 
                except:   
                    user_task = UserTask.objects.create(
                            user = student,
                            content_type = ContentType.objects.get_for_model(models[model]),
                            object_id = id
                    )
                p = Paginator(cohort_students2,5)
                page_number = request.GET.get('page')
                cohort_students2 = p.get_page(page_number)
        
                context = {'students':students,'cohorts':cohorts,'cohort_students':cohort_students2,'cohort_students3':cohort_students3}
                return render(request,'project/taskassign.html',context)
            elif request.POST.get('type') == 'class':
                id_class = request.POST.get('class_assign')
                cohort = Cohorts.objects.get(id=id_class)
                cohort_students = Linking_UC.objects.filter(cohort=cohort).values_list('student', flat=True)
                user_task = UserTask.objects.filter(user__id__in=cohort_students,content_type=content_type,object_id=id).values_list('user', flat=True)
                cohort_student_ids = list(cohort_students)
                user_task_ids = list(user_task)

                # Get IDs in cohort_students that are not present in user_task
                remaining_students = [student_id for student_id in cohort_student_ids if student_id not in user_task_ids]
                                
                for i in remaining_students:
                    
                    student = get_user_model().objects.get(id=i)
                    content_type = ContentType.objects.get_for_model(models[model])
                   
                    
                    user_task = UserTask.objects.create(
                            user = student,
                            content_type = ContentType.objects.get_for_model(models[model]),
                            object_id = id
                        )
                p = Paginator(cohort_students2,5)
                page_number = request.GET.get('page')
                cohort_students2 = p.get_page(page_number)

                context = {'students':students,'cohorts':cohorts,'cohort_students':cohort_students2,'cohort_students3':cohort_students3}
                return render(request,'project/taskassign.html',context)
            else:
                student_id= request.POST.get('student_id')
                student = get_user_model().objects.get(id=student_id)
                user_task = UserTask.objects.get(user=student,content_type=content_type,object_id=id)
                user_task.delete()
                p = Paginator(cohort_students2,5)
                page_number = request.GET.get('page')
                cohort_students2 = p.get_page(page_number)
                context = {'students':students,'cohorts':cohorts,'cohort_students':cohort_students2,'cohort_students3':cohort_students3}
                return render(request,'project/taskassign.html',context)
                
                


        
    else:
        return redirect('home')
    
    
    context = {'students':students,'cohorts':cohorts,'cohort_students':cohort_students2,'cohort_students3':cohort_students3
               ,'page':page,'cohort_name':cohort_name,'lessons_cohort':lessons_cohort}
    return render(request,'project/taskassign.html',context)


# redirect to task assiging
@login_required(login_url='login')
def taskassignre(request,pk):
    user_role = request.user.role

    if user_role == 'teacher' or user_role == 'admin':
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            request.session['task_id'] = id
            request.session['task_model'] = model
                           
            return redirect('assign_task',pk=pk)
                       
    else:
        return redirect('home')
    

# Added by Hamza 7-2-24
    # Task Preview Section for Teacher
    
# T1 Preview
@login_required(login_url='login')
def t1preview(request,pk):
    task = T1.objects.get(id=pk)
    
 
        
    context = {'task':task}
    return render(request,'project/t1preview.html',context)


# T2 preview
@login_required(login_url='login')
def t2preview(request,pk):
    task = T2.objects.get(id=pk)
     
    context = {'task':task}
    return render(request,'project/t2preview.html',context)

# T3 preview
@login_required(login_url='login')
def t3preview(request,pk):
    task = T3.objects.get(id=pk)
        
    context = {'task':task}
    return render(request,'project/t3preview.html',context)

# T4 preview
@login_required(login_url='login')
def t4preview(request,pk):
    task = T4.objects.get(id=pk)   
        
    context = {'task':task}
    return render(request,'project/t4preview.html',context)

# T5 preview
@login_required(login_url='login')
def t5preview(request,pk):
    task = T5.objects.get(id=pk)
        
    context = {'task':task}
    return render(request,'project/t5preview.html',context)

# T6 preview
@login_required(login_url='login')
def t6preview(request,pk):
    task = T6.objects.get(id=pk)
        
    context = {'task':task}
    return render(request,'project/t6preview.html',context)

# T7 preview
@login_required(login_url='login')
def t7preview(request,pk):
    task = T7.objects.get(id=pk)  
    black_count = int(task.blanks_count) 
        
    context = {'task':task,'black_count':black_count}
    return render(request,'project/t7preview.html',context)

# T8 preview
@login_required(login_url='login')
def t8preview(request,pk):
    task = T8.objects.get(id=pk)
    task_length = len(task.answer)
        
    context = {'task':task,'task_length':task_length}
    return render(request,'project/t8preview.html',context)


    # Task preview View
@login_required(login_url='login')
def preview(request,pk):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            print(model)
            # T1 preview handle handle
            if model == 'T1':
                return redirect('task1_preview',pk=id)
            # T2 preview handle handle
            if model == 'T2':
                return redirect('task2_preview',pk=id)
            # T3 preview handle handle
            if model == 'T3':
                return redirect('task3_preview',pk=id)
            # T4 preview handle handle
            if model == 'T4':
                return redirect('task4_preview',pk=id)
            # T5 preview handle handle
            if model == 'T5':
                return redirect('task5_preview',pk=id)
            # T6 preview handle handle
            if model == 'T6':
                return redirect('task6_preview',pk=id)
            # T7 preview handle handle
            if model == 'T7':
                return redirect('task7_preview',pk=id)
            # T8 preview handle handle
            if model == 'T8':
                return redirect('task8_preview',pk=id)
            # Did not handle this 
            if model == 'SpeechQuestion':
                return redirect('speechQuestion_attempt',pk=id)
    else:
        return redirect('home')
    
    return redirect(f'/lesson_details/{pk}/')
# Added by Hamza 7-2-24 end
    


# Task attempt section


# T1 Attempt
@login_required(login_url='login')
def t1attempt(request,pk):
    task = T1.objects.get(id=pk)
    lessonid = request.session['lessonid']
    
    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        answer4 = request.POST.get('answer4')
        answer = task.answer.split(',')

        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if (answer[0] == str(answer1) and answer[1] == str(answer2) and answer[2] == str(answer3)
                               and answer[3] == str(answer4)) else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T1),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
            
        return redirect(f'/lesson_details/{lessonid}/')
        
    context = {'task':task}
    return render(request,'project/t1attempt.html',context)

# T2 Attempt
@login_required(login_url='login')
def t2attempt(request,pk):
    task = T2.objects.get(id=pk)
    lessonid = request.session['lessonid']
   
    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        answer4 = request.POST.get('answer4')
        answer = task.answer.split(',')
        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if (answer[0] == str(answer1) and answer[1] == str(answer2) and answer[2] == str(answer3)
                               and answer[3] == str(answer4)) else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T2),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()
        
        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
            
        return redirect(f'/lesson_details/{lessonid}/')
        
    context = {'task':task}
    return render(request,'project/t2attempt.html',context)

# T3 Attempt
@login_required(login_url='login')
def t3attempt(request,pk):
    task = T3.objects.get(id=pk)
    lessonid = request.session['lessonid']

    if request.method == 'POST':
        answer = request.POST.get('answer')

        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if answer == task.answer else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T3),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
          
        return redirect(f'/lesson_details/{lessonid}/')
        
    context = {'task':task}
    return render(request,'project/t3attempt.html',context)

# T4 Attempt
@login_required(login_url='login')
def t4attempt(request,pk):
    task = T4.objects.get(id=pk)
    lessonid = request.session['lessonid']
    
    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        answer4 = request.POST.get('answer4')
        answer = task.answer.split(',')
        

        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if (answer[0] == str(answer1) and answer[1] == str(answer2) and answer[2] == str(answer3)
                               and answer[3] == str(answer4)) else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T4),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
            
        return redirect(f'/lesson_details/{lessonid}/')
        
    context = {'task':task}
    return render(request,'project/t4attempt.html',context)

# T5 Attempt
@login_required(login_url='login')
def t5attempt(request,pk):
    task = T5.objects.get(id=pk)
    lessonid = request.session['lessonid']
    
    answer_list = task.answer.split(',')
    request.session['answer_list'] = answer_list
    request.session['life'] = task.number_of_life
    
    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        print('Answer1 is ', answer1)
        
        
        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)
        if answer1 == 'pass':
            score_value = 100 
            print('her1')
        else:
            score_value = 0
            print('her2')

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T5),
            object_id = task.id,
        )
        if 'answer_list' in request.session:
            del request.session['answer_list']
        if 'life' in request.session:
            del request.session['life']

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
            
        return redirect(f'/lesson_details/{lessonid}/')
    audio_display = task.total_images-1
    context = {'task':task,'audio_display':audio_display}
    return render(request,'project/t5attempt.html',context)

# Added by hamza
# Task 5 Ajax Part
def t5ajax(request):
    if request.method == 'POST':
        answerid = request.POST.get('imageanswer')
        check = answerid[5:]
        
        # print('answer id is ',answerid)
        # print('answer id is ',check)
        answer = request.session['answer_list']
        dead = False
        finished = False
        if check == answer[0]:
            pass
        else:
            life = request.session['life']
            life = life-1
            if life <= 0:
                dead = True

            # print('Current life',life)
            request.session['life'] = life
        #     print('after life',request.session['life'] )
        #     print('dead status',dead )
        # print('answer is',answer)
        answer.pop(0)
        if answer == []:
            finished = True
        request.session['answer_list'] = answer
        # print('answer is',answer)

        remainingLives = request.session['life']
        data = {'status': 'success','dead':dead,'finished':finished,'remainingLives':remainingLives}
        return JsonResponse(data)

    # Handle other HTTP methods if needed
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
# Added by hamza end

# T6 Attempt
@login_required(login_url='login')
def t6attempt(request,pk):
    task = T6.objects.get(id=pk)
    lessonid = request.session['lessonid']
    answer = task.answer.split(',')
    total_audios = len(answer)
    
    if request.method == 'POST':
        result = True
        for i in range(1,total_audios+1):
            check = request.POST.get(f'answer{i}')
            if check != answer[i-1]:
                result = False
                break
        
        # print('+++++=',answer)
        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if result else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T6),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
            
        return redirect(f'/lesson_details/{lessonid}/')

        
    
        
    context = {'task':task,'total_audios':total_audios}
    return render(request,'project/t6attempt.html',context)

# T7 Attempt
@login_required(login_url='login')
def t7attempt(request,pk):
    task = T7.objects.get(id=pk)
    black_count = int(task.blanks_count)
    lessonid = request.session['lessonid']
    print(task.option1)
    if request.method == 'POST':
        stored_answer = task.answer.split(',')
        
        for i in range(1,black_count+1):
            answer = request.POST.get(f'answer{i}').lower()
            stored_ans = stored_answer[i-1]
            print('answer is :',answer)
            print('stored asnwer is :',stored_answer[i-1])
            if answer == stored_ans:
                result = True
            else:
                result = False
                print('Wrong answer')
                break

        
        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if result else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T7),
            object_id = task.id,
        )
        
        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()

        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
        return redirect(f'/lesson_details/{lessonid}/')
        
    context = {'task':task,'black_count':black_count}
    print("HERE NOT THERE",task)
    return render(request,'project/t7attempt.html',context)

# T8 Attempt
@login_required(login_url='login')
def t8attempt(request,pk):
    task = T8.objects.get(id=pk)
    lessonid = request.session['lessonid']
    task_length = len(task.answer)
    
   
    if request.method == 'POST':
        answer_parts = []
        
        for i in range(1,task_length+1):
            answer_part = request.POST.get(f'answer{i}').lower()
            answer_parts.append(answer_part)
            
        answer = ''.join(answer_parts)
        print('===========', answer)
        student_id = request.user.id
        student = get_user_model().objects.get(id=student_id)

        score_value = 100 if answer == task.answer else 0

        score , created = Score.objects.get_or_create(
            student = student,
            content_type = ContentType.objects.get_for_model(T8),
            object_id = task.id,
        )

        if not created:
            score.score = score_value
            score.save()
        else:
            score.score = score_value
            score.save()


        
        if lessonid == -1:
            del request.session['lessonid']
            return redirect('/task_list/')
        return redirect(f'/lesson_details/{lessonid}/')
        
     
    context = {'task':task,'task_length':task_length}
    return render(request,'project/t8attempt.html',context)





# speech Attempt
@login_required(login_url='login')
def speechQuestionattempt(request,pk):
    task = SpeechQuestion.objects.get(id=pk)
    lessonid = request.session['lessonid']
   
    if request.method == 'POST':
        pass
        # This is where we will advance to the next question
        return redirect(f'/lesson_details/{lessonid}/')
        
        
    context = {'task':task}
    return render(request,'project/speechQuestionattempt.html',context)

# Task attempt View
@login_required(login_url='login')
def attempt(request,pk):
    user_role = request.user.role
    if user_role == 'student':
        request.session['lessonid'] =pk
        lesson = Lesson.objects.get(id=pk)
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            print(model)
            # T1 Update handle
            if model == 'T1':
                return redirect('task1_attempt',pk=id)
            # T2 Update handle
            if model == 'T2':
                return redirect('task2_attempt',pk=id)
            # T3 Update handle
            if model == 'T3':
                return redirect('task3_attempt',pk=id)
            # T4 Update handle
            if model == 'T4':
                return redirect('task4_attempt',pk=id)
            # T5 Update handle
            if model == 'T5':
                return redirect('task5_attempt',pk=id)
            # T6 Update handle
            if model == 'T6':
                return redirect('task6_attempt',pk=id)
            # T7 Update handle
            if model == 'T7':
                return redirect('task7_attempt',pk=id)
            # T8 Update handle
            if model == 'T8':
                return redirect('task8_attempt',pk=id)
            if model == 'SpeechQuestion':
                return redirect('speechQuestion_attempt',pk=id)
    else:
        return redirect('home')
    
    return redirect(f'/lesson_details/{pk}/')

# Added by Hamza 8-2-24
    # Contuniuse Qeustion Attempt Tasks
def que_attempt(request,pk):
    user_role = request.user.role
    if user_role == 'student':
        # Creating list for question attempting
        tasks_list = []
        model_classes = [T1, T2, T3, T4, T5, T6, T7, T8]
        for model_class in model_classes:
        
            tasks = model_class.objects.filter(lesson_id=pk)
        
            # Create dictionaries and append to the list
            for task in tasks:
                task_dict = {
                    'model_name': model_class.__name__,
                    'task_id': task.id,
                }
                tasks_list.append(task_dict)

        # Print or use the task_list as needed
        tasks_list2 = random.sample(tasks_list,len(tasks_list))
        print('Origrnal',tasks_list)
        print('random',tasks_list2)

        firsttask = tasks_list2[0]
        taskmodel = firsttask['model_name']
        id = firsttask['task_id']
        tasks_list2.pop(0)
        # Saving list in sessions and lesson id in sessions
        print('after pop',tasks_list2)
        print('in attempt',firsttask)
        print('in attempt',taskmodel)
        request.session['tasks_list']=tasks_list2
        request.session['lessonid'] =pk

        # redirecting to corresponding task
        # T1 Update handle
        if taskmodel == 'T1':
            return redirect('task1_attempt',pk=id)
        # T2 Update handle
        if taskmodel == 'T2':
            return redirect('task2_attempt',pk=id)
        # T3 Update handle
        if taskmodel == 'T3':
            return redirect('task3_attempt',pk=id)
        # T4 Update handle
        if taskmodel == 'T4':
            return redirect('task4_attempt',pk=id)
        # T5 Update handle
        if taskmodel == 'T5':
            return redirect('task5_attempt',pk=id)
        # T6 Update handle
        if taskmodel == 'T6':
            return redirect('task6_attempt',pk=id)
        # T7 Update handle
        if taskmodel == 'T7':
            return redirect('task7_attempt',pk=id)
        # T8 Update handle
        if taskmodel == 'T8':
            return redirect('task8_attempt',pk=id)
        if taskmodel == 'SpeechQuestion':
            return redirect('speechQuestion_attempt',pk=id)
       
    return redirect(f'/lesson_details/{pk}/')
# Added by Hamza 8-2-24

# Task Results View
@login_required(login_url='login')
def result(request,pk):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        
        lesson = Lesson.objects.get(id=pk)
        # Handling lessons show for one cohort
        page='ls_show'
        cohort_name = Cohorts.objects.get(classname = lesson.cohort)
        lessons_cohort = Lesson.objects.filter(cohort = lesson.cohort)


        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            
            # T1 content type assigning
            if model == 'T1':
                content_type = ContentType.objects.get_for_model(T1)
            # T2 content type assigning
            if model == 'T2':
                content_type = ContentType.objects.get_for_model(T2)
            # T3 content type assigning
            if model == 'T3':
                content_type = ContentType.objects.get_for_model(T3)
            # T4 content type assigning
            if model == 'T4':
                content_type = ContentType.objects.get_for_model(T4)
            # T5 content type assigning
            if model == 'T5':
                content_type = ContentType.objects.get_for_model(T5)
            # T6 content type assigning
            if model == 'T6':
                content_type = ContentType.objects.get_for_model(T6)
            # T7 content type assigning
            if model == 'T7':
                content_type = ContentType.objects.get_for_model(T7)
            # T8 content type assigning
            if model == 'T8':
                content_type = ContentType.objects.get_for_model(T8)
            # T8 content type assigning
            if model == 'SpeechQuestion':
                content_type = ContentType.objects.get_for_model(SpeechQuestion)

            results = Score.objects.filter(content_type=content_type,object_id = id)
            p = Paginator(results,10)
            page_number = request.GET.get('page')
            results = p.get_page(page_number)
    else:
        return redirect('home')
   

    context = {'results':results,'page':page,'cohort_name':cohort_name,'lessons_cohort':lessons_cohort}
    return render(request,'project/taskresult.html',context)

# Task list from home page
# Task attempt View
@login_required(login_url='login')
def task_list(request):
    user_role = request.user.role
    if user_role == 'student':
        request.session['lessonid'] = -1

        # getiing task for user
        student = get_user_model().objects.get(id=request.user.id)
        user_assigned_tasks = UserTask.objects.filter(user = student)
        all_task_with_score_and_model=[]
        for task1 in user_assigned_tasks:
            try:
                score = Score.objects.get(student=student,content_type=task1.content_type,object_id=task1.object_id)
                score = score.score
            except:
                score = "--"
            model_instance = task1.content_type.get_object_for_this_type(id=task1.object_id)
           
            
                # print("=========",task.id,model,score)
            all_task_with_score_and_model.append({
                    'task': model_instance,
                    'model': task1.content_type.model_class().__name__,
                    'score': score
            })
            
        p = Paginator(all_task_with_score_and_model,5)
        page_number = request.GET.get('page')
        all_task_with_score_and_model = p.get_page(page_number)
        
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            
            # T1 Update handle
            if model == 'T1':
                return redirect('task1_attempt',pk=id)
            # T2 Update handle
            if model == 'T2':
                return redirect('task2_attempt',pk=id)
            # T3 Update handle
            if model == 'T3':
                return redirect('task3_attempt',pk=id)
            # T4 Update handle
            if model == 'T4':
                return redirect('task4_attempt',pk=id)
            # T5 Update handle
            if model == 'T5':
                return redirect('task5_attempt',pk=id)
            # T6 Update handle
            if model == 'T6':
                return redirect('task6_attempt',pk=id)
            # T7 Update handle
            if model == 'T7':
                return redirect('task7_attempt',pk=id)
            # T8 Update handle
            if model == 'T8':
                return redirect('task8_attempt',pk=id)
            # SpeechQuesiton Update handle
            if model == 'SpeechQuestion':
                return redirect('SpeechQuestion_attempt',pk=id)
    else:
        return redirect('home')
    lesson = -1
    context = {'all_tasks':all_task_with_score_and_model,'lesson':lesson}
    return render(request,'project/task_list.html',context)


    
    
# generating the question lists
@login_required(login_url='login')
def questionsRGB(request):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        cohorts = Cohorts.objects.all()
        # cohorts = Cohorts.objects.all()
        # p = Paginator(cohorts,5)
        # page_number = request.GET.get('page')
        # cohorts = p.get_page(page_number)


    context = {'cohorts':cohorts}
    return render(request,'project/questionsRGB.html',context)

@login_required(login_url='login')
def red(request):
    user_role = request.user.role
    if user_role == 'teacher' or user_role == 'admin':
        t1 = T1.objects.all()
        t2 = T2.objects.all()
        t3 = T3.objects.all()
        t4 = T4.objects.all()
        t5 = T5.objects.all()
        t6 = T6.objects.all()
        t7 = T7.objects.all()
        t8 = T8.objects.all()
        # cohorts = Cohorts.objects.all()
        # p = Paginator(cohorts,5)
        # page_number = request.GET.get('page')
        # cohorts = p.get_page(page_number)


    context = {'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t6':t6,'t7':t7,'t8':t8}
    return render(request,'project/red.html',context)

def recognize_speech_azure(audio_file, subscription_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    print(1)

    # with open(audio_file, "rb") as audio_file:
    #     audio_data = audio_file.read()
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    print(2,audio_config)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="ga-IE",audio_config=audio_config)
    print(3)
    result = speech_recognizer.recognize_once()
    print(result)
    return result.text 

import wave
import array

def save_wav_file(file_path, audio_data, sample_rate=44100, bit_depth=16, channels=1):
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(bit_depth // 8)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(len(audio_data) // (bit_depth // 8) // channels)
        wav_file.setcomptype('NONE', 'not compressed')

        # Convert audio data to bytes using the correct type ('h' for signed short)
        # audio_bytes = array.array('h', audio_data).tobytes()
        wav_file.writeframes(audio_data)

from pydub import AudioSegment
from io import BytesIO

def convert_webm_to_wav(webm_file):
    # Load the WebM file from InMemoryUploadedFile
    audio_content = webm_file.read()
    print("1")
    # Decode the WebM audio content using the 'webm' codec
    decoded_audio = array.array('h', audio_content).tobytes()
    print("2")
    # Assuming the WebM audio has a sample width of 16 bits
    sample_width = 2

    # Create a new WAV file in memory
    wav_file = BytesIO()
    with wave.open(wav_file, 'wb') as wav_writer:
        wav_writer.setnchannels(2)  # Mono
        wav_writer.setsampwidth(sample_width)
        wav_writer.setframerate(44100)  # Adjust this to the appropriate sample rate
        wav_writer.writeframes(decoded_audio)
    print(f"WebM file size: {len(audio_content)} bytes")
    print(f"Decoded audio size: {len(decoded_audio)} bytes")
    return wav_file.getvalue()


# Example usage:
# audio_data is a list or array containing the audio samples
# Save as a mono (1 channel) WAV file with a sample rate of 44100 Hz and 16-bit depth
from django.core.files.storage import default_storage
@csrf_exempt  # To allow cross-origin requests (CSRF protection is disabled, handle with care in production)
def upload_audio_speech(request):
    if request.method == 'POST' :#and request.FILES.get('audioAsblob')
        print("HERERERERERERERER")
        print(request.FILES)
        audio_file = request.FILES['audio_file']
        wav_content = convert_webm_to_wav(audio_file)

        # Now, you can save the WAV content to a file or do whatever you need with it

        with open('.\\media\\output.wav', 'wb') as wav_file:
            wav_file.write(wav_content)

        # file_path = default_storage.save('recorded_audio_new.wav', audio_file)
        # audio_file = audio_file.read()
        # audio_file = io.BytesIO(audio_file)
        print("HERERnkdslnfjdsknb")
        # print(audio_file)
        # upload_folder = '.\\media\\'

        # Ensure the upload folder exists, create it if necessary
        # if not os.path.exists(upload_folder):
        #     os.makedirs(upload_folder)

        # Create a path for the uploaded file in the upload folder
        # file_path = os.path.join(upload_folder, 'recorded_audio.wav')

        # Write the content of the uploaded file to the specified path
        # with open(file_path, 'wb') as destination:
        #     for chunk in audio_file.chunks():
        #         destination.write(chunk)
        print("Here first")
        # play_wav_file(audio_file)
        print("HERE After")
        # reference_audio_file = ['cb.wav','cc.wav','cd.wav']
        subscription_key = '27431817deef478cb5190dec49e4c15f'
        region = 'northeurope'  # e.g., 'eastus'
        # save_wav_file(file_path, audio_file, sample_rate=44100, bit_depth=16, channels=1)
        audio_file_path = '.\\media\\output.wav'
        user_text = recognize_speech_azure(audio_file_path, subscription_key, region)


        file_path = '.\\media\\output.wav'
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting file '{file_path}': {e}")
        # recorded_audio = RecordedAudio(audio_file=audio_file)
        # audio_file.save()
        return JsonResponse({'message': 'Audio file uploaded successfully'})
    else:
        return JsonResponse({'error': 'No audio file found'})
    


