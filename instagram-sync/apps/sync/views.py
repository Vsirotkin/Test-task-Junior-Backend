# apps/sync/views.py
"""Views для синхронизации с Instagram."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.posts.services import get_instagram_client
from .services import SyncService


class SyncView(APIView):
    """
    API endpoint для запуска синхронизации.

    POST /api/sync/
    """

    def post(self, request):
        """Запускает полную синхронизацию постов из Instagram."""
        try:
            client = get_instagram_client()
            sync_service = SyncService(client)
            stats = sync_service.sync_all_media()
            client.close()

            return Response(
                {"message": "Sync completed", "stats": stats}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Sync failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
