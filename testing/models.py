from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    pub_date = models.DateField(default=now)
    questions_amount = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


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


class UserTests(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    test_in_process = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    question_in_process = models.SmallIntegerField(default=1)
    score = models.SmallIntegerField(default=0)


