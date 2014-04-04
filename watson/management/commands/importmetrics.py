import csv
from django.core.management.base import BaseCommand, CommandError
from watson import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Command requires file name on input')
        self.stdout.write('Loading file: %s' % args[0])
        with open(args[0], 'r') as csvfile:
            file_reader = csv.reader(csvfile)
            for line in file_reader:
                model = getattr(models, line[0])
                if not model.objects.filter(name=line[2]):
                    new = model()
                    if line[1]:
                        setattr(new, 'category', line[1])
                    setattr(new, 'name', line[2])
                    self.stdout.write('%s added' % new)
                    new.save()