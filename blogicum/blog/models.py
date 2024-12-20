from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
        help_text="Дата и время добавления."
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        "Заголовок", max_length=256, help_text="Введите заголовок категории."
    )
    description = models.TextField(
        "Описание", blank=True, help_text="Добавьте описание категории (необязательно)."
    )
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name="Название места",
        help_text="Введите название местоположения."
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name="Заголовок",
        help_text="Введите заголовок публикации.",
    )
    text = models.TextField(verbose_name="Текст",
                            help_text="Введите текст публикации.")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
                  "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        help_text="Выберите автора публикации.",
        related_name="posts"
    )
    location = models.ForeignKey(
        "Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
        help_text="Выберите местоположение для публикации (необязательно).",
        related_name="posts"
    )
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию для публикации.",
        related_name="posts"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,  # Сделать поле nullable
        verbose_name="Обновлено",
        help_text="Дата и время последнего изменения публикации.",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Счётчик просмотров публикации.",
    )

    @classmethod
    def get_published_posts(cls):
        return cls.objects.filter(
            is_published=True,
            pub_date__lte=now()
        )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title
