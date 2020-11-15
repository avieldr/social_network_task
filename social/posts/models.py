from django.db import models


from django.contrib.auth import get_user_model
User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(email='sentinelemail@tradecore.com')[0]


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True)

    class Meta:
        default_related_name = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title