from django.db import models

# Create your models here.
class Tests(models.Model):
    test_name = models.CharField(max_length=40)
    test_description = models.CharField(max_length=200)

    def __str__(self):
        return self.test_name


class Questions(models.Model):
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    choice1 = models.CharField(max_length=100)
    choice2 = models.CharField(max_length=100)
    choice3 = models.CharField(max_length=100)
    choice4 = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text
