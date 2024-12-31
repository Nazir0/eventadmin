from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from participation.models import Participation
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from events.models import Event

def secret_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


@api_view(['GET'])
def event_users(request, event_id):
    """
    Retrieve all users for a specific event.
    """
    event = get_object_or_404(Event, id = event_id)
    participations = Participation.objects.filter(event=event)
    users = [participation.participant for participation in participations]
    serializer = UserSerializer(users, many= True)
    return Response(serializer.data)