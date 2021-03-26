from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

from .models import Test, Question, Answer, UserTest

def get_quesiton_in_progress_or_create(test_pk: int, username: str) -> int:
    test = Test.objects.get(pk=test_pk)
    user = User.objects.get(username=request.user.username)
    
    if not UserTest.objects.filter(user=user, test_in_process=test):
        user_test = UserTest(user=user, test_in_process=test)
        user_test.save()
    
    return user_test.question_in_process
