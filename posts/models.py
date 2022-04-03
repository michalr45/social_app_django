from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='posts',
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=350)
    slug = models.SlugField(max_length=200,
                            blank=True,
                            unique=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_liked',
                                        blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.user) + "-" + str(self.id)
            self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True,
                               db_index=True)

    class Meta:
        ordering = ['-created']
