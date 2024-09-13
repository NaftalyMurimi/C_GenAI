from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def progress(self, student):
        topics = self.topics.all()
        completed_topics = topics.filter(studentprogress__student=student, studentprogress__completed=True).count()
        total_topics = topics.count()
        if total_topics == 0:
            return 0
        return (completed_topics / total_topics) * 100
    def __str__(self):
        return self.name
class Topic(models.Model):
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def progress(self, student):
        progress = StudentProgress.objects.filter(student=student, topic=self).first()
        return progress.completed if progress else False

class StudentProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,null=True)
    completed = models.BooleanField(default=False)