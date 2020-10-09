from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .models import Follow, Group, Post
from .permissions import IsOwner, IsReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class BaseCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class GroupViewSet(BaseCreateListViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class FollowViewSet(BaseCreateListViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsReadOnly | (IsAuthenticated & IsOwner)]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsReadOnly | (IsAuthenticated & IsOwner)]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)
