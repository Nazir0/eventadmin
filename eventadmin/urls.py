from django.contrib import admin
from django.urls import include, path

from django.urls import path
from events.views import user_events
from accounts.views import event_users
from accounts import views as accounts_views
from events import views as events_views
from home import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('login/', accounts_views.secret_page, name='secret_page'),  # Login page
    path('create/event/', events_views.create_event, name='create_event'),  # Create a new event
    path('home/', home_views.list_events, name='home'),  # List all events on the home page
    path('logout/', home_views.logout_view, name='logout'),  # Logout view
    path('event/<int:event_id>/', home_views.event_detail, name='event_detail'),  # Event detail page
    path('api/events/<str:username>/', user_events, name='user_events'),  # API to get events for a specific user
    path('api/events/user/<int:event_id>/', event_users, name='event_users'),  # API to get users for a specific event
    path('api-auth/', include('rest_framework.urls'))  # API authentication
]
