from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Test, Question, Answer, UserTests
# Register your models here.

class AnswersInline(admin.TabularInline):
    model = Answer
    extra = 2

class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 1

class UserTestsInline(admin.TabularInline):
    model = UserTests
    extra = 0

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['text', 'test',]}),
    ]
    inlines = [AnswersInline]

class TestsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name', 'description', 'questions_amount']}),
    ]
    inlines = [QuestionsInline]

class UserAdmin(BaseUserAdmin):
    inlines = (UserTestsInline,)


admin.site.register(Question, QuestionsAdmin)

admin.site.register(Test, TestsAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

