# apps/posts/urls.py
from django.urls import path
from .views import PostListView, CommentCreateView

app_name = "posts"

urlpatterns = [  # ← важно: именно urlpatterns, во множественном числе!
    path("posts/", PostListView.as_view(), name="post-list"),
     path("posts/<int:pk>/comment/", CommentCreateView.as_view(), name="comment-create"),
]
