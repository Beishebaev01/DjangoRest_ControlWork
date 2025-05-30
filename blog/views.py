from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, PostValidateSerializer, CommentValidateSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostListSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'id'


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body')
        is_published = serializer.validated_data.get('is_published')

        post = Post.objects.create(
            title=title,
            body=body,
            is_published=is_published,
            author=self.request.user
        )
        return Response(status=status.HTTP_201_CREATED, data=PostDetailSerializer(post).data)

class CommentAPIViewSet(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        body = serializer.validated_data.get('body')
        post_id = serializer.validated_data.get('post_id')
        is_approved = serializer.validated_data.get('is_approved', False)

        comment = Comment.objects.create(
            body=body,
            post_id=post_id,
            author=self.request.user,
            is_approved=is_approved
        )
        return Response(status=status.HTTP_201_CREATED, data=CommentSerializer(comment).data)