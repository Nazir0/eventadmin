from django.db import models
from django.contrib.auth.models import User
from events.models import Event

from eventadmin import settings


class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('event', 'participant')

    def __str__(self):
        return f'{self.participant.username} - {self.event.title}'
