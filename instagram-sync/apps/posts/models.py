from django.db import models


class Post(models.Model):
    """Модель поста из Instagram Graph API."""

    # Instagram API fields
    instagram_id = models.CharField(max_length=255, unique=True, db_index=True)
    media_type = models.CharField(max_length=50)  # IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url = models.URLField()
    permalink = models.URLField(blank=True, null=True)
    caption = models.TextField(blank=True, default="")
    timestamp = models.DateTimeField()
    like_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    # Local metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return f"Post {self.instagram_id} ({self.media_type})"


class Comment(models.Model):
    """Модель комментария к посту."""

    # Instagram API fields
    instagram_comment_id = models.CharField(max_length=255, unique=True, db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField()
    username = models.CharField(max_length=255, blank=True, default="")

    # Local metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        return f"Comment by {self.username} on Post {self.post.instagram_id}"  # pylint: disable=no-member
