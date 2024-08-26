from django.db import models

class Poll(models.Model):
    question_text = models.CharField(max_length=200)
    instruction_text = models.TextField(default='')
    display_summary_statistics = models.BooleanField(default=False)
    def __str__(self):
        return self.question_text

class Response(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')