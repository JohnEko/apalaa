from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'apalaa/home.html')


def news(request, pk):
    return render(request, 'news.html')
