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
    """Returns question in progress. It is 1 by default"""
    test = Test.objects.get(pk=test_pk)
    user = User.objects.get(username=username)
    tests_in_process = UserTest.objects.filter(user=user, test_in_process=test)

    if not tests_in_process:
        user_test = UserTest(user=user, test_in_process=test)
        user_test.save()
        return 1
    
    return tests_in_process[0].question_in_process


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


def post_answer(test_pk: int, question_num_key: int, usertest, answers: list) -> None:
    question = Question.objects.get(question_num=question_num_key, test=Test.objects.get(pk=test_pk))

    if _check_answer_is_correct(question=question, answers=answers):
        usertest.score += 1
        usertest.save()


def check_test_completed(test_pk: int, question_num_key: int, usertest):

    if Test.objects.get(pk=test_pk).questions_amount != question_num_key:
        usertest.question_in_process += 1
        usertest.save()
        return False
    else:
        return True



