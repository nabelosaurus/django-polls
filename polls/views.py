from django.http import Http404
from django.shortcuts import get_object_or_404, render

from . models import Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id=1):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)

def results(request, question_id=1):
    context = {}
    return render(request, 'polls/results.html', context)

def vote(request, question_id=1):
    context = {}
    return render(request, 'polls/vote.html', context)