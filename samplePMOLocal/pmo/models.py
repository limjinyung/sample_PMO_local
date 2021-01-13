from django.db import models


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.name, self.description)


class Developer(models.Model):
    POSITIONS = (
        ('PM', 'Project Manager'),
        ('QA', 'Quality Assurance'),
        ('SD', 'Software Developer'),
    )
    name = models.CharField(max_length=20)
    task = models.ManyToManyField('Task')
    position = models.CharField(max_length=20, choices=POSITIONS, null=True, default=POSITIONS[2][0])

    def __str__(self):
        return '%s %s %s' % (self.name, self.task, self.position)