from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

from .models import TestGroup, Test, Question, Answer, UserTest


def _check_answer_is_correct(question, answers: list) -> bool:
    correct_answers = [str(answer.pk) for answer in Answer.objects.filter(question=question, is_correct=True)]
    
    if correct_answers == sorted(answers):
        return True
    else:
        return False


def get_groups_of_tests():
    return TestGroup.objects.all()


def get_group_of_tests_by_pub_date(group: str):
    group = TestGroup.objects.get(name=group)
    return Test.objects.filter(group=group).order_by('-pub_date')


def get_test_by_pk(t_pk: int):
    return Test.objects.get(pk=t_pk)


def get_tests_by_user(username: str) -> list:
    return [ i for i in Test.objects.filter(creator=User.objects.get(username=username))]


def get_questions(test) -> list:
    questions = Question.objects.filter(test=test).order_by('question_num')
    return [i for i in questions]


def get_quesiton_in_progress_or_create(test_pk: int, username: str) -> int:
    """ Returns question in progress. If there is none in progress, creates one """
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


def get_answers(question) -> list:
    answers = Answer.objects.filter(question=question)
    return [a for a in answers]


def get_question_context(test_obj, question_num_key: int) -> dict:
    """Returns test and quesiton with its answers"""
    question = Question.objects.get(question_num=question_num_key, test=test_obj)
    context = {
        'test_name': test_obj.name,
        'question': question.text,
        'answers': Answer.objects.filter(question=question),
        }

    return context


def _post_answer(question, usertest, answers: list) -> None:
    """Called when user sends his answer/answers to question. If his answers are correct adds +1 to score"""
    
    if _check_answer_is_correct(question=question, answers=answers):
        usertest.score += 1
        usertest.save()


def _is_answer_valid(question, answers: list) -> bool:
    """Checks if user didn't select all answers or none of them"""
    correct_answers_len = len(Answer.objects.filter(question=question)) 
    if len(answers) == correct_answers_len or len(answers) == 0:
        return False
    else: 
        return True


def _check_test_completed(test, usertest, question_num_key: int) -> bool:

    if test.questions_amount != question_num_key:
        usertest.question_in_process += 1
        usertest.save()
        return False
    else:
        return True


def testing_process_post(t_pk, q_pk, username, answers) -> str:
    """called when TestingProcessView gets POST"""
    test = Test.objects.get(pk=t_pk)
    question = Question.objects.get(test=test, question_num=q_pk)

    if not _is_answer_valid(question, answers):
        return 'unvalid'
 
    usertest = UserTest.objects.get(user=User.objects.get(username=username))
    _post_answer(question, usertest, answers)

    if _check_test_completed(test, q_pk, usertest=usertest):
        return 'completed'
    else:
        return 'next'


def end_test(t_pk: int, username: str) -> dict:
    """when test completed delete UserTest object and get score"""
    test = Test.objects.get(pk=t_pk)
    user = User.objects.get(username=username)
    user_test = UserTest.objects.get(user=user, test_in_process=test)
    percentage = str(int(user_test.score) / int(test.questions_amount) * 100)
    
    score = {
        'questions_amount': test.questions_amount,
        'score': user_test.score,
        'percentage': percentage,
    }

    UserTest.objects.get(user=user, test_in_process=test).delete()

    return score


def try_to_login_user(username: str, raw_password: str, request) -> bool:
    user = authenticate(username=username, password=raw_password)

    if user is not None:
        login(request, user)
        return True
    else:
        return False


def try_to_register_user(request, form) -> bool:

    if form.is_valid():
        form.save()
        try_to_login_user(
            username=form.cleaned_data.get('username'), 
            raw_password=form.cleaned_data.get('password1'), 
            request=request)
        return True
    else:
        return False


def logout_user(request):
    logout(request)


def access_to_test(username, test) -> bool:

    if test.creator.username == username:
        return True
    else:
        return False


def is_question_valid(question):

    if len(question) < 5:
        return 'Question should be longer than 5 characters'
    elif len(question) > 200:
        return 'Question should be shorter than 200 characters'
    else:
        if question[-1] != '?':
            return 'Question should have "?" at the end'


def is_answer_valid(answer):

    if not answer:
        return 'Answer should not be empty'
    if len(answer) > 100:
        return 'Answer should be shorter than 100 characters'


def validate_qna(post_data) -> list:
    """ if list is empty data is valid """
    msg = []

    question = post_data['question']
    answers = post_data.getlist('answer_text')

    q_msg = is_question_valid(question)
    a_msg = [is_answer_valid(a) for a in answers]

    if q_msg:
        msg.append(q_msg)
    for m in a_msg:
        if m:
            msg.append(m)

    return msg

