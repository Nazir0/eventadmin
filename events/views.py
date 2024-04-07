from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event
from eventadmin import settings
from participation.models import Participation

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('home')
        else:
            return render(request, 'events/create_event.html', {'form': form})
    else:
        form = EventForm()
        return render(request, 'events/create_event.html', {'form': form})

def add_participant(request):
    if request.method == 'POST':
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=form.cleaned_data.get('event_id'))
    else:
        form = AddParticipantForm()
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants, 'form': form})


@login_required
def show_participants(event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Participation.objects.filter(event=event)
    return participants
