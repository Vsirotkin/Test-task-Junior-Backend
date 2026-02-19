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

        # Сериализуем и валидируем данные
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем комментарий с привязкой к посту
            comment = serializer.save(post=post)
            return Response(
                CommentSerializer(comment).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
