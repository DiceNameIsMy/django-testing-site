from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

from .services import *


class MainPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/main_page.html')


class GroupsOfTestsView(LoginRequiredMixin, View): 
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        """ sends all groups of tests """
        return render(request, 'testing/groups.html', {'groups': get_groups_of_tests})
    

class GroupTestsView(LoginRequiredMixin, View):
    login_url='/signin/'
    
    def get(self, request, group_slug, *args, **kwargs):
        """ returns all tests of group """
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
        test = get_test_by_pk(t_pk)
        context = get_question_context(test_obj=test, question_num_key=q_pk)
        return render(request, 'testing/testing_process.html', context)
        
    def post(self, request, group_slug, t_pk, q_pk, *args, **kwargs): # it can be done better
        answers = request.POST.getlist('answers')
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
        score = end_test(t_pk, username)

        return render(request, 'testing/completed.html', score)

    def post(self, request, t_pk, *args, **kwargs):
        pass


class LoginUserView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'is_auth': request.user.is_authenticated, 
            'next': request.GET.get('next', ''),
        }
        return render(request, 'testing/signin.html', context)

    def post(self, request, *args, **kwargs):
        attempt_to_login = try_to_login_user(username=request.POST['username'], raw_password=request.POST['password'], request=request)

        if attempt_to_login:
            print(request.POST['next'])
            return HttpResponseRedirect(f"{ request.POST['next']}")
        else:
            context = {'is_auth': request.user.is_authenticated, 'message': 'Please enter the correct username and password.'}
            return render(request, 'testing/signin.html', context)


class RegisterUserView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'testing/signup.html', {'form': UserCreationForm()})

    def post(self, request, *args, **kwargs):
        uploaded_form = UserCreationForm(request.POST)
        
        if try_to_register_user(request=request, form=uploaded_form):
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


class UserPageView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        context = {
            "username": request.user.username,
            "user_created_tests": get_tests_by_user(request.user.username),
        }
        return render(request, 'testing/user_page.html', context=context)


class ManageTestsView(LoginRequiredMixin, View):
    login_url='/signin/'

    def get(self, request, *args, **kwargs):
        user_created_tests = get_tests_by_user(request.user.username)
        return render(request, 'testing/manage_tests.html', context={'user_created_tests': user_created_tests})


class TestDetailView(LoginRequiredMixin, View): # raw view
    login_url='/signin/'

    def get(self, request, t_pk, *args, **kwargs):
        test = get_test_by_pk(t_pk)

        if access_to_test(request.user.username, test):
            questions = get_questions(test)
            questions_w_answers = [(q, get_answers(q)) for q in questions]

            context = {
                'name': test.name,
                'description': test.description,
                'group': test.group,
                'pub_date': test.pub_date,
                'questions_w_answers': questions_w_answers,
                'message': args,
            }
            return render(request, 'testing/test_detail.html', context=context)
        else:
            return render(request, 'testing/access_denied.html')
    
    def post(self, request, t_pk, *args, **kwargs):

        post_data = {
            'q_text': request.POST['question'],
            'q_pk': request.POST['q_pk'],
            'answers': set(zip(request.POST.getlist('answer_text'), request.POST.getlist('a_pk'))), 
        }

        if 'is_cor' in request.POST:
            post_data['cor_answers_pk'] = request.POST.getlist('is_cor')

        error_msg = validate_qna(post_data)
        
        if not error_msg:
            return HttpResponseRedirect(request.path)
        else:
            return self.get(request, t_pk, error_msg, **kwargs)
