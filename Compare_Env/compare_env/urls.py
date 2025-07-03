from django.contrib import admin
from django.urls import path
from compare_env_app.views import compare_envs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compare/', compare_envs, name='compare_envs'),
]
# This file defines the URL patterns for the Django application.
# It includes the admin interface and a custom view for comparing environments.