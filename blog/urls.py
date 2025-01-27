from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    


    path('', views.home, name='home'),
    path('news/<str:pk>/', views.news, name='news'),
    path('user-profile/<str:pk>/', views.userProfile, name='profile'),
    path('create-post/', views.createPost, name='create'),
    path('update/<str:pk>/', views.updatePost, name='update'),
     path('edit-comment/<str:pk>/', views.editComment, name='edit-comment'),
    path('delete-post/<str:pk>/', views.deletePost, name='delete'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('update-user/', views.updateUser, name='update-user'),

    path('topics/', views.topicsView, name='topics'),
     path('activity/', views.activityView, name='activity'),



]
