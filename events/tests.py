from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Event
from .serializers import EventSerializer
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class EventModelTest(TestCase):
    """Test the Event model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.event = Event.objects.create(
            name='Test Event',
            description='Test Description',
            location='Test Location',
            date=timezone.now() + timedelta(days=10),
            creator=self.user
        )
    
    def test_event_creation(self):
        """Test creating an event is successful"""
        self.assertEqual(self.event.name, 'Test Event')
        self.assertEqual(self.event.description, 'Test Description')
        self.assertEqual(self.event.location, 'Test Location')
        self.assertEqual(self.event.creator, self.user)
    
    def test_event_string_representation(self):
        """Test the string representation of event"""
        self.assertEqual(str(self.event), self.event.name)

class EventAPITest(APITestCase):
    """Test the Event API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.event_data = {
            'name': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'date': (timezone.now() + timedelta(days=10)).isoformat(),
            'creator': self.user.id
        }
        
        self.event = Event.objects.create(
            name='Existing Event',
            description='Existing Description',
            location='Existing Location',
            date=timezone.now() + timedelta(days=5),
            creator=self.user
        )
    
    def test_create_event(self):
        """Test creating a new event via API"""
        url = reverse('event_api_create')
        response = self.client.post(url, self.event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)  # Existing event + new one
        self.assertEqual(Event.objects.get(name='Test Event').creator, self.user)
    
    def test_get_event(self):
        """Test retrieving an event via API"""
        url = reverse('event_api_detail', args=[self.event.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EventSerializer(self.event)
        self.assertEqual(response.data, serializer.data)
    
    def test_update_event(self):
        """Test updating an event via API"""
        url = reverse('event_api_detail', args=[self.event.id])
        updated_data = {
            'name': 'Updated Event',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'date': (timezone.now() + timedelta(days=15)).isoformat(),
            'creator': self.user.id
        }
        
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')
        self.assertEqual(self.event.description, 'Updated Description')
    
    def test_delete_event(self):
        """Test deleting an event via API"""
        url = reverse('event_api_detail', args=[self.event.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)
    
    def test_user_events(self):
        """Test retrieving all events for a specific user"""
        url = reverse('user_events', args=[self.user.username])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = Event.objects.filter(creator=self.user)
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializer.data)