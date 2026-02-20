# apps/posts/tests/test_comments.py
"""Интеграционные тесты для эндпоинта создания комментария."""

import pytest
import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.posts.models import Post, Comment


class TestCommentCreateView(APITestCase):
    """Тесты для POST /api/posts/{id}/comment/"""

    BASE_URL = "https://graph.instagram.com"

    def setUp(self):
        """Создаёт тестовый пост для использования в тестах."""
        self.post = Post.objects.create(
            instagram_id="17841405823_test",
            media_type="IMAGE",
            media_url="https://example.com/image.jpg",
            caption="Test post",
            timestamp="2026-02-19T12:00:00Z",
        )
        self.comment_url = reverse("posts:comment-create", kwargs={"pk": self.post.pk})

    def test_create_comment_success(self):
        """Тест успешного создания комментария."""
        instagram_comment_id = "17851234567890"

        with requests_mock.Mocker() as m:
            # Мок проверки существования поста
            m.get(
                f"{self.BASE_URL}/{self.post.instagram_id}",
                json={"id": self.post.instagram_id},
                status_code=200,
            )
            # Мок создания комментария
            m.post(
                f"{self.BASE_URL}/me/comments",
                json={"id": instagram_comment_id},
                status_code=200,
            )

            data = {
                "text": "Great post!",
                "timestamp": "2026-02-19T13:00:00Z",
                "username": "testuser",
            }
            response = self.client.post(self.comment_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "Great post!"

        comment = Comment.objects.get(instagram_comment_id=instagram_comment_id)
        assert comment.post == self.post

    def test_create_comment_post_not_found(self):
        """Тест обработки ошибки, если пост не найден в БД."""
        url = reverse("posts:comment-create", kwargs={"pk": 99999})

        data = {"text": "Test", "timestamp": "2026-02-19T12:00:00Z", "username": "user"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Post not found"

    def test_create_comment_post_deleted_from_instagram(self):
        """Тест обработки ошибки, если пост удалён из Instagram."""
        with requests_mock.Mocker() as m:
            # Мок: пост не найден в Instagram
            m.get(
                f"{self.BASE_URL}/{self.post.instagram_id}",
                json={"error": {"message": "Media not found"}},
                status_code=400,
            )

            data = {
                "text": "Test",
                "timestamp": "2026-02-19T12:00:00Z",
                "username": "user",
            }
            response = self.client.post(self.comment_url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Comment.objects.count() == 0  # ← ИСПРАВЛЕНО: комментарий НЕ создан
