from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from .models import Test, Question, Answer

# Create your views here.
class AllQuestionsView(generic.ListView):
    template_name = 'testing/all_questions.html'
    context_object_name = 'data'


    def get_queryset(self):
        answers = {}

        for answer in Answer.objects.all():
            if answer.question.text in answers:
                answers[answer.question.text].append(answer.text) # if question to witch answer is related exists -> add to {question_text: [answer_obj,]}
            else:
                answers[answer.question.text] = [answer.text,] # if question to witch answer is related doesn't exist -> add {question_text: [answer_obj,]}

        return answers


class TestsView(generic.ListView):
    template_name = 'testing/tests.html'
    context_object_name = 'tests'
    
    def get_queryset(self):
        return Test.objects.order_by('-pub_date')


def TestingUser(request, pk):
    if request.method == 'POST':
        pass
    else:
        context = {}
        return render(request, 'testing/testing.html', context)


# it needs to be reworked
def RegisterUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse('Registration is success!')
    else:
        form = UserCreationForm()
        return render(request, 'testing/reg.html', {'form': form,})


def MainPage(request):
    print(request.user)
    if request.method == "POST":
        if request.POST['send_to'] == 'Questions':
            return HttpResponseRedirect('questions')
        elif request.POST['send_to'] == 'Tests':
            return HttpResponseRedirect('tests/')
        else:
            return HttpResponse('An Error has occured.')
    elif request.method == "GET":
        return render(request, 'testing/main_page.html')
    else:
        return render(request, 'testing/main_page.html')