from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Test, Question, Answer

# Create your views here.
class AllQuestionsView(generic.ListView):
    template_name = 'testing/all_questions.html'
    context_object_name = 'data'


    def get_queryset(self):
        questions = []
        answers = {}

        for answer in Answer.objects.all():
            if answer.question.text in answers:
                answers[answer.question.text].append(answer.text)
            else:
                answers[answer.question.text] = [answer.text,]
                questions.append(answer.question)
        print(answers)
        return answers


class TestsView(generic.ListView):
    template_name = 'testing/tests.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.all()


def MainPage(request):
    return(HttpResponse('You are in the main page.'))
