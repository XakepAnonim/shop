# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=Product)
# def update_product_index(sender, instance, **kwargs):
#     product_index = ProductIndex(
#         meta={'id': instance.uuid},
#         uuid=instance.uuid,
#         name=instance.name,
#         description=instance.description,
#         price=instance.price,
#     )
#     product_index.save()
