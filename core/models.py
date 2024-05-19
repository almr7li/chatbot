from django.db import models
from uuid import uuid4

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chatbot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    key = models.CharField(max_length=36, editable=True)
    collection_id = models.CharField(blank=True, max_length=36)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbots')
    created_at = models.DateTimeField(auto_now_add=True)

class QuestionAnswer(models.Model):
    chatbot = models.ForeignKey(Chatbot, related_name='question_answers', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        unique_together = ('chatbot', 'question')

