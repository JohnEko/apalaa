from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Comment, Post
from django.contrib.auth.models import User

from .forms import PostForm

"""
The first view function is to get all the user and again we using filter yo filter user
The second function is to be a specific user with the news detail
The other is to post new updated news from user
This is to check if user can update is comments or post
This to help user to deletes is post 

"""
# Create your views here.

def loginPage(request):
    page = 'loginPage'
    #if am login i should not be allowed to be on login oage
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
           
        except:
            messages.error(request, 'User dose not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name and Password dose not exist')

    context = {'page': page}
    return render(request, 'apalaa/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False) #help to set the details to automatic lower case
            user.username = user.username.lower()
            user.save()
            login(request, user) #logging the user that just registered
            return redirect('home')
        else:
            messages.error(request, 'error occur during registration')


    context = {'form' : form}
    return render(request, 'apalaa/login_register.html', context)

#we can also add the number of visited users everyday
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    post_details = Post.objects.filter(
        Q(title__icontains=q) |
        Q(created_at__icontains=q) |
        Q(content__icontains=q) 
        )
    user_comments = Comment.objects.all()
    post_count = post_details.count() #count the number of post in the blog
    news_comments = Comment.objects.all() #This will help to see people you follow comments
    context ={"post_details" : post_details,
              "user_comments" : user_comments,
              "post_count" : post_count,
              "news_comments" : news_comments
              }
    return render(request, 'apalaa/home.html', context=context)


"""
 # this takes the messades from the model and set everything 
 # here never mind if its cap letter it turns it to lower case
 Most recent message order by
"""

def news(request, pk):
    post = Post.objects.get(id=pk)
    post_meassges = Comment.objects.all().order_by('-created_at')
    participants= post.participants.all() #Bringing all our participant from our models
    
    #Creating a post request for user to comments on a post in an article
    if request.method == 'POST':
        message = Comment.objects.create(
            post = post,
            user=request.user,
            content=request.POST.get('body')
        )
        #We need to process a participant when they are added to a conversation
        #we can also remove the participant also
        post.participants.add(request.user)
        return redirect('news', pk=post.id)
    context = {"post" : post,
               'post_messages': post_meassges,
               'participants': participants
               }
    return render(request, 'news.html', context=context)


#We direct the user to our login page if users want to see some pages
@login_required(login_url='/login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "apalaa/post_form.html", context)

# Giving permission to users
@login_required(login_url='/login')
def updatePost(request, pk):
    update_post = Post.objects.get(id=pk)
    form = PostForm(instance=update_post)

    #restrict other users from delecting someone post if they are not the owner of the post
    # if request.user != update_post:
    #     return HttpResponse('You are not allowed to edith or delete this post')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=update_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'apalaa/post_form.html', context)


# Giving login users permission permission to users
@login_required(login_url='/login')
def deletePost(request, pk):
    delete_post = Post.objects.get(id=pk)

    if request.user != delete_post:
        return HttpResponse('You are not allowed to edith or delete this post')


    if request.method == "POST":
        delete_post.delete()
        return redirect('home')

    context = {'obj' : delete_post}
    return render(request, "apalaa/delete.html", context)

#Create a function for users to delete there message

@login_required(login_url='/login')
def deleteComment(request, pk):
    delete_comment = Comment.objects.get(id=pk)

    if request.user != delete_comment.user:
        return HttpResponse('You are not allowed to edith or delete this post')


    if request.method == "POST":
        delete_comment.delete()
        return redirect('home')

    context = {'obj' : delete_comment}
    return render(request, "apalaa/delete.html", context)

def editComment(request, pk):
    edit_comment = Comment.objects.get(id=pk)
    form = PostForm(instance=edit_comment)

    #restrict other users from delecting someone post if they are not the owner of the post
    # if request.user != update_post:
    #     return HttpResponse('You are not allowed to edith or delete this post')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=edit_comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'apalaa/post_form.html', context)
