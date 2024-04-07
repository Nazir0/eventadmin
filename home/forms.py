from django import forms
from events.models import Event
from participation.models import Participation


class AddParticipantForm(forms.ModelForm):
    event_id = forms.IntegerField()
    class Meta:
        model = Participation
        fields = ['participant', 'event']

    def clean_event_id(self):
        event_id = self.cleaned_data.get('event_id')
        if not Event.objects.filter(id=event_id).exists():
            raise forms.ValidationError("Event with this ID does not exist.")
        return event_id

    def save(self, commit=True):
        participant = super().save(commit=False)
        event_id = self.cleaned_data.get('event_id')
        event = Event.objects.get(id=event_id)
        participant.event = event
        if commit:
            participant.save()
        return participant