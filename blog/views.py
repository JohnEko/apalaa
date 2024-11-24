from django.shortcuts import render
from .models import Category, Comment, Post

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
    context = {}
    return render(request, "apalaa/post_form.html", context)
