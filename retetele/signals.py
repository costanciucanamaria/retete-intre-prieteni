# https://docs.djangoproject.com/en/6.0/topics/signals/

import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Retete


@receiver(pre_save, sender=Retete)
def my_signal_pre_save(sender, instance: Retete, **kwargs):
    print("Salvare Reteta!.")

@receiver(pre_delete, sender=Retete)
def cleanup_image(sender, instance: Retete, **kwargs):
    if instance.poza is not None:
        try:
            if os.path.isfile(instance.poza.path):
                os.remove(instance.poza.path)
        except ValueError as e:
            pass