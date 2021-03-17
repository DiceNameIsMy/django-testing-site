from django.contrib import admin

from .models import Test, Question, Answer
# Register your models here.

class AnswersInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 10

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['text', 'test',]}),
    ]
    inlines = [AnswersInline]

class TestsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name', 'description',]}),
    ]
    inlines = [QuestionsInline]

admin.site.register(Question, QuestionsAdmin)

admin.site.register(Test, TestsAdmin)


