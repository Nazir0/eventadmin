from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event
from eventadmin import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from accounts.models import CustomUser
from .serializers import EventSerializer
from participation.models import Participation
from rest_framework import status


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

@api_view(['GET'])
def user_events(request, username):
    """
    Retrieve all events for a specific user.
    """
    events = Event.objects.filter(creator__username=username).order_by('date')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_api(request, event_id=None, username=None):
    if request.method == 'GET':
        if username:
            events = Event.objects.filter(creator__username=username).order_by('date')
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'POST':
        request.data["creator"] = request.user.id
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method in ['PUT', 'DELETE']:
        try:
            event = Event.objects.get(id=event_id)
            if event.creator != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
                
            if request.method == 'PUT':
                request.data["creator"] = request.user.id
                serializer = EventSerializer(event, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:  # DELETE
                event.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
                
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

