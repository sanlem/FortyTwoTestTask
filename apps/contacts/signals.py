from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.contacts.models import ChangeEntry


IGNORED_MODELS = ['ChangeEntry']


@receiver(post_save, dispatch_uid='nope')
def post_save_processor(sender, **kwargs):
    if sender.__name__ in IGNORED_MODELS:
        return
    ce = ChangeEntry()
    ce.model_name = sender.__name__
    # session objects have no id. Saving user's id.
    if sender.__name__ == 'Session':
        uid = kwargs['instance'].get_decoded().get('_auth_user_id')
        if not uid:
            uid = 0
        ce.instance_id = uid
    else:
        ce.instance_id = kwargs['instance'].id
    if kwargs['created']:
        ce.action = 'created'
    else:
        ce.action = 'updated'
    ce.save()


@receiver(post_delete, dispatch_uid='nope')
def post_delete_processor(sender, **kwargs):
    if sender.__name__ in IGNORED_MODELS:
        return
    ce = ChangeEntry()
    ce.model_name = sender.__name__
    # session objects have no id. Saving user's id.
    if sender.__name__ == 'Session':
        uid = kwargs['instance'].get_decoded().get('_auth_user_id')
        if not uid:
            uid = 0
        ce.instance_id = uid
    else:
        ce.instance_id = kwargs['instance'].id
    ce.action = 'deleted'
    ce.save()
