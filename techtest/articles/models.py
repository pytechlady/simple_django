from django.db import models
from techtest.author.models import Author


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    regions = models.ManyToManyField(
        'regions.Region', related_name='articles', blank=True
    )
    authors = models.ForeignKey(
        Author, related_name='articles', on_delete=models.SET_NULL, blank=True, null=True
    )
