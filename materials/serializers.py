from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidator(field="video_link")]


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_is_subscribed(self, course):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(course=course, user=user).exists()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
