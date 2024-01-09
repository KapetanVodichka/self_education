from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        superuser = User.objects.create(email='admin', is_staff=True, is_superuser=True)
        superuser.set_password('admin')
        superuser.save()

        teacher = User.objects.create(email='teacher', is_staff=True, role=User.TEACHER)
        teacher.set_password('teacher')
        teacher.save()

        user = User.objects.create(email='student', is_staff=False, is_superuser=False, role=User.STUDENT)
        user.set_password('student')
        user.save()
