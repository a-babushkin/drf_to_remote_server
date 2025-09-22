from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validation_domain


# ===== Секция уроков ===============================================
class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validation_domain])

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonsForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description"]


# ===== Секция курсов ===============================================
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonsForCourseSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        current_user = self.context["request"].user
        return Subscription.objects.filter(user=current_user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]


# ===== Секция подписок ===============================================
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
