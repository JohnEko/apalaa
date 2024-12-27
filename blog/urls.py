from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('news/<str:pk>/', views.news, name='news'),
    path('create-post/', views.createPost, name='create'),
    path('update/<str:pk>/', views.updatePost, name='update'),
    path('delete-post/<str:pk>/', views.deletePost, name='delete'),


]
