# apps/sync/services.py
"""Сервисный слой для синхронизации данных из Instagram."""

from typing import List, Optional
from django.db import transaction
from apps.posts.models import Post
from apps.posts.services import InstagramAPIClient


class SyncService:
    """Сервис для синхронизации постов из Instagram в локальную БД."""

    def __init__(self, client: InstagramAPIClient):
        self.client = client

    def _parse_media_item(self, item: dict) -> dict:
        """Преобразует данные из API в формат для модели Post."""
        return {
            "instagram_id": item["id"],
            "media_type": item.get("media_type", ""),
            "media_url": item.get("media_url", ""),
            "permalink": item.get("permalink", ""),
            "caption": item.get("caption", ""),
            "timestamp": item.get("timestamp"),
            "like_count": item.get("like_count", 0),
            "comments_count": item.get("comments_count", 0),
        }

    @transaction.atomic
    def sync_all_media(self) -> dict:
        """
        Синхронизирует все медиа-объекты пользователя.

        Returns:
            Dict со статистикой: {created: int, updated: int, total: int}
        """
        stats = {"created": 0, "updated": 0, "total": 0}
        next_url = None

        while True:
            # Получаем страницу данных
            if next_url:
                data = self.client.get_next_page(next_url)
            else:
                data = self.client.get_user_media()

            if not data or "data" not in data:
                break

            # Обрабатываем каждый пост
            for item in data["data"]:
                parsed = self._parse_media_item(item)

                # Upsert: update_or_create по уникальному instagram_id
                obj, created = Post.objects.update_or_create(
                    instagram_id=parsed["instagram_id"], defaults=parsed
                )

                if created:
                    stats["created"] += 1
                else:
                    stats["updated"] += 1
                stats["total"] += 1

            # Проверяем, есть ли следующая страница
            paging = data.get("paging", {})
            next_url = paging.get("next")
            if not next_url:
                break

        return stats
