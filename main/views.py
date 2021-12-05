from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Tweet
from main.models import Confusion
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

def postlecture_view(request):
    return render(request, 'postlecture.html' )

def teacherclass_view(request):
    return render(request, 'teacherClass.html' )

def teacherpostlecture_view(request):
    return render(request, 'teacherpostlecture.html' )



'''ACTIONS'''
# delete a tweet routing
def delete_view(request):
    tweet = Tweet.objects.get(id=request.GET['id'])
    if tweet.author == request.user:
        tweet.delete()
    return redirect('/')

# like a tweet
def like_tweet(request):
    tweet = Tweet.objects.get(id=request.GET['id'])

    # not yet liked
    if len(tweet.likes.filter(username=request.user.username)) == 0:
        tweet.likes.add(request.user)
    
    # liked
    else:
        tweet.likes.remove(request.user)

    tweet.save()
    return redirect('/')


'''USER LOGIN/REGISTRATION/LOGOUT'''

# login
def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

# signupstudent
def signupstudent_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    return redirect('/')

# signupteacher
def signupteacher_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    return redirect('/teacherClass')

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