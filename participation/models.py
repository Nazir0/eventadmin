from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event


class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participations')
    participant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='participations')


    class Meta:
        unique_together = ('event', 'participant')

    def __str__(self):
        return f'{self.participant.username} - {self.event.name}'
