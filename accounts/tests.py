from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomUserModelTest(TestCase):
    """Test the custom user model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            phone_number='1234567890',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test creating a user is successful"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class TokenAuthTest(APITestCase):
    """Test token authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication_url = reverse('api_token_auth')
    
    def test_token_authentication(self):
        """Test obtaining a token with valid credentials"""
        response = self.client.post(
            self.api_authentication_url,
            {'username': 'testuser', 'password': 'testpass123'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_token_authentication_invalid_credentials(self):
        """Test token authentication with invalid credentials"""
        response = self.client.post(
            self.api_authentication_url,
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_api_requires_authentication(self):
        """Test that API endpoints require authentication"""
        # Create a URL for a protected endpoint
        url = reverse('user_events', args=['testuser'])
        
        # Try accessing without token
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Add token authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)