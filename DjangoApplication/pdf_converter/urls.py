from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('creation/', add_resume, name='add_resume'),
    path('logout/', logout_user, name='logout'),
    path('show/', show_archive, name='show_archive'),
    path('download/<int:resume_id>/', download, name='download'),
    path('view/<int:resume_id>/', view, name='view'),
    path('resume/<int:resume_id>/', show_resume, name='show_resume')
]