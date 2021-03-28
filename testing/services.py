from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

from .models import Test, Question, Answer, UserTest


def _check_answer_is_correct(question, answers: list) -> bool:
    correct_answers = [str(answer.pk) for answer in Answer.objects.filter(question=question, is_correct=True)]
    
    if correct_answers == answers:
        return True
    else:
        return False


def get_quesiton_in_progress_or_create(test_pk: int, username: str) -> int:
    """Returns question in progress. If there is none in progress, creates one. It is 1 by default"""
    test = Test.objects.get(pk=test_pk)
    user = User.objects.get(username=username)
    tests_in_process = UserTest.objects.filter(user=user)

    if not tests_in_process:
        user_test = UserTest(user=user, test_in_process=test)
        user_test.save()
        return 1
    elif tests_in_process[0].test_in_process == test:
        return tests_in_process[0].question_in_process
    else:
        tests_in_process[0].delete()
        user_test = UserTest(user=user, test_in_process=test)
        user_test.save()
        return 1


def get_question_context(test_pk: int, question_num_key: int) -> dict:
    """Returns test and quesiton with its answers"""
    test = Test.objects.get(pk=test_pk) 
    question = Question.objects.get(question_num=question_num_key, test=test)
    context = {
        'test_name': test.name,
        'question': question.text,
        'answers': Answer.objects.filter(question=question),
        }

    return context


def post_answer(test , question_num_key: int, usertest, answers: list) -> None:
    """Called when user sends his answer/answers to question. If his answers are correct adds +1 to score"""
    question = Question.objects.get(question_num=question_num_key, test=test)

    if _check_answer_is_correct(question=question, answers=answers):
        usertest.score += 1
        usertest.save()


def validate_answer(test, question_num, answers):
    """Checks if user didn't select all answers or none of them"""
    question = Question.objects.get(test=test, question_num=question_num)
    correct_answers_len = len(Answer.objects.filter(question=question)) 
    if len(answers) == correct_answers_len or len(answers) == 0:
        return False
    else: 
        return True


def check_test_completed(test_pk: int, question_num_key: int, usertest) -> bool:

    if Test.objects.get(pk=test_pk).questions_amount != question_num_key:
        usertest.question_in_process += 1
        usertest.save()
        return False
    else:
        return True


def get_score_of_completed_test(t_pk: int, username: str) -> dict:
    test = Test.objects.get(pk=t_pk)
    user = User.objects.get(username=username)
    user_test = UserTest.objects.get(user=user, test_in_process=test)
    percentage = str(int(user_test.score) / int(test.questions_amount) * 100)
    
    score = {
        'questions_amount': test.questions_amount,
        'score': user_test.score,
        'percentage': percentage,
    }
    return score


def complete_test(t_pk: int, username: str) -> None:
    """Deletes users UserTest object."""
    user = User.objects.get(username=username)
    test = Test.objects.get(pk=t_pk)

    UserTest.objects.get(user=user, test_in_process=test).delete()


def try_to_login_user(username: str, raw_password: str, request) -> bool:
    user = authenticate(username=username, password=raw_password)

    if user is not None:
        login(request, user)
        return True
    else:
        return False


def try_to_register_user(form) -> bool:

    if form.is_valid():
        form.save()
        try_to_login_user(username=form.cleaned_data.get('username'), raw_password=form.cleaned_data.get('password1'))
        return True
    else:
        return False


def logout_user(request) -> None:
    logout(request)

