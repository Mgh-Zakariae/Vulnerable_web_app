from django.urls import include, path 
from . import views

urlpatterns = [
    path('', views.DisplayAll, name='posts'),
    path('posts/create_post', views.create_post, name='createPost'),
    path('posts/<int:id>', views.dispalyPost, name='post'),
    path('posts/my_posts', views.my_posts, name='myPost'),
    path('posts/my_posts/edit_post/<int:id>', views.edit_post, name='editpost'),
    path('posts/my_posts/details/', views.details, name='details'),
    path('posts/my_posts/delete/<int:id>', views.delete_post, name='delete'),
]