from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post, Reaction
from .permissions import IsCreatorOrReadOnly
from .serializers import PostSerializer, ReactionSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsCreatorOrReadOnly]


class ReactionListCreateView(ListCreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type']

    def get_post(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post

    def get_queryset(self):
        return Reaction.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, post_id=self.kwargs['post_id'])

class ReactionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_post(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post

    def get_queryset(self):
        return Reaction.objects.filter(post=self.get_post())
