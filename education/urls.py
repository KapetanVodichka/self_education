from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LessonViewSet, CourseViewSet, TestViewSet, QuestionViewSet, SubmitAnswersAPIView


router = DefaultRouter()
router.register(r'lessons', LessonViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit-answers/', SubmitAnswersAPIView.as_view(), name='submit-answers'),
]
