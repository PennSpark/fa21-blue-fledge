from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Confusion, Profile
from datetime import datetime

'''TEMPLATE RENDERING'''
def main_view(request):
    if not request.user.is_authenticated:
        return redirect('/onboarding/')
    
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

def postlecture_view(request):
    return render(request, 'feedback.html' )

def onboarding_view(request):
    return render(request, 'onboarding.html' )



''' TEACHER / STUDENT VIEWS '''

def teacherclass_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')
    #count = Confusion.objects.all().count()

    ''' (1) % students confused '''
    confused_students = set()
    confusions = Confusion.objects.all()
    for confusion in confusions:
        person = confusion.author.username
        confused_students.add(person)
    number_confused_students = len(confused_students)
    
    total_num_students = 0
    students = Profile.objects.all()
    for student in students:
        if student.accountType == "student":
            total_num_students += 1

    percent_confused = number_confused_students / total_num_students * 100.0

    ''' (2) num of each type of confusion '''
    confusion_counts = {
        'general': 0,
        'slow': 0,
        'repeat': 0,
        'rephrase': 0,
        'example': 0,
        'other': 0
    }
    for confusion in confusions:
        confusion_type = confusion.student_request
        confusion_counts[confusion_type] += 1
        
    return render(request, 'teacherClass.html', {
        'percent_confused' : percent_confused, 
        'num_general' : confusion_counts['general'],
        'num_slow' : confusion_counts['slow'],
        'num_repeat' : confusion_counts['repeat'],
        'num_rephrase' : confusion_counts['rephrase'],
        'num_example' : confusion_counts['example'],
        'num_other' : confusion_counts['other'],
    })

def teacherpostlecture_view(request):
    return render(request, 'teacherpostlecture.html' )


'''USER LOGIN/REGISTRATION/LOGOUT'''

# login
def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if user.profile.accountType == "student":
            return redirect('/')
        else:
            return redirect('/teacherClass')
        #return redirect('/')
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