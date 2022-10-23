from django.db import models
from imagekit.processors import Thumbnail
from imagekit.models import ProcessedImageField

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = ProcessedImageField(
        blank=True,
        upload_to='photos/',
        processors=[Thumbnail(300, 300)],
        format='JPEG',
        options={'quality': 80},
    )

    def __str__(self):
        return self.content
