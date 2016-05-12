from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id=1):
    return HttpResponse("You're looking at the question %s." % question_id)

def results(request, question_id=1):
    return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id=1):
    return HttpResponse("Hello, world. You're voting on question %s." % question_id )