from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from education.models import Course, Lesson, Test, Question


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.teacher = User.objects.create(email='teacher', is_staff=True, role=User.TEACHER)
        self.client.force_authenticate(user=self.teacher)

    def test_list_courses(self):

        response = self.client.get('/courses/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_course(self):
        data = {
            'title': 'Test Course',
            'description': 'Course for testing',
        }

        response = self.client.post('/courses/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Course.objects.filter(title='Test Course').exists()
        )

    def test_retrieve_course(self):
        course = Course.objects.create(title='Test Course', description='Course for testing')

        response = self.client.get(f'/courses/{course.pk}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.teacher = User.objects.create(email='teacher', is_staff=True, role=User.TEACHER)
        self.client.force_authenticate(user=self.teacher)
        self.course = Course.objects.create(title='Test Course', description='Course for testing')

    def test_create_lesson(self):
        data = {
            'title': 'Test Lesson',
            'description': 'Test',
            'course': self.course.id
        }

        response = self.client.post('/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson', course=self.course)

        response = self.client.get(f'/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons(self):
        Lesson.objects.create(title='Lesson 1', description='Description 1', course=self.course)
        Lesson.objects.create(title='Lesson 2', description='Description 2', course=self.course)

        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


class QuestionViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.teacher = User.objects.create(email='teacher', is_staff=True, role=User.TEACHER)
        self.client.force_authenticate(user=self.teacher)

        self.course = Course.objects.create(title='Test Course', description='Course for testing')
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson', course=self.course)
        self.test = Test.objects.create(lesson=self.lesson)

        self.question_data = {
            'text': 'What is the capital of France?',
            'correct_answer': 'Paris',
            'test': self.test.id
        }

    def test_create_question(self):
        response = self.client.post(reverse('question-list'), self.question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_question(self):
        test = Test.objects.create(lesson=self.lesson)

        self.question_data['test'] = test

        question = Question.objects.create(**self.question_data)

        response = self.client.get(reverse('question-detail', args=[question.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text', response.data)


class SubmitAnswersAPIViewTestCase(APITestCase):

    def setUp(self) -> None:
        self.student = User.objects.create(email='student', is_staff=False, role=User.STUDENT)
        self.client.force_authenticate(user=self.student)

        self.course = Course.objects.create(title='Test Course', description='Course for testing')
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson', course=self.course)
        self.test = Test.objects.create(lesson=self.lesson)

        self.question_data = {
            'text': 'What is the capital of France?',
            'correct_answer': 'Paris',
            'test': self.test  # передаем экземпляр объекта Test, а не его id
        }

        self.question = Question.objects.create(**self.question_data)

    def test_submit_answers(self):
        answers_data = [
            {'question': self.question.id, 'answer': 'Paris'},
        ]

        data = {
            'test': self.test.id,
            'answers': answers_data,
        }

        response = self.client.post('/submit-answers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_data = response.data
        self.assertEqual(result_data['test_id'], self.test.id)
        self.assertTrue(len(result_data['answers']) > 0)
        self.assertTrue(result_data['answers'][0]['correct'])
