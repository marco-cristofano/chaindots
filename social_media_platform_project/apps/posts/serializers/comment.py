from rest_framework import serializers

from apps.posts.models import Comment
from apps.users.serializers.social_media_user import SocialMediaUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = SocialMediaUserSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'comment',
            'created_at'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'author',
            'post',
            'comment',
        ]


class CommentCreatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'post',
            'comment',
            'created_at'
        ]
