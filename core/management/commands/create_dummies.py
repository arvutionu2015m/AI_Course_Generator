from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, Module, Chapter, Quiz, Assignment

class Command(BaseCommand):
    help = "Loo 3 täiuslikku testkursust teemal 'python env' kasutajale demo"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username="demo")
        if created:
            user.set_password("demo123")
            user.save()

        Course.objects.filter(user=user, topic__icontains="python env").delete()  # puhastus

        for i in range(1, 4):
            course = Course.objects.create(user=user, topic=f"Python env praktika {i}")

            module = Module.objects.create(course=course, title=f"Virtuaalkeskkondade loomine {i}")

            chapter = Chapter.objects.create(
                module=module,
                title=f"Peatükk {i}: venv & pipenv",
                content=(
                    f"Selles peatükis õpime looma virtuaalkeskkondi Pythonis. "
                    f"Käsud: `python3 -m venv venv`, `source venv/bin/activate` ja `pip install ...`."
                )
            )

            Quiz.objects.create(
                chapter=chapter,
                question="Mis on vahe venv ja pipenv vahel?",
                answer="venv on standardne tööriist, pipenv lisab sõltuvuste halduse ja lukustamise funktsionaalsuse."
            )

            Assignment.objects.create(
                chapter=chapter,
                instruction="Loo virtuaalkeskkond projektile ja installi sinna Django. Kirjelda protsessi samm-sammult."
            )

        self.stdout.write(self.style.SUCCESS("3 dummykursust loodud teemal 'python env' kasutajale demo"))
