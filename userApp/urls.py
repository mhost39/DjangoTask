from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import routers

from . import views


router = DefaultRouter()
router.register(r'organization', views.OrganizationViewSet, basename='orgaminzation')

urlpatterns = [
    path('', include(router.urls)),
]
