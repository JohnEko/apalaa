from django.shortcuts import render, redirect
from .models import Category, Comment, Post
from .forms import PostForm
# Create your views here.

def home(request):
    post_details = Post.objects.all()
    context ={"post_details" : post_details}
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
    update_news = Post.objects.get(id=pk)
    form =PostForm(instance=update_news)
    if request.method == 'Post':
        form = PostForm(request.POST, instance=update_news)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'apalaa/post_form.html', context)