from django.shortcuts import render,redirect
from .models import *
from project.models import get_user_model
from .forms import *
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery

# Create your views here.
# Cphort creating
@login_required(login_url='login')
def create_class(request):
    user_role = request.user.role
    if user_role == 'teacher':
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
def update_cohort(request,pk):
    cohort = Cohorts.objects.get(id=pk)

    user_role = request.user.role
    if user_role == 'teacher':
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
    if user_role == 'teacher':
        cohort.delete()
    else:
        return redirect('home')

    return redirect('home')




# Cohorts Assigning students
@login_required(login_url='login')
def assign_cohort(request,pk):
    user_role = request.user.role
    if user_role == 'teacher':
        cohort = Cohorts.objects.get(id = pk)

        linked_students_ids = Linking_UC.objects.all().values_list('student_id', flat=True)

        students = get_user_model().objects.filter(role = 'student',).exclude(id__in = linked_students_ids)
        if request.method == 'POST':
            id = request.POST.get('student_assign')
            student = get_user_model().objects.get(id=id)
            print('student===========',student)
            cohort = Linking_UC.objects.create(
                cohort = cohort,
                student = student
            )
            return redirect(f'/assign_cohort/{pk}/')


    else:
        return redirect('home')
    
    context = {'cohort':cohort,'students':students}
    return render(request,'project/cohortassign.html',context)


# Single Cohort Details
@login_required(login_url='login')
def cohortdetails(request,pk):
   
    cohort = Cohorts.objects.get(id=pk)
    lessons = Lesson.objects.filter(cohort=cohort)

    context = {'cohort':cohort,'lessons':lessons}
    return render(request,'project/cohortdetails.html',context)

# Lesson Create funtion
@login_required(login_url='login')
def lessoncreate(request,pk):
    user_role = request.user.role
    if user_role == 'teacher':
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
    if user_role == 'teacher':
        
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
    if user_role == 'teacher':
        
        lesson.delete()
        return redirect('home')
        
   
        
    else:
        return redirect('home')
    context ={'lesson':lesson}
    return render(request,'project/lessoncreate.html',context)

# Lesson Details
@login_required(login_url='login')
def lesson_details(request,pk):
    lesson = Lesson.objects.get(id=pk)
    task_models = [T1, T2, T3, T4, T5, T6, T7, T8]

    # Retrieve tasks for each model and store them in a list of dictionaries
    all_tasks_with_model = [{'task': model.objects.filter(lesson=lesson), 'model': model.__name__} for model in task_models]
    all_task = []
    # Deleting session lessonid
    if 'lessonid' in request.session:
        del request.session['lessonid']
    user_role = request.user.role
    if user_role == 'teacher':
    # Redirecting to appropriate task creation form
        if request.method == 'POST':
            # print('Booooooooooooooooooom',request.POST.get('task_type'))
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
        

    context = {'lesson':lesson,'all_tasks_with_model':all_tasks_with_model}
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
@login_required(login_url='login')
def t1update(request,id):
   
    task = T1.objects.get(id=id)
    form = T1form(instance=task)
    if request.method == 'POST':
        form = T1form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'home')
        else:
            context = {'form':form}
            return render(request,'project/t1.html',context)
        
    context = {'form':form}
    return render(request,'project/t1.html',context)


# T1  Update
@login_required(login_url='login')
def t1update(request,pk):
    task = T1.objects.get(id=pk)
    form = T1form(instance=task)
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
            return render(request,'project/t7.html',context)
        
    context = {'form':form,'lesson':lesson}
    return render(request,'project/t7.html',context)


# Task edit View
@login_required(login_url='login')
def taskedit(request,pk):
    user_role = request.user.role
    if user_role == 'teacher':
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
    if user_role == 'teacher':
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
    if user_role == 'teacher':
        id =  request.session['task_id']
        model = request.session['task_model']
        models= {'T1':T1,'T2':T2,'T3':T3,'T4':T4,'T5':T5,'T6':T6,'T7':T7,'T8':T8}
        content_type = ContentType.objects.get_for_model(models[model])

        lesson = Lesson.objects.get(id=pk)
        linked_students_ids = UserTask.objects.filter(content_type=content_type,object_id=id ).values_list('user_id',flat=True)
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
        

        if request.method == 'POST':
            if request.POST.get('type') == 'id':

                student_id = request.POST.get('student_assign')
                student = get_user_model().objects.get(id=student_id)
               
                    
                user_task = UserTask.objects.create(
                        user = student,
                        content_type = ContentType.objects.get_for_model(models[model]),
                        object_id = id
                )
                return redirect(f'/lesson_details/{pk}/')
            else:
                id_class = request.POST.get('class_assign')
                cohort = Cohorts.objects.get(id=id_class)
                cohort_students = Linking_UC.objects.filter(cohort=cohort).values_list('student', flat=True)
                for i in cohort_students:
                    student = get_user_model().objects.get(id=i)
                    user_task = UserTask.objects.create(
                        user = student,
                        content_type = ContentType.objects.get_for_model(models[model]),
                        object_id = id
                    )
                return redirect(f'/lesson_details/{pk}/')
                


        
    else:
        return redirect('home')
    context = {'students':students,'cohorts':cohorts}
    return render(request,'project/taskassign.html',context)



@login_required(login_url='login')
def taskassignre(request,pk):
    user_role = request.user.role

    if user_role == 'teacher':
        if request.method == 'POST':
            id = request.POST.get('id')
            model = request.POST.get('model')
            request.session['task_id'] = id
            request.session['task_model'] = model
                           
            return redirect('assign_task',pk=pk)
                       
    else:
        return redirect('home')
    
    
