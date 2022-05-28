from django.db import models
import datetime
from django.contrib import admin
from django.utils import timezone


# Create your models here.


class PollQuestion(models.Model):
    question = models.CharField(max_length=300)
    question_date = models.DateTimeField('publication date for this poll')

    @admin.display(
        boolean=True,
        ordering='question_date',
        description='published recently'
    )
    def was_published_recently(self):
        current_time = timezone.now()
        return current_time - datetime.timedelta(days=1) <= self.question_date <= current_time

    objects = models.Manager()

    def __str__(self):
        return self.question


class PollAnswer(models.Model):
    poll_question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE, related_name="choices")
    answer = models.CharField(max_length=300)
    total_votes = models.IntegerField()

    def __str__(self):
        return self.answer
