from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

# Url routes for API
urlpatterns = [
    path('api/classes/', views.ListCourses.as_view())
]