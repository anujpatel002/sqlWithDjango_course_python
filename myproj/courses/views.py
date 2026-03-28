from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Submission


def course_list(request: HttpRequest) -> HttpResponse:
	courses = Course.objects.all().order_by('title')
	return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request: HttpRequest, course_id: int) -> HttpResponse:
	course = get_object_or_404(
		Course.objects.prefetch_related('questions__choices'),
		pk=course_id,
	)
	return render(request, 'courses/course_detail.html', {'course': course})


def submit_exam(request: HttpRequest, course_id: int) -> HttpResponse:
	if request.method != 'POST':
		return redirect('courses:course-detail', course_id=course_id)

	course = get_object_or_404(
		Course.objects.prefetch_related('questions__choices'),
		pk=course_id,
	)

	selected_choices: dict[str, int | None] = {}

	for question in course.questions.all():
		answer_key = f'question_{question.id}'
		choice_id_value = request.POST.get(answer_key)
		selected_choice_id = None
		if choice_id_value:
			try:
				selected_choice_id = int(choice_id_value)
			except ValueError:
				selected_choice_id = None

		selected_choices[str(question.id)] = selected_choice_id

	submission = Submission.objects.create(
		course=course,
		selected_choices=selected_choices,
	)

	return redirect('courses:exam-result', submission_id=submission.id)


def exam_result(request: HttpRequest, submission_id: int) -> HttpResponse:
	submission = get_object_or_404(
		Submission.objects.select_related('course').prefetch_related('course__questions__choices'),
		pk=submission_id,
	)

	result_rows = []
	score = 0
	total_questions = submission.course.questions.count()

	for question in submission.course.questions.all():
		selected_choice_id = submission.selected_choices.get(str(question.id))
		selected_choice = None
		if selected_choice_id is not None:
			selected_choice = question.choices.filter(pk=selected_choice_id).first()

		correct_choice = question.choices.filter(is_correct=True).first()
		is_correct = selected_choice is not None and selected_choice.is_correct
		if is_correct:
			score += 1

		result_rows.append(
			{
				'question': question.text,
				'selected_choice': selected_choice.text if selected_choice else None,
				'correct_choice': correct_choice.text if correct_choice else None,
				'is_correct': is_correct,
			}
		)

	if submission.score != score or submission.total_questions != total_questions:
		submission.score = score
		submission.total_questions = total_questions
		submission.save(update_fields=['score', 'total_questions'])

	context = {
		'submission': submission,
		'result_rows': result_rows,
	}
	return render(request, 'courses/exam_result.html', context)
