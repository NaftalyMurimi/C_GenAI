from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def progress(self, student):
        topics = self.topics.all()
        total_subtopics = Subtopic.objects.filter(topic__in=topics).count()
        completed_subtopics = Subtopic.objects.filter(
            topic__in=topics,
            studentprogress__student=student,
            studentprogress__completed=True
        ).count()
        if total_subtopics == 0:
            return 0
        return (completed_subtopics / total_subtopics) * 100

    def __str__(self):
        return self.name


class Topic(models.Model):
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def progress(self, student):
        subtopics = self.subtopics.all()
        total_subtopics = subtopics.count()
        completed_subtopics = subtopics.filter(
            studentprogress__student=student,
            studentprogress__completed=True
        ).count()
        if total_subtopics == 0:
            return 0
        return (completed_subtopics / total_subtopics) * 100

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def progress(self, student):
        progress = StudentProgress.objects.filter(student=student, subtopic=self).first()
        return progress.completed if progress else False

    def mark_complete(self, student):
        # Mark the subtopic as complete for the student
        progress, created = StudentProgress.objects.get_or_create(student=student, subtopic=self)
        progress.completed = True
        progress.save()

    def __str__(self):
        return self.name


class StudentProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'topic', 'subtopic')

    def __str__(self):
        topic_name = self.topic.name if self.topic else "No Topic"
        subtopic_name = self.subtopic.name if self.subtopic else "No Subtopic"
        return f"{self.student.username} - {topic_name} - {subtopic_name} - {'Completed' if self.completed else 'Incomplete'}"
