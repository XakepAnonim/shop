from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.elasticsearch.index import ProductDocument
from apps.products.models import Product


@receiver(post_save, sender=Product)
def update_product_index(sender, instance, **kwargs):
    """
    Обновляет индекс Elasticsearch при сохранении модели
    """
    ProductDocument().update(instance)
