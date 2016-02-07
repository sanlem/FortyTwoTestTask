from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def edit_link(obj):

    content_types = ContentType.objects.get_for_model(obj.__class__)
    return reverse('admin:%s_%s_change' % (content_types.app_label,
                   content_types.name), args=(obj.id,))
