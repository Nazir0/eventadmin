# eventadmin/urls.py
from django.contrib import admin
from django.urls import include, path

from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth urls
    path('secret/', views.secret_page, name='secret_page'),
    # Include other apps' urls here
]