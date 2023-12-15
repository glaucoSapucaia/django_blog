from django.db import models
from utils.rands import slugifyNew
from django.contrib.auth.models import User
from utils.images_size import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse

# Create your models here.
class PostAttachment(AbstractAttachment):
    class Meta:
        verbose_name = 'Anexo (codemirror)'
        verbose_name_plural = 'Anexos (codemirror)'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name
        if file_changed:
            resize_image(self.file, 900)
        
        return super_save

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

class PageManager(models.Manager):
    def isPublished(self):
        return self.filter(is_published=True).order_by('-id')

class Page(models.Model):
    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'

    my_objects = PageManager()

    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default="",
                            null=False, blank=True, max_length=255)
    is_published = models.BooleanField(default=False,
                                       help_text='Marque para tornar a página pública',)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:page', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.title)
        return super().save(*args, **kwargs)

class PostManager(models.Manager):
    def isPublished(self):
        return self.filter(is_published=True).order_by('-id')

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    my_objects = PostManager()

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
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugifyNew(self.title)
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        if cover_changed:
            resize_image(self.cover, 900)
        
        return super_save