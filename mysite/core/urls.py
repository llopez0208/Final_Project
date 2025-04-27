
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/add/', views.post_create, name='post_add'),
    path('posts/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('posts/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('', views.post_list, name='home'),
]
