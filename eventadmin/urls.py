
from django.contrib import admin
from django.urls import include, path


from accounts import views as accounts_views
from events import views as events_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('secret/', accounts_views.secret_page, name='secret_page'),
    path('create/event/', events_views.create_event, name='create_event'),
]
