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

@login_required
def add_participant(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Participation.objects.filter(event=event)
    
    if request.method == 'POST':
        from participation.models import Participation
        # Create participation
        Participation.objects.create(
            event=event,
            participant=request.user
        )
        return redirect('event_detail', event_id=event_id)
    
    return render(request, 'events/event_detail.html', {
        'event': event, 
        'participants': participants
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_participants(request, event_id):
    """
    Retrieve all participants for a specific event.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        participants = Participation.objects.filter(event=event)
        data = [{
            'id': p.participant.id,
            'username': p.participant.username,
            'email': p.participant.email
        } for p in participants]
        return Response(data, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response(
            {"error": "Event not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events(request, username):
    """
    Retrieve all events for a specific user.
    """
    try:
        user = CustomUser.objects.get(username=username)
        events = Event.objects.filter(creator=user).order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )


    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_api(request, event_id=None):
    """
    API endpoint for managing events:
    - GET by ID: Retrieve event details
    - POST: Create a new event
    - PUT: Update an existing event (creator only)
    - DELETE: Delete an event (creator only)
    """
    # GET single event
    if request.method == 'GET' and event_id:
        try:
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    # POST - create new event
    elif request.method == 'POST':
        data = request.data.copy()
        data["creator"] = request.user.id
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # PUT or DELETE - update or delete event
    elif request.method in ['PUT', 'DELETE'] and event_id:
        try:
            event = Event.objects.get(id=event_id)
            # Check permissions - only creator can modify or delete
            if event.creator != request.user:
                return Response(
                    {"error": "You don't have permission to modify this event"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # PUT - update event
            if request.method == 'PUT':
                data = request.data.copy()
                data["creator"] = request.user.id
                serializer = EventSerializer(event, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # DELETE - remove event
            else:
                event.delete()
                return Response(
                    {"message": "Event deleted successfully"}, 
                    status=status.HTTP_204_NO_CONTENT
                )
                
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Invalid request
    else:
        return Response(
            {"error": "Invalid request"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

