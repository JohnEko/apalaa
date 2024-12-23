from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Category, Comment, Post
from .forms import PostForm

"""
The first view function is to get all the user and again we using filter yo filter user
The second function is to be a specific user with the news detail
The other is to post new updated news from user
This is to check if user can update is comments or post
This to help user to deletes is post 

"""
# Create your views here.

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

def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "apalaa/post_form.html", context)

def updatePost(request, pk):
    update_post = Post.objects.get(id=pk)
    form = PostForm(instance=update_post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=update_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'apalaa/post_form.html', context)


def deletePost(request, pk):
    delete_post = Post.objects.get(id=pk)

    if request.method == "POST":
        delete_post.delete()
        return redirect('home')

    context = {'obj' : delete_post}
    return render(request, "apalaa/delete.html", context)