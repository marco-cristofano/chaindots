from rest_framework import serializers
from apps.users.serializers.social_media_user import SocialMediaUserSerializer
from apps.posts.models import Comment


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
