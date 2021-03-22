from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect

from .models import Test, Question, Answer, UserTests


class MainPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/main_page.html')

    def post(self, request, *args, **kwargs):
        message = "".join(request.POST['send_to'].lower().split()) 
        return HttpResponseRedirect(f'/{message}/')



class TestsView(View):
    
    def get(self, request, *args, **kwargs):
        context = {'tests': Test.objects.order_by('-pub_date')}
        return render(request, 'testing/tests.html', context)



class TestingPageView(View):

    def get(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/tests')
        test = Test.objects.get(pk=pk)

        return render(request, 'testing/testing.html', {'test': test})

    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/tests')
        
        test = Test.objects.get(pk=pk)
        user = User.objects.get(username=request.user.username) # get user that is logged in
        user_test = UserTests(user=user, test_in_process=test) # create user usertests model
        user_test.save()

        return HttpResponseRedirect('1')



class TestingUserView(View):

    def check_answer(self, question, answers):
        correct_answers = {str(answer.pk) for answer in Answer.objects.filter(question=question, is_correct=True)}
        print(correct_answers, answers)
        if correct_answers == answers:
            return True
        else:
            return False
    
    def get(self, request, pk, q_pk, *args, **kwargs):
        test = Test.objects.get(pk=pk) 
        question = Question.objects.get(pk=q_pk, test=test)
        context = {
            'test_name': test.name,
            'question': question,
            'answers': Answer.objects.filter(question=question),
            }
        return render(request, 'testing/testing_process.html', context)
        
    def post(self, request, pk, q_pk, *args, **kwargs): # it can be done better
        test = Test.objects.get(pk=pk) 
        question = Question.objects.get(pk=q_pk, test=test)
        posted_answers = set(request.POST.getlist('answers'))
        
        user = User.objects.get(username=request.user.username)
        usertest = UserTests.objects.get(user=user)

        if self.check_answer(question, posted_answers):
            usertest.score += 1
        
        if test.questions_amount == q_pk:
            return HttpResponseRedirect(f'/tests/{pk}/completed')   
        else:
            usertest.question_in_process += 1
            usertest.save()
            return HttpResponseRedirect(f'{q_pk + 1}')



class LoginUserView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/signin.html', {'is_auth': request.user.is_authenticated})

    def post(self, request, *args, **kwargs):
        if request.POST['log'] == "Logout":
            logout(request)
        elif request.POST['log'] == "Login":
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'testing/signin.html', {'message': 'Please enter the correct username and password.'})



class RegisterUserView(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'testing/signup.html', {'form': form,})

    def post(self, request, *args, **kwargs):
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
    