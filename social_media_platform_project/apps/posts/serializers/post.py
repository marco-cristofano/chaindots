from rest_framework import serializers
from apps.posts.models import Post
from apps.posts.serializers.comment import CommentSerializer


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'author',
            'content'
        ]


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'created_at'
        ]


class PostDetailedSerializer(serializers.ModelSerializer):
    last_comments = serializers.SerializerMethodField()

    def get_last_comments(self, post):
        comments = post.comments.select_related(
            'author'
        ).order_by('-created_at')[:3]  # TODO: llevar a la query
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'created_at',
            'last_comments'
        ]
