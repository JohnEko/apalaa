from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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

    context = {}
    return render(request, 'apalaa/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    post_details = Post.objects.filter(
        Q(title__icontains=q) |
        Q(created_at__icontains=q) |
        Q(content__icontains=q) 
        )
    user_comments = Comment.objects.all()
    post_count = post_details.count() #count the number of post in the blog
    context ={"post_details" : post_details,
              "user_comments" : user_comments,
              "post_count" : post_count
              }
    return render(request, 'apalaa/home.html', context=context)


def news(request, pk):
    post = Post.objects.get(id=pk)
    context = {"post" : post}
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
    if request.user != update_post:
        return HttpResponse('You are not allowed to edith or delect this post')

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
        return HttpResponse('You are not allowed to edith or delect this post')


    if request.method == "POST":
        delete_post.delete()
        return redirect('home')

    context = {'obj' : delete_post}
    return render(request, "apalaa/delete.html", context)