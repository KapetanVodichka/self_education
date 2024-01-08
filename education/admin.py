from django.contrib import admin
from .models import Course, Lesson, Test, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Test, TestAdmin)
admin.site.register(Question)
