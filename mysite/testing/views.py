from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Questions, Tests

# Create your views here.
class AllQuestionsView(generic.ListView):
    template_name = 'testing/all_questions.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        return Questions.objects.all()

def MainPage(request):
    return(HttpResponse('You are in the main page.'))
