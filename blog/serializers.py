from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at', 'updated_at', 'is_published')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'body', 'created_at', 'updated_at', 'is_approved')


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    body = serializers.CharField(required=True, min_length=1)
    is_published = serializers.BooleanField(required=True)

    def validate(self, data):
        return data

class CommentValidateSerializer(serializers.Serializer):
    body = serializers.CharField(required=True, min_length=1, max_length=1000)
    post_id = serializers.IntegerField(required=True, min_value=1)
    is_approved = serializers.BooleanField(required=False, default=False)

    def validate_post_id(self, post_id):
        try:
            Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError('Post does not exist')
        return post_id