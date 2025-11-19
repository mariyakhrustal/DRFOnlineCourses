from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
        # fields = ("name", "description", "image", "lessons_count")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
