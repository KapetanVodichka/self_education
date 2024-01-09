from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Test, Question
from .permissions import IsTeacher, IsReadOnly
from .serializers import CourseSerializer, LessonSerializer, LessonCreateSerializer, TestCreateSerializer, \
    CourseCreateSerializer, TestSerializer, QuestionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsTeacher | IsReadOnly)]

    def create(self, request, *args, **kwargs):
        serializer = LessonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, (IsTeacher | IsReadOnly)]

    def create(self, request, *args, **kwargs):
        serializer = CourseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, (IsTeacher | IsReadOnly)]

    def create(self, request, *args, **kwargs):
        serializer = TestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, (IsTeacher | IsReadOnly)]

    def create(self, request, *args, **kwargs):
        test_id = request.data.get('test')
        test = Test.objects.get(id=test_id)

        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(test=test)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmitAnswersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        test_id = request.data.get('test')
        answers_data = request.data.get('answers')

        # Логика проверки ответов
        result_data = {'test_id': test_id, 'answers': []}

        for answer_data in answers_data:
            question_id = answer_data.get('question')
            student_answer = answer_data.get('answer')
            question = get_object_or_404(Question, id=question_id)

            is_correct = student_answer == question.correct_answer
            result_data['answers'].append({
                'question_id': question_id,
                'student_answer': student_answer,
                'correct_answer': question.correct_answer,
                'correct': is_correct,
            })

        return Response(result_data, status=status.HTTP_200_OK)
