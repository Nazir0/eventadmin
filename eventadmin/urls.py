
from django.contrib import admin
from django.urls import include, path


from accounts import views as accounts_views
from events import views as events_views
from home import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', accounts_views.secret_page, name='secret_page'),
    path('create/event/', events_views.create_event, name='create_event'),
    path('home/', home_views.list_events, name='home'),
    path('logout/', home_views.logout_view, name='logout'),
    path('event/<int:event_id>/', home_views.event_detail, name='event_detail')
]
