from django.contrib import admin
from .models import Course, Topic, StudentProgress, Subtopic

class TopicInline(admin.TabularInline):
    model = Topic

class CourseAdmin(admin.ModelAdmin):
    inlines = [TopicInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Subtopic)
admin.site.register(StudentProgress)
