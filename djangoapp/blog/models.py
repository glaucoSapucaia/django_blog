from django.db import models
from utils.rands import slugifyNew

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.name)
        return super().save(*args, **kwargs)
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.name)
        return super().save(*args, **kwargs)
    
class Page(models.Model):
    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'

    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default="",
                            null=False, blank=True, max_length=255)
    is_published = models.BooleanField(default=False,
                                       help_text='Marque para tornar a página pública',)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.title)
        return super().save(*args, **kwargs)