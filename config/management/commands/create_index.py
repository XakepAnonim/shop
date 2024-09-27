# from django.core.management.base import BaseCommand
#
# from apps.products.search import ProductIndex
#
#
# class Command(BaseCommand):
#     help = 'Create Elasticsearch index for Product'
#
#     def handle(self, *args, **kwargs):
#         self.stdout.write('Creating the index...')
#         ProductIndex.init()
#         self.stdout.write(self.style.SUCCESS('Index created successfully!'))
