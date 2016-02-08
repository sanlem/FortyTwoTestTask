from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.contacts.models import ChangeEntry


PROCESS_MODELS = ['User', 'RequestEntry', 'Contacts']


@receiver(post_save, dispatch_uid='nope')
def post_save_processor(sender, **kwargs):
    if sender.__name__ not in PROCESS_MODELS:
        return

    ce = ChangeEntry()
    ce.model_name = sender.__name__
    ce.instance_id = kwargs['instance'].id
    if kwargs['created']:
        ce.action = 'created'
    else:
        ce.action = 'updated'
    ce.save()


@receiver(post_delete, dispatch_uid='nope')
def post_delete_processor(sender, **kwargs):
    if sender.__name__ not in PROCESS_MODELS:
        return

    ce = ChangeEntry()
    ce.model_name = sender.__name__
    ce.instance_id = kwargs['instance'].id
    ce.action = 'deleted'
    ce.save()
