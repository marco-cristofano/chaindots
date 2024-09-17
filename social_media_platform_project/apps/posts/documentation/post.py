from drf_spectacular.utils import OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.posts.serializers.comment import (
    CommentCreateSerializer,
    CommentSerializer
)
from apps.posts.serializers.post import (
    PostCreateSerializer,
    PostDetailedSerializer,
    PostSerializer
)


doc_post_list = {
    'responses': {
        '200': OpenApiResponse(
            description='Operación exitosa.',
            response=PostSerializer,
            ),
    },
    'operation_id': 'Return posts order by descending created_at.',
    'description': 'Return posts ordered, paginated and filtered.',
    'parameters': [
        OpenApiParameter(
            name='page_size',
            location=OpenApiParameter.QUERY,
            description="Posts per page.",
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='page_number',
            location=OpenApiParameter.QUERY,
            description="Page number.",
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='from_date',
            location=OpenApiParameter.QUERY,
            description="Filter posts from this date.",
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='to_date',
            location=OpenApiParameter.QUERY,
            description="Filter posts to this date.",
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='author_id',
            location=OpenApiParameter.QUERY,
            description="Filter posts by author.",
            type=OpenApiTypes.INT
        )
    ]
}

doc_post_create = {
    'responses': {
        '201': OpenApiResponse(
            description='Operación exitosa.',
            response=PostSerializer,
            ),
    },
    'operation_id': 'Create a new post.',
    'description': 'Create a new post.',
    'request': PostCreateSerializer
}

doc_post_retrieve = {
    'responses': {
        '200': OpenApiResponse(
            description='Operación exitosa.',
            response=PostDetailedSerializer,
            ),
    },
    'operation_id': 'Return a detailed post.',
    'description': 'Return a detailed post including its author.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description="Id of post.",
            type=OpenApiTypes.INT
        )
    ]
}

doc_post_post_comments = {
    'methods': ('POST',),
    'responses': {
        '201': OpenApiResponse(
            description='Operación exitosa.',
            response=CommentSerializer,
            ),
    },
    'operation_id': 'Create a new comment for specific post.',
    'description': 'Create a new comment for specific post.',
    'request': CommentCreateSerializer
}

doc_post_get_comments = {
    'methods': ('GET',),
    'responses': {
        '200': OpenApiResponse(
            description='Operación exitosa.',
            response=CommentSerializer,
            ),
    },
    'operation_id': 'Return all comments for specific post.',
    'description': 'Return all comments for specific post.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description="Id of post.",
            type=OpenApiTypes.INT
        )
    ]
}
