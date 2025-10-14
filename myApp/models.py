from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Tool(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=64, default="mail")  # lucide key or icon type
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tools")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=120)
    status = models.CharField(max_length=32, default="active")  # active|paused|archived
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    KIND_CHOICES = [
        ("email", "Email"),
        ("image", "Image"),
        ("video", "Video"),
        ("code", "Code"),
        ("content", "Content"),
        ("analytics", "Analytics"),
        ("generic", "Generic"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.CharField(max_length=24, choices=KIND_CHOICES, default="generic")
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.text} ({self.kind})"
