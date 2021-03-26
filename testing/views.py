from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render 
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect

from .models import Test, Question, Answer, UserTest
from .services import *


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



class TestingPageView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, pk, *args, **kwargs):
        test = Test.objects.get(pk=pk)
        return render(request, 'testing/testing.html', {'test': test})

    def post(self, request, pk, *args, **kwargs):
        question_num = get_quesiton_in_progress_or_create(test_pk=pk, username=request.user.username)
        return HttpResponseRedirect(f'testing/{question_num}')



class TestingProcessView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, t_pk, q_pk, *args, **kwargs):
        context = get_question_context(test_pk=t_pk, question_num_key=q_pk)
        return render(request, 'testing/testing_process.html', context)
        
    def post(self, request, t_pk, q_pk, *args, **kwargs): # it can be done better
        answers = sorted(request.POST.getlist('answers'))
        usertest = UserTest.objects.get(user=User.objects.get(username=request.user.username))
        
        post_answer(test_pk=t_pk, question_num_key=q_pk, usertest=usertest, answers=answers)

        if check_test_completed(test_pk=t_pk, question_num_key=q_pk, usertest=usertest):
            return HttpResponseRedirect(f'/tests/{t_pk}/completed')   
        else:
            return HttpResponseRedirect(f'{q_pk + 1}')



class TestCompletedView(LoginRequiredMixin, View):
    login_url='/signin/'    

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        test = Test.objects.get(pk=pk)
        user_test = UserTest.objects.get(user=user, test_in_process=test)
        percentage = str(int(user_test.score) / int(test.questions_amount) * 100)
        print(percentage)

        context = {
            'score': user_test.score,
            'questions_amount': test.questions_amount,
            'percentage': percentage,
            }
        UserTest.objects.filter(user=user, test_in_process=test).delete()

        return render(request, 'testing/completed.html', context)

    def post(self, request, pk, *args, **kwargs):
        pass



class LoginUserView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/signin.html', {'is_auth': request.user.is_authenticated})

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {'is_auth': request.user.is_authenticated, 'message': 'Please enter the correct username and password.'}
            return render(request, 'testing/signin.html', context)



class RegisterUserView(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'testing/signup.html', {'form': form,})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse('Registration is success!')
        else:
            return HttpResponse('Your form is invalid!')

    

class LogoutUserView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        context = {'username': request.user.username}
        return render(request, 'testing/logout.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.POST['logout'] == "Yes":
            logout(request)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


# doesn't work properly, probably will be deleted because it wasn't in TD.
class DeleteUserView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, pk, *args, **kwargs):
        if request.user.username == User.objects.get(pk=pk).username:
            context = {'username': request.user.username}
            return render(request, 'testing/delete_user.html', context)
        else:
            context = {'access_denied': True}
            return render(request, 'testing/delete_user.html', context)
            
    def post(self, request, pk, *args, **kwargs):
        if request.POST['delete'] == "Yes":
            user = User.objects.get(pk=pk)
            user.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


