# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from fiesta_core.apps.blog.models import News
from django.core.management.base import BaseCommand
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        events_list = News.objects.all().filter(is_archive=False, type=3)
        date = datetime.date.today()
        for event in events_list:
            if event.deadline_date:
                if event.deadline_date.date() < date:
                    event.is_archive = True
                    event.save()
            elif event.event_date and event.event_date.date() < date:
                event.is_archive = True
                event.save()
        self.stdout.write("done")
