from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)


class Developer(models.Model):
    POSITIONS = (
        ('PM', 'Project Manager'),
        ('QA', 'Quality Assurance'),
        ('SD', 'Software Developer'),
    )
    name = models.CharField(max_length=20)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=20, choices=POSITIONS, null=True, default=POSITIONS[2][0])