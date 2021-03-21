from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
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
    test = Test.objects.get(pk=pk)

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/tests')
    if request.method == 'GET':
        context = {
            'test': test,
            'first_question': Question.objects.get(test=test, question_num=1).pk,
        }
        return render(request, 'testing/testing.html', context)
    elif request.method == 'POST':
        if request.POST['start'] == 'Start':
            user = User.objects.get(username=request.user.username) # get user that is logged in
            user_test = UserTests(user=user, test_in_process=test) # create users usertests model
            user_test.save()
            return HttpResponseRedirect('1')


def TestingUser(request, pk, q_pk):
    test = Test.objects.get(pk=pk) 
    question = Question.objects.get(question_num=q_pk, test=test)

    if request.method == "POST":
        # contains pk's of correct answers
        correct_answers_pk = [str(answer.pk) for answer in Answer.objects.filter(question=question, is_correct=True)] 
        # contains pk's of posted answers
        posted_answers = request.POST.getlist('answers')
        
        user = User.objects.get(username=request.user.username)
        usertest = UserTests.objects.get(user=user)
        usertest.question_in_process += 1

        for answer in correct_answers_pk: 
            if answer in posted_answers: #if correct answer is in posted answers delete it from there
                posted_answers.remove(answer)
            else: # if correct answer is not in posted answers break loop and head to the next question
                break
        else: #if all answers was correct
            if posted_answers == []: #if no answers left(all correct answers was deleted)
                usertest.score += 1 # add one point to user score
        
        usertest.save()

        try:
            return HttpResponseRedirect(f'{q_pk + 1}')
        except Exception:
            return HttpResponseRedirect(f'/tests/{pk}/completed')

    elif request.method == 'GET':
        question = Question.objects.get(pk=q_pk, test=test)
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
            return HttpResponse('Your form is invalid!')
    else:
        form = UserCreationForm()
        return render(request, 'testing/signup.html', {'form': form,})


def LoginUser(request):
    if request.method == "POST":
        if str(request.POST['log']) == "Logout":
            logout(request)
        elif request.POST['log'] == "Login":
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'testing/signin.html', {'message': 'Please enter the correct username and password.'})
        else:
            return HttpResponseRedirect('Fuck')

    if request.user.is_authenticated:
        return render(request, 'testing/signin.html', {'is_auth': True})
    else:
        return render(request, 'testing/signin.html', {'is_auth': False})


def MainPage(request):
    if request.method == "POST":
        # make posted message lowercase and delete spaces
        message = "".join(request.POST['send_to'].lower().split()) 
        return HttpResponseRedirect(f'/{message}/')
    elif request.method == "GET":
        return render(request, 'testing/main_page.html')
    else:
        return render(request, 'testing/main_page.html')
