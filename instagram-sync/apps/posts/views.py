from rest_framework import generics, status
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class CustomCursorPagination(CursorPagination):
    """Кастомная пагинация для постов."""

    page_size = 10
    page_size_query_param = "page_size"
    ordering = "-timestamp"


class PostListView(generics.ListAPIView):
    """API endpoint для списка постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomCursorPagination


class CommentCreateView(APIView):
    """API endpoint для создания комментария к посту."""

    def post(self, request, pk):
        """
        Создает комментарий к посту.

        Args:
            pk: Внутренний Primary Key поста в нашей БД.
        """
        # Проверяем существование поста
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, существует ли пост в Instagram
        from apps.posts.services import get_instagram_client

        client = get_instagram_client()

        if not client.check_media_exists(post.instagram_id):
            client.close()
            return Response(
                {"error": "Post not found in Instagram"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Отправляем комментарий в Instagram API
        try:
            instagram_response = client.post_comment(
                post.instagram_id, request.data["text"]
            )
            client.close()
        except Exception as e:
            client.close()
            return Response(
                {"error": f"Instagram API error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Сохраняем комментарий в БД с instagram_comment_id из ответа API
        comment = Comment.objects.create(
            post=post,
            instagram_comment_id=instagram_response["id"],
            text=request.data["text"],
            timestamp=request.data.get("timestamp"),
            username=request.data.get("username", ""),
        )

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
