from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render 
from django.views import View
from django.http import HttpResponseRedirect

from .services import *


class MainPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/main_page.html')

    def post(self, request, *args, **kwargs):
        """transforms post value and redirects to there"""
        message = "".join(request.POST['send_to'].lower().split()) 
        return HttpResponseRedirect(f'/{message}/')



class GroupOfTestsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/groups.html', {'groups': get_groups_of_tests})
    

class GroupTestsView(View):
    
    def get(self, request, group_slug, *args, **kwargs):
        context = {'tests': get_group_of_tests_by_pub_date(group=group_slug)}
        return render(request, 'testing/group_tests.html', context)



class TestingPageView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, t_pk, *args, **kwargs):
        return render(request, 'testing/testing.html', {'test': get_test_by_pk(t_pk)})

    def post(self, request, t_pk, *args, **kwargs):
        question_num = get_quesiton_in_progress_or_create(test_pk=t_pk, username=request.user.username)
        return HttpResponseRedirect(f'testing/{question_num}')



class TestingProcessView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, t_pk, q_pk, *args, **kwargs):
        context = get_question_context(test_pk=t_pk, question_num_key=q_pk)
        return render(request, 'testing/testing_process.html', context)
        
    def post(self, request, group_slug, t_pk, q_pk, *args, **kwargs): # it can be done better
        answers = sorted(request.POST.getlist('answers'))
        username = request.user.username

        result = testing_process_post(t_pk, q_pk, username, answers)

        if result == 'unvalid':
            return HttpResponseRedirect(str(q_pk))
        elif result == 'completed':
            return HttpResponseRedirect(f'/tests/{group_slug}/{t_pk}/completed')   
        else:
            return HttpResponseRedirect(str(q_pk+1))



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


class ManageTestsView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        user_created_tests = [i for i in get_tests_by_user(request.user.username)]
        return render(request, 'testing/manage_tests.html', context={'tests': user_created_tests})