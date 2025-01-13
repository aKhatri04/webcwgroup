"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from .views import hobby_api, hobbies_api, users_api, user_api, user_hobbies_api, main_spa
from .views import main_spa
from . import views

urlpatterns = [
    path('', main_spa),

    # API entry points should be defined here
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('hobbies/', hobbies_api, name='hobbies api'),
    path('hobby/<int:hobby_id>', hobby_api, name='hobby api'),
    path('users/', users_api, name='users api'),
    path('user/<int:user_id>', user_api, name='user api'),
    path('user_hobbies/', user_hobbies_api, name='user hobbies api'),
    path('user_hobby/<int:user_hobby_id>', user_hobbies_api, name='user hobby api'),
]

