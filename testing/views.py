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

    def get(self, request, t_pk, *args, **kwargs):
        test = Test.objects.get(pk=t_pk)
        return render(request, 'testing/testing.html', {'test': test})

    def post(self, request, t_pk, *args, **kwargs):
        question_num = get_quesiton_in_progress_or_create(test_pk=t_pk, username=request.user.username)
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

    def get(self, request, t_pk, *args, **kwargs):
        username = request.user.username
        score = get_score_of_completed_test(t_pk, username)
        complete_test(t_pk, username)

        return render(request, 'testing/completed.html', score)

    def post(self, request, t_pk, *args, **kwargs):
        pass



class LoginUserView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/signin.html', {'is_auth': request.user.is_authenticated})

    def post(self, request, *args, **kwargs):
        attempt = try_to_login_user(username=request.POST['username'], raw_password=request.POST['password'], request=request)

        if attempt:
            return HttpResponseRedirect('/')
        else:
            context = {'is_auth': request.user.is_authenticated, 'message': 'Please enter the correct username and password.'}
            return render(request, 'testing/signin.html', context)



class RegisterUserView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/signup.html', {'form': UserCreationForm()})

    def post(self, request, *args, **kwargs):
        uploaded_form = UserCreationForm(request.POST)
        
        if try_to_register_user(form=uploaded_form):
            return HttpResponseRedirect('/')
        else:
            return render(request, 'testing/signup.html', {'form': UserCreationForm()})
    

class LogoutUserView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/logout.html', {'username': request.user.username})
    
    def post(self, request, *args, **kwargs):
        
        if request.POST['logout'] == "Yes":
            logout_user(request)
        return HttpResponseRedirect('/')


# doesn't work properly, probably will be deleted because it wasn't in TD.
class DeleteUserView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, u_pk, *args, **kwargs):
        if request.user.username == User.objects.get(pk=u_pk).username:
            context = {'username': request.user.username}
            return render(request, 'testing/delete_user.html', context)
        else:
            context = {'access_denied': True}
            return render(request, 'testing/delete_user.html', context)
            
    def post(self, request, u_pk, *args, **kwargs):
        if request.POST['delete'] == "Yes":
            user = User.objects.get(pk=u_pk)
            user.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


