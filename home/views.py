from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from events.models import Event
from .forms import AddParticipantForm
from django.contrib.auth import logout
from participation.models import Participation

@login_required
def list_events(request):
    events = Event.objects.filter(creator=request.user).order_by('date')
    return render(request, 'home/list_events.html', {'events': events, 'username': request.user.username})

def event_detail(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    participations = Participation.objects.filter(event=event)

    if request.method == 'POST':
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event_id)
    else:
        form = AddParticipantForm(initial={'event_id': event_id})

    return render(request, 'home/detail_event.html', {'event': event, 'participations': participations, 'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
