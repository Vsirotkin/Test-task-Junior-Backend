# apps/posts/services.py
"""Сервисный слой для работы с Instagram Graph API."""

import requests
from typing import Optional, List, Dict, Any
from django.conf import settings


class InstagramAPIClient:
    """Клиент для взаимодействия с Instagram Graph API."""

    BASE_URL = "https://graph.instagram.com"

    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id
        self.session = requests.Session()

    def _get_common_params(self) -> Dict[str, str]:
        """Возвращает общие параметры для всех запросов."""
        return {
            "access_token": self.access_token,
        }

    def fetch_media_fields(self) -> str:
        """Возвращает строку полей для запроса медиа-объектов."""
        return "id,media_type,media_url,permalink,caption,timestamp,like_count,comments_count"

    def get_user_media(self, limit: int = 25) -> Dict[str, Any]:
        """
        Получает список медиа-объектов пользователя.

        Returns:
            Dict с данными API (включая пагинацию).
        """
        url = f"{self.BASE_URL}/me/media"
        params = {
            **self._get_common_params(),
            "fields": self.fetch_media_fields(),
            "limit": limit,
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_next_page(self, next_url: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Получает следующую страницу пагинации.

        Args:
            next_url: URL из поля 'paging.next' предыдущего ответа.

        Returns:
            Dict с данными следующей страницы или None.
        """
        if not next_url:
            return None
        # next_url уже содержит access_token, добавляем только fields
        response = self.session.get(
            next_url, params={"fields": self.fetch_media_fields()}
        )
        response.raise_for_status()
        return response.json()

    def post_comment(self, media_id: str, text: str) -> Dict[str, Any]:
        """
        Публикует комментарий к медиа-объекту.

        Args:
            media_id: Instagram ID поста.
            text: Текст комментария.

        Returns:
            Dict с ответом API (содержит 'id' созданного комментария).
        """
        url = f"{self.BASE_URL}/me/comments"
        params = {
            **self._get_common_params(),
            "media_id": media_id,
            "text": text,
        }
        response = self.session.post(url, data=params)
        response.raise_for_status()
        return response.json()

    def check_media_exists(self, instagram_id: str) -> bool:
        """
        Проверяет, существует ли медиа-объект в Instagram.

        Args:
            instagram_id: Instagram ID поста.

        Returns:
            True если пост существует, False иначе.
        """
        url = f"{self.BASE_URL}/{instagram_id}"
        params = {
            **self._get_common_params(),
            "fields": "id",
        }
        try:
            response = self.session.get(url, params=params)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def close(self):
        """Закрывает сессию (для очистки ресурсов)."""
        self.session.close()


# client factory
def get_instagram_client() -> InstagramAPIClient:
    """
    Factory function для создания клиента Instagram API.

    Берёт токены из настроек Django (через .env).
    """
    return InstagramAPIClient(
        access_token=settings.INSTAGRAM_ACCESS_TOKEN,
        user_id=settings.INSTAGRAM_USER_ID,
    )
