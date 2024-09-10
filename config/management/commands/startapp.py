from django.core.management.commands.startapp import Command as StartAppCommand
import os


class Command(StartAppCommand):
    print(1)
    def handle(self, *args, **options):
        super().handle(*args, **options)
        app_name = options['name']
        app_dir = os.path.join(os.getcwd(), app_name)

        # Создание папки services
        test_dir = os.path.join(app_dir, 'services')
        os.makedirs(test_dir, exist_ok=True)

        # Создание папки test
        test_dir = os.path.join(app_dir, 'test')
        os.makedirs(test_dir, exist_ok=True)

        # Создание файлов test_data.py, tests_models.py и tests_views.py
        with open(os.path.join(test_dir, 'test_data.py'), 'w') as f:
            f.write('# test_data\n')
        with open(os.path.join(test_dir, 'tests_models.py'), 'w') as f:
            f.write('from django.test import TestCase\n')
        with open(os.path.join(test_dir, 'tests_views.py'), 'w') as f:
            f.write('from django.test import TestCase\n')
        os.path.join(test_dir, '__init__.py')

        # Создание файла serializers.py
        with open(os.path.join(app_dir, 'serializers.py'), 'w') as f:
            f.write('from rest_framework import serializers')

        # Создание файла urls.py
        with open(os.path.join(app_dir, 'urls.py'), 'w') as f:
            f.write('from django.urls import path')
