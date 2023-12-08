from django.shortcuts import render,redirect
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from project.models import Cohorts
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    cohort = Cohorts.objects.all()
    if request.user.is_authenticated:
        role = request.user.role
    else:
        role = ''
    context = {'cohort':cohort,'role':role}
    return render(request,'authuser/index.html',context)


def loginpage(request):
    page = 'login'
    
    if request.method =='POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        print("user name +++++++++++++",email)
        print("Password ++++++++++++++++++",password)
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
    context ={'page':page}
    return render(request,'authuser/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def resetpassword(request):
    messages=None
    user = User.objects.get(email = request.session['email'])
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
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.email=user.email.lower()
            user.save()
            # login(request,user)
            return redirect('home')
        else:
            messages = (request,'Something went wrong with registration')
    context={'form':form,'messages':messages}
    return render(request,'authuser/login.html',context)
