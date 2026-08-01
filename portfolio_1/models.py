from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import get_language
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Дата изменения",
        auto_now=True,
    )

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):

    photographer_name_ru = models.CharField(
        "Имя фотографа на русском",
        max_length=150,
    )
    photographer_name_en = models.CharField(
        "Имя фотографа на английском",
        max_length=150,
        blank=True,
    )

    short_description_ru = models.TextField(
        "Краткое описание на русском",
        blank=True,
    )
    short_description_en = models.TextField(
        "Краткое описание на английском",
        blank=True,
    )

    biography_ru = models.TextField(
        "Биография на русском",
        blank=True,
    )
    biography_en = models.TextField(
        "Биография на английском",
        blank=True,
    )

    logo = models.ImageField(
        "Логотип",
        upload_to="site/logo/",
        blank=True,
        null=True,
    )
    photographer_photo = models.ImageField(
        "Фотография фотографа",
        upload_to="site/photographer/",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        "Телефон",
        max_length=30,
        blank=True,
    )
    email = models.EmailField(
        "Email",
        blank=True,
    )
    address_ru = models.CharField(
        "Адрес на русском",
        max_length=255,
        blank=True,
    )
    address_en = models.CharField(
        "Адрес на английском",
        max_length=255,
        blank=True,
    )

    copyright_ru = models.CharField(
        "Авторское право на русском",
        max_length=255,
        blank=True,
    )
    copyright_en = models.CharField(
        "Авторское право на английском",
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    @property
    def photographer_name(self):
        if get_language() == "en" and self.photographer_name_en:
            return self.photographer_name_en

        return self.photographer_name_ru


    @property
    def short_description(self):
        if get_language() == "en" and self.short_description_en:
            return self.short_description_en

        return self.short_description_ru


    @property
    def biography(self):
        if get_language() == "en" and self.biography_en:
            return self.biography_en

        return self.biography_ru


    @property
    def address(self):
        if get_language() == "en" and self.address_en:
            return self.address_en

        return self.address_ru


    @property
    def copyright(self):
        if get_language() == "en" and self.copyright_en:
            return self.copyright_en

        return self.copyright_ru

    def __str__(self):
        return self.photographer_name_ru


class SocialLink(TimeStampedModel):
    name = models.CharField(
        "Название",
        max_length=50,
    )
    url = models.URLField(
        "Ссылка",
    )
    icon = models.CharField(
        "Название иконки",
        max_length=50,
        blank=True,
        help_text="Например: telegram, instagram, whatsapp",
    )
    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

    def __str__(self):
        return self.name


class HomeSlide(TimeStampedModel):
    """
    Слайды главной страницы.
    """

    title_ru = models.CharField(
        "Заголовок на русском",
        max_length=150,
        blank=True,
    )
    title_en = models.CharField(
        "Заголовок на английском",
        max_length=150,
        blank=True,
    )

    image_desktop = models.ImageField(
        "Изображение для компьютера",
        upload_to="slides/desktop/",
    )
    image_mobile = models.ImageField(
        "Изображение для телефона",
        upload_to="slides/mobile/",
        blank=True,
        null=True,
    )

    link = models.CharField(
        "Ссылка",
        max_length=255,
        blank=True,
        help_text="Например: /portfolio/studio/",
    )
    alt_text = models.CharField(
        "Описание изображения",
        max_length=255,
        blank=True,
    )

    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды главной страницы"

    @property
    def title(self):
        if get_language() == "en" and self.title_en:
            return self.title_en

        return self.title_ru

    def __str__(self):
        return self.title_ru or f"Слайд №{self.pk}"


class PortfolioCategory(TimeStampedModel):
    title_ru = models.CharField(
        "Название на русском",
        max_length=150,
    )
    title_en = models.CharField(
        "Название на английском",
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        "Адрес страницы",
        max_length=180,
        unique=True,
        blank=True,
    )

    description_ru = models.TextField(
        "Описание на русском",
        blank=True,
    )
    description_en = models.TextField(
        "Описание на английском",
        blank=True,
    )

    cover = models.ImageField(
        "Обложка",
        upload_to="portfolio/covers/",
    )
    cover_mobile = models.ImageField(
        "Обложка для телефона",
        upload_to="portfolio/covers/mobile/",
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )
    show_on_home = models.BooleanField(
        "Показывать на главной",
        default=True,
    )

    seo_title = models.CharField(
        "SEO-заголовок",
        max_length=255,
        blank=True,
    )
    seo_description = models.CharField(
        "SEO-описание",
        max_length=320,
        blank=True,
    )

    class Meta:
        ordering = ["order", "title_ru"]
        verbose_name = "Категория портфолио"
        verbose_name_plural = "Категории портфолио"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (
                slugify(
                    self.title_en or self.title_ru,
                    allow_unicode=True,
                )
                or uuid4().hex[:10]
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "portfolio:portfolio_detail",
            kwargs={"slug": self.slug},
        )
    
    @property
    def title(self):
        if get_language() == "en" and self.title_en:
            return self.title_en

        return self.title_ru


    @property
    def description(self):
        if get_language() == "en" and self.description_en:
            return self.description_en

        return self.description_ru

    def __str__(self):
        return self.title_ru


class Photo(TimeStampedModel):
    class Orientation(models.TextChoices):
        PORTRAIT = "portrait", "Вертикальная"
        LANDSCAPE = "landscape", "Горизонтальная"
        SQUARE = "square", "Квадратная"

    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Категория",
    )
    image = models.ImageField(
        "Фотография",
        upload_to="portfolio/photos/",
    )
    thumbnail = models.ImageField(
        "Миниатюра",
        upload_to="portfolio/thumbnails/",
        blank=True,
        null=True,
    )

    title_ru = models.CharField(
        "Название на русском",
        max_length=150,
        blank=True,
    )
    title_en = models.CharField(
        "Название на английском",
        max_length=150,
        blank=True,
    )
    alt_text = models.CharField(
        "Описание фотографии",
        max_length=255,
        blank=True,
    )

    orientation = models.CharField(
        "Ориентация",
        max_length=20,
        choices=Orientation.choices,
        default=Orientation.PORTRAIT,
    )
    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )
    is_featured = models.BooleanField(
        "Избранная фотография",
        default=False,
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    @property
    def title(self):
        if get_language() == "en" and self.title_en:
            return self.title_en

        return self.title_ru
    
    def get_absolute_url(self):
        return reverse(
            "portfolio:photo_detail",
            kwargs={
                "category_slug": self.category.slug,
                "photo_id": self.pk,
            },
        )

    def __str__(self):
        return self.title_ru or f"Фотография №{self.pk}"


class Service(TimeStampedModel):
    title_ru = models.CharField(
        "Название на русском",
        max_length=150,
    )
    title_en = models.CharField(
        "Название на английском",
        max_length=150,
        blank=True,
    )

    description_ru = models.TextField(
        "Описание на русском",
    )
    description_en = models.TextField(
        "Описание на английском",
        blank=True,
    )

    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_text_ru = models.CharField(
        "Текст цены на русском",
        max_length=100,
        blank=True,
        help_text="Например: от 5 000 сом",
    )
    price_text_en = models.CharField(
        "Текст цены на английском",
        max_length=100,
        blank=True,
    )

    duration_minutes = models.PositiveIntegerField(
        "Продолжительность в минутах",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        "Обложка",
        upload_to="services/",
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )

    class Meta:
        ordering = ["order", "title_ru"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    @property
    def title(self):
        if get_language() == "en" and self.title_en:
            return self.title_en

        return self.title_ru


    @property
    def description(self):
        if get_language() == "en" and self.description_en:
            return self.description_en

        return self.description_ru


    @property
    def price_text(self):
        if get_language() == "en" and self.price_text_en:
            return self.price_text_en

        return self.price_text_ru

    def __str__(self):
        return self.title_ru


class Review(TimeStampedModel):
    client_name = models.CharField(
        "Имя клиента",
        max_length=150,
    )
    text_ru = models.TextField(
        "Отзыв на русском",
    )
    text_en = models.TextField(
        "Отзыв на английском",
        blank=True,
    )

    client_photo = models.ImageField(
        "Фотография клиента",
        upload_to="reviews/",
        blank=True,
        null=True,
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        default=5,
    )
    is_active = models.BooleanField(
        "Опубликован",
        default=True,
    )
    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )

    rating = models.PositiveSmallIntegerField(
        "Оценка",
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    @property
    def text(self):
        if get_language() == "en" and self.text_en:
            return self.text_en

        return self.text_ru

    def __str__(self):
        return self.client_name


class FAQ(TimeStampedModel):
    question_ru = models.CharField(
        "Вопрос на русском",
        max_length=255,
    )
    question_en = models.CharField(
        "Вопрос на английском",
        max_length=255,
        blank=True,
    )
    answer_ru = models.TextField(
        "Ответ на русском",
    )
    answer_en = models.TextField(
        "Ответ на английском",
        blank=True,
    )

    order = models.PositiveIntegerField(
        "Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        "Показывать",
        default=True,
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Вопрос и ответ"
        verbose_name_plural = "Частые вопросы"
    
    @property
    def question(self):
        if get_language() == "en" and self.question_en:
            return self.question_en

        return self.question_ru


    @property
    def answer(self):
        if get_language() == "en" and self.answer_en:
            return self.answer_en

        return self.answer_ru

    def __str__(self):
        return self.question_ru


class AvailableDate(TimeStampedModel):
    date = models.DateField(
        "Дата",
        unique=True,
    )
    note_ru = models.CharField(
        "Примечание на русском",
        max_length=255,
        blank=True,
    )
    note_en = models.CharField(
        "Примечание на английском",
        max_length=255,
        blank=True,
    )
    is_available = models.BooleanField(
        "Дата свободна",
        default=True,
    )

    class Meta:
        ordering = ["date"]
        verbose_name = "Свободная дата"
        verbose_name_plural = "Свободные даты"

    @property
    def note(self):
        if get_language() == "en" and self.note_en:
            return self.note_en

        return self.note_ru
    
    @property
    def month(self):
        return self.date.strftime("%B")
    
    @property
    def day(self):
        return self.date.day
    
    @property
    def weekday(self):
        return self.date.strftime("%A")

    def __str__(self):
        return str(self.date)


class BookingRequest(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONTACTED = "contacted", "Связались"
        CONFIRMED = "confirmed", "Подтверждена"
        COMPLETED = "completed", "Завершена"
        CANCELLED = "cancelled", "Отменена"

    name = models.CharField(
        "Имя",
        max_length=150,
    )
    phone = models.CharField(
        "Телефон",
        max_length=30,
        blank=True,
    )
    email = models.EmailField(
        "Email",
        blank=True,
    )
    messenger = models.CharField(
        "Мессенджер или социальная сеть",
        max_length=150,
        blank=True,
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        related_name="booking_requests",
        verbose_name="Услуга",
        blank=True,
        null=True,
    )
    preferred_date = models.DateField(
        "Желаемая дата",
        blank=True,
        null=True,
    )
    message = models.TextField(
        "Сообщение",
        blank=True,
    )

    consent = models.BooleanField(
        "Согласие на обработку данных",
        default=False,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    admin_comment = models.TextField(
        "Комментарий администратора",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на съёмку"
        verbose_name_plural = "Заявки на съёмку"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d.%m.%Y}"