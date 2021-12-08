from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Confusion, Profile
from datetime import datetime

'''TEMPLATE RENDERING'''
def main_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')
    
    if request.method == 'POST' and request.POST['confusions'] != "":
        confuse = Confusion.objects.create(
            student_request = request.POST['confusions'],
            author = request.user,
            created_at = datetime.now()
        )
        confuse.save()

    #tweets = Tweet.objects.all().order_by('-created_at')
    #Confusion.objects.all().count()
    
    return render(request, 'main.html')

def splash_view(request):
    return render(request, 'splash.html' )

def student_view(request):
    return render(request, 'studentHome.html' )

def teacher_view(request):
    return render(request, 'teacherHome.html' )

def postlecture_view(request):
    return render(request, 'postlecture.html' )

def teacherclass_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')
    #count = Confusion.objects.all().count()
    return render(request, 'teacherClass.html' )

def teacherpostlecture_view(request):
    return render(request, 'teacherpostlecture.html' )


'''USER LOGIN/REGISTRATION/LOGOUT'''

# login
def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if user.profile.accountType == "teacher":
            return redirect('/teacher')
        else:
            return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

def signup_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    profile = Profile.objects.create(
        user = user,
        accountType = request.POST.get('account_type', "student")
    )
    profile.save()
    return redirect('/')

# logout
def logout_view(request):
    logout(request)
    return redirect('/splash')

# endclass
def endclass_view(request):
    # endclass(request)
    return redirect('/postlecture')

# teacherEnd
def teacherEnd_view(request):
    return redirect('/teacherpostlecture')