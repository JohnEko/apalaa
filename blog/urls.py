from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<str:pk>/', views.news, name='news'),

]
