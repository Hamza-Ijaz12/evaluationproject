from django.shortcuts import render,redirect
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,UserupdateForm,StudentUserForm
from project.models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import csv
from io import TextIOWrapper


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        a=False
        all_task_with_score_and_model=[]
        if request.user.role == 'teacher' or request.user.role == 'admin':
            cohort = Cohorts.objects.all()[:3]
            if cohort:
                a=True
            context = {'cohort':cohort,'all_tasks':all_task_with_score_and_model,'cohort_count':a}
            return render(request,'authuser/index.html',context)
        else:
            
            student = User.objects.get(id=request.user.id)
            link_to_cohort = Linking_UC.objects.filter(student=student).first()
            lessons_info = []
            if link_to_cohort:
                cohort = Cohorts.objects.get(classname=link_to_cohort.cohort)
                cohort_lessons = Lesson.objects.filter(cohort = cohort)
                
                print('------------her1')
                for lesson in cohort_lessons:
                    # Count total tasks for each lesson
                    total_tasks = T1.objects.filter(lesson=lesson).count() + T2.objects.filter(lesson=lesson).count() + \
                                T3.objects.filter(lesson=lesson).count() +T4.objects.filter(lesson=lesson).count() + \
                                T5.objects.filter(lesson=lesson).count() +T6.objects.filter(lesson=lesson).count() + \
                                T7.objects.filter(lesson=lesson).count() + T8.objects.filter(lesson=lesson).count()

                    # Count completed tasks by the user for each lesson
                    completed_tasks = (
                        Score.objects.filter(student=student, content_type__in=[
                            ContentType.objects.get_for_model(T1),ContentType.objects.get_for_model(T2),ContentType.objects.get_for_model(T3),
                            ContentType.objects.get_for_model(T4),ContentType.objects.get_for_model(T5),ContentType.objects.get_for_model(T6),
                            ContentType.objects.get_for_model(T7),ContentType.objects.get_for_model(T8),
                        ], object_id__in=[
                            *T1.objects.filter(lesson=lesson).values_list('id', flat=True),*T2.objects.filter(lesson=lesson).values_list('id', flat=True),
                            *T3.objects.filter(lesson=lesson).values_list('id', flat=True),*T4.objects.filter(lesson=lesson).values_list('id', flat=True),
                            *T5.objects.filter(lesson=lesson).values_list('id', flat=True),*T6.objects.filter(lesson=lesson).values_list('id', flat=True),
                            *T7.objects.filter(lesson=lesson).values_list('id', flat=True),*T8.objects.filter(lesson=lesson).values_list('id', flat=True),
                        ]).count()
                    )
                    print('===========here2',total_tasks)
                    # Append the lesson info to the list
                    lessons_info.append({
                        'lesson_name': lesson,
                        'total_tasks': total_tasks,
                        'completed_tasks': completed_tasks
                    })

                a=True
            else:
                cohort = []
            user_assigned_tasks = UserTask.objects.filter(user=student)[:3]
            for task1 in user_assigned_tasks:
                try:
                    score = Score.objects.get(student=student, content_type=task1.content_type, object_id=task1.object_id)
                    score = score.score
                except Score.DoesNotExist:
                    score = "--"
                model_instance = task1.content_type.get_object_for_this_type(id=task1.object_id)
                all_task_with_score_and_model.append({
                        'task': model_instance,
                        'model': task1.content_type.model_class().__name__,
                        'score': score
                    })
                
            context = {'cohort':cohort,'all_tasks':all_task_with_score_and_model,'cohort_count':a
                       ,'lessons_info':lessons_info}
            return render(request,'authuser/index.html',context)
                
            
        
        
        
    else:
        return redirect('login')


def loginpage(request):
    
    if request.method =='POST':
        
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
        except:
            return HttpResponse("User does not exits")
        user = authenticate(request,email=email,password=password)
        
            
        

        if user is not None:
            login(request,user)
            # Redirect to passoword change if he is login for the first time
            if user.role == 'teacher' and user.first_login:
                request.session['email'] = email
                print("Session entry done+++++++++++++++++=")
                    
                return redirect('reset')
            else:
                user.first_login = False
                user.save()

            return redirect('home')
        else:
            return HttpResponse("Invalid Credantials")
    context ={}
    return render(request,'authuser/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def resetpassword(request):
    messages=None
    user = User.objects.get(id = request.user.id)
    # del request.session['email']
    # print(user.email,'========================')
    if request.method =='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            if user.role == 'teacher' and user.first_login:
                user.first_login =False
            
            user.save()

            messages = "Password changed successfully"
            logout(request)
            return redirect('/login')

        else:
            messages = "Password do not match"

    context ={'messages':messages}
    return render(request,'authuser/reset.html',context)

# New User creation
def registerpage(request):
    messages = ''
    form=UserForm()
    if request.method=='POST':
        form=UserForm(request.POST,request.FILES)
        print('----------------- here1')
        if form.is_valid():
            print('----------------- here2')
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.email=user.email.lower()
            user.set_password(form.cleaned_data['password1'])
            print('----------------- here3')
            user.save()
            return redirect('home')
            
        else:
            messages = (request,'Something went wrong with registration')
    context={'form':form,'messages':messages}
    return render(request,'authuser/register.html',context)

# USer Update
def updateuserpage(request,pk):
    messages = ''
    user = User.objects.get(id=pk)
    form=UserupdateForm(instance=user)
    if request.method=='POST':
        form=UserupdateForm(request.POST,request.FILES,instance=user)
        print('----------------- here1')
        if form.is_valid():
            print('----------------- here2')
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.email=user.email.lower()
            print('----------------- here3')
            user.save()
            return redirect('home')
            
        else:
            messages = (request,'Something went wrong with registration')
    context={'form':form,'messages':messages}
    return render(request,'authuser/userupdate.html',context)

# all users list
def alluser(request):
    users = User.objects.all().exclude(email = 'hamza@gmail.com')
    p = Paginator(users,10)
    page_number = request.GET.get('page')
    users = p.get_page(page_number)

    # Handling form submissions
    if request.method == 'POST':
        id = request.POST.get('user_id')
        role = request.POST.get('role_select')
        user = User.objects.get(id=id)
        user.role = role
        user.save()


    context={'users':users}
    return render(request,'authuser/alluser.html',context)


# New User creation
def studentregister(request):
    messages = ''
    form = StudentUserForm()
    if request.method=='POST':
        form=StudentUserForm(request.POST,request.FILES)
        print('----------------- here1')
        if form.is_valid():
            print('----------------- here2')
            csv_file = form.cleaned_data['csv_file']
            csv_file.seek(0)
            # Keith - May have to change this
            csv_reader = csv.DictReader(TextIOWrapper(csv_file.file, encoding='utf-8-sig'))
            print(csv_file)
            headers = csv_reader.fieldnames
            print(f'Headers: {headers}')

            # Process each row in the CSV file
            for row in csv_reader:
                username = row['username'].lower()
                email = row['email'].lower()
                password = row['password']

                # Create a new User object
                user = User(username=username, email=email)
                user.set_password(password)

                # Save the User object to the database
                user.save()
                student = get_user_model().objects.get(username=username)
                cohort = Cohorts.objects.get(classname = row['cohort'])
                Linking_UC.objects.create(
                    cohort = cohort,
                    student = student
                )
            
            # csv_file.seek(0)
            # csv_reader = csv.DictReader(TextIOWrapper(csv_file, encoding='utf-8'))
            # print(csv_reader)
            # with open(csv_file, 'r', encoding='utf-8') as csvfile_a:
            #     csvfile_a = csv.reader(csvfile_a)
            
            #     # Assuming the first row contains headers
            #     headers = next(csvfile_a)
            #     print(f'Headers: {headers}')

            #     # Print each row in the CSV file
            #     for row in csvfile_a:
            #         print(row)
            # for row in csv_reader:
            #     # Extract data from the CSV row
            #     print(row)
                # username = row['username'].lower()
                # email = row['email'].lower()
                # password = row['password']

                # # Create a new User object
                # user = User(username=username, email=email)
                # user.set_password(password)

                # # Save the User object to the database
                # user.save()
            print('----------------- here3')
            return redirect('home')
            
        else:
            messages = (request,'Something went wrong with registration')
    context={'form':form,'messages':messages}
    return render(request,'authuser/studentregister.html',context)

