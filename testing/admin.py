from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Test, Question, Answer, UserTest, TestGroup
# Register your models here.

class AnswersInline(admin.TabularInline):
    model = Answer
    extra = 2

class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 1

class TestsInline(admin.StackedInline):
    model = Test
    extra = 0

class UserTestsInline(admin.TabularInline):
    model = UserTest
    extra = 0


class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['text', 'test',]}),
    ]
    inlines = [AnswersInline]


class TestsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name', 'description', 'group', 'questions_amount']}),
    ]
    inlines = [QuestionsInline]


class TestGroupsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name', 'description']})
    ]
    inlines = [TestsInline]


class UserAdmin(BaseUserAdmin):
    inlines = (UserTestsInline,)


admin.site.register(Question, QuestionsAdmin)

admin.site.register(Test, TestsAdmin)

admin.site.register(TestGroup, TestGroupsAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

