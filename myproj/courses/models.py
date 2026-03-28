from django.db import models


class Course(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	def __str__(self) -> str:
		return self.title


class Question(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
	text = models.CharField(max_length=500)

	def __str__(self) -> str:
		return f"{self.course.title}: {self.text[:60]}"


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
	text = models.CharField(max_length=300)
	is_correct = models.BooleanField(default=False)

	def __str__(self) -> str:
		return self.text


class Submission(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
	submitted_at = models.DateTimeField(auto_now_add=True)
	# Map of question id -> selected choice id
	selected_choices = models.JSONField(default=dict, blank=True)
	score = models.PositiveIntegerField(default=0)
	total_questions = models.PositiveIntegerField(default=0)

	def __str__(self) -> str:
		return f"Submission #{self.pk} - {self.course.title}"

	@property
	def percentage(self) -> float:
		if self.total_questions == 0:
			return 0.0
		return (self.score / self.total_questions) * 100
