from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema

from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from utils.exists_or_404 import exists_object_or_404

from apps.posts.documentation import post as DOC
from apps.posts.models import Post
from apps.posts.serializers.comment import (
    CommentCreatedSerializer,
    CommentCreateSerializer,
    CommentSerializer
)
from apps.posts.serializers.post import (
    PostCreateSerializer,
    PostDetailedSerializer,
    PostSerializer
)
from apps.posts.services.post import PostService


class PostsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'page_number'


class PostsFilter(filters.FilterSet):
    from_date = filters.DateFilter(
        field_name='created_at__date', lookup_expr='gte'
    )
    to_date = filters.DateFilter(
        field_name='created_at__date', lookup_expr='lte'
    )
    author_id = filters.NumberFilter(
        field_name='author_id'
    )


class PostViewset(PostsPagination, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    detailed_serializer_class = PostDetailedSerializer
    create_serializer_class = PostCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostsFilter
    http_method_names = ['get', 'post']

    @extend_schema(**DOC.doc_post_list)
    def list(self, request):
        posts = self.get_queryset().order_by('-created_at')
        posts = self.filter_queryset(posts)
        posts = self.paginate_queryset(posts, request)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    @extend_schema(**DOC.doc_post_retrieve)
    def retrieve(self, request, pk=None):
        exists_object_or_404(Post, pk)
        user = PostService.detailed(post_id=pk)
        serializer = self.detailed_serializer_class(user)
        return Response(serializer.data)

    @extend_schema(**DOC.doc_post_create)
    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        serializer_out = self.serializer_class(post)
        return Response(serializer_out.data, status=status.HTTP_201_CREATED)

    @extend_schema(**DOC.doc_post_post_comments)
    @extend_schema(**DOC.doc_post_get_comments)
    @action(detail=True, methods=['GET', 'POST'], url_path='comments')
    def comments(self, request, pk=None):
        exists_object_or_404(Post, pk)
        if request.method == 'GET':
            comments = PostService.get_all_comments(post_id=pk)
            data = CommentSerializer(comments, many=True).data
            return Response(data)
        else:
            serializer = CommentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            comment = serializer.save()
            data = CommentCreatedSerializer(comment).data
            return Response(data, status=status.HTTP_201_CREATED)
