from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from events.models import Event
from django.contrib.auth import logout


@login_required
def list_events(request):
    events = Event.objects.filter(creator=request.user).order_by('date')
    return render(request, 'home/list_events.html', {'events': events, 'username': request.user.username})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
