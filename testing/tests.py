from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate

from .models import TestGroup, Test, Question, Answer, UserTest
from .services import *


class AuthTest(TestCase):
    """ Created by following tutorial """

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user', password='DjangoPass_User', email='test@example.com')
        self.user.save()
    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test_user', password='DjangoPass_User')
        self.assertTrue(user is not None and user.is_authenticated)
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='DjangoPass_User')
        self.assertFalse(user is not None and user.is_authenticated)
    def test_wrong_password(self):
        user = authenticate(username='test_user', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class MainServicesTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user', password='DjangoPass_User', email='test@example.com')
        self.user.save()

        self.test_group = TestGroup(name='tg_name', description='tg_desc')
        self.test_group.save()

        self.test = Test(
            name='test_name',
            description='test_description',
            group=self.test_group,
            questions_amount=1,
            creator=self.user,
        )
        self.test.save()

        self.question = Question(test=self.test, text='question_text', question_num=1)
        self.question.save()

        self.answer1 = Answer(question=self.question, text='cor_answer1_text', is_correct=True)
        self.answer1.save()
        self.answer2 = Answer(question=self.question, text='wr_answer2_text', is_correct=False)
        self.answer2.save()

        self.user_test = UserTest(pk=1, user=self.user, test_in_process=self.test)

    def tearDown(self):
        self.test.delete()
        self.user.delete()
        self.test_group.delete()
        self.question.delete()
        self.answer1.delete()
        self.answer2.delete()
        self.user_test.delete()

    def test_get_groups_of_tests(self):
        groups = [group for group in get_groups_of_tests()]
        self.assertEqual(groups, [self.test_group])


        
    

    