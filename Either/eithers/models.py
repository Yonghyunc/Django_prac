from random import choices
from django.db import models

# Create your models here.
class Vote(models.Model):
    title = models.CharField(max_length=30)
    issue_a = models.CharField(max_length=15)
    issue_b = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Comment(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    content = models.TextField()
    PICK_CHOICE = [('issue_a', 'A'), ('issue_b', 'B')]
    pick = models.CharField(max_length=15, choices=PICK_CHOICE, default='issue_a')

    def __str__(self):
        return self.content
