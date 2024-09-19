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

    def set_progress(self, student, progress):
        # Update or create StudentProgress record for the course
        progress_record, created = StudentProgress.objects.get_or_create(student=student, topic__course=self)
        progress_record.completed_percentage = progress
        progress_record.save()

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
    class Meta:
        unique_together = ('student', 'topic')
    def __str__(self):
        return f"{self.student.username} - {self.topic.name} - {'Completed' if self.completed else 'Incomplete'}"




