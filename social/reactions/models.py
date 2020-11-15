from django.db import models
from posts.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

LIKE = 1
ANGRY = 2
HAPPY = 3
LOVE = 4
REACTION_TYPES = (
    (LIKE, 'Like'),
    (ANGRY, 'Angry'),
    (HAPPY, 'Happy'),
    (LOVE, 'Love'),
)

class PostReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField(choices=REACTION_TYPES)

    class Meta:
        default_related_name = 'post_reactions'
        unique_together = ('post', 'user')

    def __str__(self):
        return f'post: {self.post.id} - value: {self.value}'