from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


MAX_FIELD_LENGTH = 256
STR_REPR_LENGTH = 15

User = get_user_model()


class PostsForPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'category',
            'author',
            'location'
        )

    def get_posts_queryset(self, is_today_posts=False, is_annotate=False):
        today = timezone.now()
        queryset = self.get_queryset()
        if is_today_posts:
            queryset = queryset.filter(pub_date__lte=today,
                                       is_published=True,
                                       category__is_published=True,)
        if is_annotate:
            queryset = queryset.annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        return queryset


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:STR_REPR_LENGTH]


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:STR_REPR_LENGTH]


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'))
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts_images',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    objects = models.Manager()
    for_page = PostsForPageManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title[:STR_REPR_LENGTH]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.text[:STR_REPR_LENGTH]
