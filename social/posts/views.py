from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializerCreate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Post
from rest_framework.permissions import IsAuthenticated


class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializerCreate




