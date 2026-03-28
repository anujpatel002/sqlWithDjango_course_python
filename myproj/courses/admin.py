from django.contrib import admin
from .models import Choice, Course, Question, Submission


class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('text', 'course')
	list_filter = ('course',)
	search_fields = ('text', 'course__title')
	inlines = [ChoiceInline]


class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('title',)
	search_fields = ('title',)
	inlines = [QuestionInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('text', 'question', 'is_correct')
	list_filter = ('is_correct', 'question__course')
	search_fields = ('text', 'question__text', 'question__course__title')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('id', 'course', 'score', 'total_questions', 'submitted_at')
	list_filter = ('course', 'submitted_at')
	readonly_fields = ('submitted_at', 'selected_choices', 'score', 'total_questions')
