from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.login_page),
    path('insertdata', login_required(views.insertdata)),
    path('garage', login_required(views.retrievedata)),
    path('index', login_required(views.index)),
    path('bill', login_required(views.bill)),
]