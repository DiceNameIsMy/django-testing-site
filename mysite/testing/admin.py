from django.contrib import admin

from .models import Test, Question, Answer
# Register your models here.

class AnswersInline(admin.StackedInline):
    model = Answer
    extra = 4

class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 10

class TestsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name', 'description',]}),
    ]
    inlines = [QuestionsInline]

admin.site.register(Test, TestsAdmin)

