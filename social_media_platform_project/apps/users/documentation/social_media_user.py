from drf_spectacular.utils import OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.users.serializers.social_media_user import (
    SocialMediaUserCreateSerializer,
    SocialMediaUserDetailedSerializer,
    SocialMediaUserSerializer
)


doc_user_create = {
    'responses': {
        '201': OpenApiResponse(
            description='Operación exitosa.',
            response=SocialMediaUserSerializer,
            ),
    },
    'operation_id': 'Create a new social media user.',
    'description': 'Create a new social media user.',
    'request': SocialMediaUserCreateSerializer
}

doc_user_retrieve = {
    'responses': {
        '200': OpenApiResponse(
            description='Operación exitosa.',
            response=SocialMediaUserDetailedSerializer,
            ),
    },
    'operation_id': 'Return detailed social media user.',
    'description': 'Return detailed social media, total posts, total comment, followed and followers.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description="Id of social media user",
            type=OpenApiTypes.INT
        )
    ]
}

doc_add_follow = {
    'responses': {
        '204': OpenApiResponse(
            description='Operación exitosa.'
            ),
    },
    'operation_id': 'Add follow to social media user.',
    'description': 'Add follow to social media user.',
    'request': None,
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description="Id of social media user.",
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='user_to_follow_pk',
            location=OpenApiParameter.PATH,
            description="Id of social media user to follow.",
            type=OpenApiTypes.INT
        )
    ]
}

doc_user_list = {
    'responses': {
        '200': OpenApiResponse(
            description='Operación exitosa.',
            response=SocialMediaUserSerializer,
            ),
    },
    'operation_id': 'Return all social media users.',
    'description': 'Return all social media users ordered by email.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description="Id of social media user",
            type=OpenApiTypes.INT
        )
    ]
}
