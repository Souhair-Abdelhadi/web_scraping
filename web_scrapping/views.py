from django.http import HttpResponse
from django.shortcuts import render

def pageNotFound(request,exception):
    return render(request,"pageNotFound.html",status=404)
