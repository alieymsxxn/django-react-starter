from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
# from django.contrib.postgres.fields import ArrayField 

User = get_user_model()


class Note(models.Model):
    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title'], name='idx_title'),
            # models.Index(fields=['tags'], name='idx_tags'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], 
                name='unique_author_title'),
        ]
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    # tags = ArrayField(base_field=models.CharField(max_length=200, null=False, blank=False),
    #                   size=15,
    #                   default=list)
    content = models.TextField(validators=[MinLengthValidator(10)], null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        # Override later to avoid duplicates for author-title pair
        if not self.pk:
            check = Note.objects.filter(author=self.author, title=self.title).exists()
            if check:
                raise ValueError('A note with the same author and title already exists.')
        return super().save(*args, **kwargs)
