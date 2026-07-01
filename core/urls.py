from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]