# apps/posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    class Meta:
        model = Comment
        fields = [
            "id",
            "instagram_comment_id",
            "post",
            "text",
            "timestamp",
            "username",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "instagram_comment_id",
            "post",
            "created_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "instagram_id",
            "media_type",
            "media_url",
            "permalink",
            "caption",
            "timestamp",
            "like_count",
            "comments_count",
            "comments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
