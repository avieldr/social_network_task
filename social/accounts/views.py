from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializerCreate


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('email')
    serializer_class = UserSerializerCreate
