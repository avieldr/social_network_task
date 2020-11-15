from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PostReactionSerializerCreate
from .models import PostReaction
from rest_framework.permissions import IsAuthenticated


class PostsReactionsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializerCreate
