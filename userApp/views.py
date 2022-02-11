from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
