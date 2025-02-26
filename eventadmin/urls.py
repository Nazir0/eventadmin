from django.contrib import admin
from django.urls import include, path

from django.urls import path
from accounts import views as accounts_views
from events import views as events_views
from home import views as home_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view

# Web URLs
web_urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('login/', accounts_views.secret_page, name='secret_page'),  # Login page
    path('create/event/', events_views.create_event, name='create_event'),  # Create a new event
    path('home/', home_views.list_events, name='home'),  # List all events on the home page
    path('logout/', home_views.logout_view, name='logout'),  # Logout view
    path('event/<int:event_id>/', home_views.event_detail, name='event_detail'),  # Event detail page
    path('event/<int:event_id>/join/', events_views.add_participant, name='add_participant'),  # Join event
]

# API URLs
api_urlpatterns = [
    path('api/users/events/<str:username>/', events_views.user_events, name='user_events'),  # API to get events for a specific user
    path('api/events/users/<int:event_id>/', accounts_views.event_users, name='event_users'),  # API to get users for a specific event
    path('api/events/', events_views.event_api, name='event_api_create'),  # API to create a new event
    path('api/events/<int:event_id>/', events_views.event_api, name='event_api_detail'),  # API to modify, display or delete an event
    path('api/events/<int:event_id>/participants/', events_views.show_participants, name='show_participants'),  # API to get participants for a specific event
    path('api/token/', obtain_auth_token, name='api_token_auth'),  # API token auth
    path('api-auth/', include('rest_framework.urls')),  # API authentication
    path('api/schema/', get_schema_view(
        title="EventAdmin API",
        description="API for event management",
        version="1.0.0"
    ), name='openapi-schema'),  # API schema
]

# Combine URL patterns
urlpatterns = web_urlpatterns + api_urlpatterns
