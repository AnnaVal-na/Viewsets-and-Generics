from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a default admin user if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS('Default admin user created successfully')
            )
        else:
            self.stdout.write('Admin user already exists')
