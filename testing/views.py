from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from .models import Test, Question, Answer, UserTests

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


def TestingPage(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/tests')
    if request.method == 'GET':
        test = Test.objects.get(pk=pk)
        context = {
            'test': test,
            'first_question': Question.objects.get(test=test, question_num=1).pk
        }
        return render(request, 'testing/testing.html', context)

def TestingUser(request, pk, q_pk):
    if request.method == 'GET':
        test = Test.objects.get(pk=pk) 
        question = Question.objects.get(pk=q_pk)

        context = {
            'test_name': test.name,
            'question': question,
            'answers': Answer.objects.filter(question=question),
            }
        return render(request, 'testing/testing_process.html', context)


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
        return render(request, 'testing/signup.html', {'form': form,})


def LoginUser(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'testing/signin.html', {'message': 'Please enter the correct username and password.'})
    else:
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in.')
        else:
            return render(request, 'testing/signin.html')


def MainPage(request):
    if request.method == "POST":
        redir = request.POST['send_to'].lower()
        return HttpResponseRedirect(f'/{redir}/')
    elif request.method == "GET":
        return render(request, 'testing/main_page.html')
    else:
        return render(request, 'testing/main_page.html')
