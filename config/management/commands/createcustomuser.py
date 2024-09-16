from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Create a superuser with predefined data'

    def handle(self, *args, **kwargs):
        first_name = 'admin'
        last_name = 'admin'
        phone_number = '78005553535'
        email = 'admin@mail.ru'
        password = 'admin'

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{first_name}" created successfully.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser "{first_name}" already exists.')
            )
