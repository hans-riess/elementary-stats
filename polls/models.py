from django.db import models

class Poll(models.Model):
    question_text = models.CharField(max_length=200)

class Response(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)