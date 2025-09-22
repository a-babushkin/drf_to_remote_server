from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializer import CourseSerializer, LessonSerializer
from materials.tasks import mail_update_course
from users.permissions import IsModerator, IsOwner


# ===== Секция курсов ===============================================
class CourseViewSet(ModelViewSet):
    """Контроллер для работы с курсами"""

    queryset = Course.objects.all().order_by("title")
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Метод делающий владельцем новой записи текущего пользователя"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Метод устанавливающий права доступа для различных запросов"""
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        updated_course.save()
        mail_update_course.delay(updated_course.id)


# ===== Секция уроков ===============================================
class LessonCreateApiView(CreateAPIView):
    """Контроллер создания новой записи урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        """Метод делающий владельцем новой записи текущего пользователя"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    """Контроллер просмотра списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Контроллер просмотра отдельной записи урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер изменения отдельной записи урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    """Контроллер удаления отдельной записи урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)


# ===== Секция подписок ===============================================
class SubscribeUnsubscribe(APIView):
    """Контроллер установки/удалении подписки"""

    def post(self, request, pk):
        """Метод обрабатывающий POST запрос для подписки"""
        user = request.user
        course = get_object_or_404(Course, pk=pk)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена."

        return Response({"message": message}, status=status.HTTP_200_OK)
