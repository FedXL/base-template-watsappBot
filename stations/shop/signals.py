from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import CartItem

@receiver(post_save, sender=CartItem)
def delete_cart_item_if_quantity_zero(sender, instance, **kwargs):
    if instance.quantity <= 0:
        instance.delete()