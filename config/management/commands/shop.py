import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        url = 'http://127.0.0.1:8000/api/v1/test/shop/'
        requests.request('GET', url=url)
