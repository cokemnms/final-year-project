from django.db import models
from django.conf import settings
from scrapyBack.models import User  # ✅ Correct import

class ScrapPost(models.Model):
    CATEGORY_CHOICES = [
        ('Metal', 'Metal'),
        ('Wood', 'Wood'),
        ('Glass', 'Glass'),
        ('Textile', 'Textile'),
        ('Electronic', 'Electronic'),
        ('Paper', 'Paper'),
        ('Furniture', 'Furniture'),
        ('Plastic', 'Plastic'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    delivery = models.CharField(max_length=50)
    image = models.ImageField(upload_to='scrap_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    saved_by = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    through='SavedScrapPost',
    related_name='saved_scrap_posts'
)


    def __str__(self):
        return self.title


class SavedScrapPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scrap_post = models.ForeignKey(ScrapPost, on_delete=models.CASCADE, related_name='saved_scrap_posts', null=True)

    class Meta:
        unique_together = ('user', 'scrap_post')


class ScrapPostAttachment(models.Model):
    scrap_post = models.ForeignKey(ScrapPost, related_name='attachments', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scrap_images/')
    
    def get_image(self):
        return 'http://localhost:8000' + self.image.url if self.image else ''

from scrapPosts.models import ScrapPost  # adjust path if needed

class ReportedScrapPost(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scrap_post = models.ForeignKey(ScrapPost, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        post_owner = self.scrap_post.user
        return f"{self.reporter.email} reported ScrapPost {self.scrap_post.id} by {post_owner.email if post_owner else 'Unknown'}"
