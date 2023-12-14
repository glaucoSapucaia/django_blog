from django.db import models
from utils.rands import slugifyNew
from django.contrib.auth.models import User

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
    
class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(unique=True, default="",
                            null=False, blank=True, max_length=255,)
    excerpt = models.CharField(max_length=255,)
    is_published = models.BooleanField(default=False,
                                       help_text='Marque para tornar o post público',)
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m', blank=True, default="",)
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Marque para exibir a capa na página do post',
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by',
    )
    updated_at = models.DateTimeField(auto_now=True,)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='',)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.title)
        return super().save(*args, **kwargs)