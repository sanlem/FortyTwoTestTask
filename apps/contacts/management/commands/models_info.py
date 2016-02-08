from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = "Prints number of each model instances."

    def handle(self, *args, **options):

        models = {}
        for model in get_models():
            models[model] = len(model.objects.all())

        for model, number in models.iteritems():
            out = "%s in database: %s" % (model._meta.module_name, number)
            self.stdout.write(out)
            self.stderr.write('error: ' + out)
