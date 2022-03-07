from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.functional import cached_property


User = get_user_model()

class AbstractTimeStampMoodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(AbstractTimeStampMoodel):
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.short_description} by {self.created_by}'

    @property
    def short_description(self):
        return truncatechars(self.text, 20)

    @cached_property
    def get_reaction_count(self):
        return Reaction.objects.filter(post=self).values_list('type').annotate(total=models.Count('post'))

class Reaction(AbstractTimeStampMoodel):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    REACT_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=7,
        choices=REACT_CHOICES,
        default=LIKE,
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('post', 'created_by',)

    def __str__(self):
        return f'{self.type} by {self.created_by} on {self.post}'
