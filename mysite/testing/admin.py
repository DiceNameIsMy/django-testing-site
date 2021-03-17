from django.contrib import admin

from .models import Questions, Tests
# Register your models here.

class QuestionsInline(admin.StackedInline):
    model = Questions
    extra = 10

class TestsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['test_name', 'test_description',]}),
    ]
    inlines = [QuestionsInline]

admin.site.register(Tests, TestsAdmin)

