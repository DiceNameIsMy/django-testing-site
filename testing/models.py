from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models


class TestGroup(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    group = models.ForeignKey(TestGroup, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateField(default=now)
    questions_amount = models.SmallIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, default=User.objects.get(pk=1))

    def __str__(self):
        return f'name:{self.name}, creator:{self.creator}'


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    question_num = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserTest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    test_in_process = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    question_in_process = models.SmallIntegerField(default=1)
    score = models.SmallIntegerField(default=0)
