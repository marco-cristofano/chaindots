from rest_framework import serializers

from apps.users.models import SocialMediaUser


class SocialMediaUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = SocialMediaUser
        fields = [
            'id',
            'email',
            'username'
        ]


class SocialMediaUserDetailedSerializer(SocialMediaUserSerializer):
    total_posts = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    followed = SocialMediaUserSerializer(many=True)
    followers = SocialMediaUserSerializer(many=True)

    class Meta:
        model = SocialMediaUser
        fields = [
            'id',
            'email',
            'username',
            'total_posts',
            'total_comments',
            'followed',
            'followers'
        ]
