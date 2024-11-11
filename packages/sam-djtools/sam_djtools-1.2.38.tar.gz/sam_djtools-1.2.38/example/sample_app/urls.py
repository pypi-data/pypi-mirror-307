from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def hello(request):
    return HttpResponse("yes")

urlpatterns = [
    path('', hello),
]
