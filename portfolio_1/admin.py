from django.contrib import admin

from .models import (
    AvailableDate,
    BookingRequest,
    BlockedDate,
    FAQ,
    HomeSlide,
    Photo,
    PortfolioCategory,
    Review,
    Service,
    ServiceImage,
    SiteSettings,
    SocialLink,
    FeatureSlide,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "photographer_name_ru",
                    "photographer_name_en",
                    "short_description_ru",
                    "short_description_en",
                    "biography_ru",
                    "biography_en",
                )
            },
        ),
        (
            "Изображения",
            {
                "fields": (
                    "logo",
                    "photographer_photo",
                    "services_background",
                    "booking_photographer_photo",
                    "reviews_background",
                    "available_dates_cta_background",
                    
                )
            },
        ),
        
        (
            "Контакты",
            {
                "fields": (
                    "phone",
                    "email",
                    "address_ru",
                    "address_en",
                )
            },
        ),
        (
            "Подвал сайта",
            {
                "fields": (
                    "copyright_ru",
                    "copyright_en",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "icon",
        "order",
        "is_active",
    )
    list_editable = (
        "order",
        "is_active",
    )
    search_fields = (
        "name",
        "url",
    )
    ordering = (
        "order",
        "name",
    )


@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = (
        "slide_name",
        "order",
        "is_active",
        "updated_at",
    )
    list_editable = (
        "order",
        "is_active",
    )
    search_fields = (
        "title_ru",
        "title_en",
        "alt_text",
    )
    ordering = (
        "order",
        "id",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Текст",
            {
                "fields": (
                    "title_ru",
                    "title_en",
                    "alt_text",
                )
            },
        ),
        (
            "Изображения",
            {
                "fields": (
                    "image_desktop",
                    "image_mobile",
                )
            },
        ),
        (
            "Настройки",
            {
                "fields": (
                    "link",
                    "order",
                    "is_active",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Слайд")
    def slide_name(self, obj):
        return obj.title_ru or f"Слайд №{obj.pk}"


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

    fields = (
        "image",
        "title_ru",
        "orientation",
        "order",
        "is_active",
        "is_featured",
    )

    ordering = (
        "order",
        "id",
    )



@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title_ru",
        "slug",
        "order",
        "show_on_home",
        "is_active",
    )
    list_editable = (
        "order",
        "show_on_home",
        "is_active",
    )
    list_filter = (
        "is_active",
        "show_on_home",
    )
    search_fields = (
        "title_ru",
        "title_en",
        "description_ru",
        "description_en",
    )
    prepopulated_fields = {
        "slug": ("title_en",),
    }
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Название",
            {
                "fields": (
                    "title_ru",
                    "title_en",
                    "slug",
                )
            },
        ),
        (
            "Описание",
            {
                "fields": (
                    "description_ru",
                    "description_en",
                )
            },
        ),
        (
            "Изображения",
            {
                "fields": (
                    "cover",
                    "cover_mobile",
                )
            },
        ),
        (
            "Отображение",
            {
                "fields": (
                    "order",
                    "is_active",
                    "show_on_home",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [
        PhotoInline,
    ]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "photo_name",
        "category",
        "orientation",
        "order",
        "is_featured",
        "is_active",
    )
    list_editable = (
        "order",
        "is_featured",
        "is_active",
    )
    list_filter = (
        "category",
        "orientation",
        "is_featured",
        "is_active",
    )
    search_fields = (
        "title_ru",
        "title_en",
        "alt_text",
        "category__title_ru",
    )
    autocomplete_fields = (
        "category",
    )
    ordering = (
        "category",
        "order",
        "id",
    )

    fieldsets = (
        (
            "Категория и изображение",
            {
                "fields": (
                    "category",
                    "image",
                    "thumbnail",
                )
            },
        ),
        (
            "Описание",
            {
                "fields": (
                    "title_ru",
                    "title_en",
                    "alt_text",
                )
            },
        ),
        (
            "Отображение",
            {
                "fields": (
                    "orientation",
                    "order",
                    "is_active",
                    "is_featured",
                )
            },
        ),
    )

    @admin.display(description="Фотография")
    def photo_name(self, obj):
        return obj.title_ru or f"Фотография №{obj.pk}"

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title_ru",
        "price_display",
        "duration_minutes",
        "order",
        "is_active",
    )
    inlines = [ServiceImageInline]
    list_editable = (
        "order",
        "is_active",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "title_ru",
        "title_en",
        "description_ru",
        "description_en",
    )
    ordering = (
        "order",
        "title_ru",
    )

    fieldsets = (
        (
            "Название",
            {
                "fields": (
                    "title_ru",
                    "title_en",
                )
            },
        ),
        (
            "Описание",
            {
                "fields": (
                    "description_ru",
                    "description_en",
                )
            },
        ),
        (
            "Цена",
            {
                "fields": (
                    "price",
                    "price_text_ru",
                    "price_text_en",
                    "duration_minutes",
                )
            },
        ),
        (
            "Акция/купон", 
            {
                "fields": (
                    "coupon_text",
                    "coupon_active",
                )
            },
        ),
        (
            "Дополнительно",
            {
                "fields": (
                    "image",
                    "order",
                    "is_active",
                )
            },
        ),
    )

    @admin.display(description="Цена")
    def price_display(self, obj):
        if obj.price_text_ru:
            return obj.price_text_ru

        if obj.price is not None:
            return f"{obj.price:,.0f}"

        return "Не указана"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "rating",
        "is_active",
        "order",
        "created_at",
    )

    list_editable = (
        "rating",
        "is_active",
        "order",
    )

    list_filter = (
        "is_active",
        "rating",
        "created_at",
    )

    search_fields = (
        "client_name",
        "text_ru",
        "text_en",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Клиент",
            {
                "fields": (
                    "client_name",
                    "client_photo",
                    "rating",
                )
            },
        ),
        (
            "Отзыв",
            {
                "fields": (
                    "text_ru",
                    "text_en",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "is_active",
                    "order",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "question_ru",
        "order",
        "is_active",
    )
    list_editable = (
        "order",
        "is_active",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "question_ru",
        "question_en",
        "answer_ru",
        "answer_en",
    )
    ordering = (
        "order",
        "id",
    )


@admin.register(AvailableDate)
class AvailableDateAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "is_available",
        "note_ru",
    )
    list_editable = (
        "is_available",
    )
    list_filter = (
        "is_available",
    )
    search_fields = (
        "note_ru",
        "note_en",
    )
    date_hierarchy = "date"
    ordering = (
        "date",
    )

@admin.register(FeatureSlide)
class FeatureSlideAdmin(admin.ModelAdmin):
    list_display = (
        "title_ru",
        "title_en",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title_ru",
        "title_en",
        "subtitle_ru",
        "subtitle_en",
        "description_ru",
        "description_en",
    )

    ordering = (
        "order",
        "id",
    )

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "image",
                    "order",
                    "is_active",
                )
            },
        ),
        (
            "Русская версия",
            {
                "fields": (
                    "subtitle_ru",
                    "title_ru",
                    "description_ru",
                    "link_text_ru",
                )
            },
        ),
        (
            "English version",
            {
                "fields": (
                    "subtitle_en",
                    "title_en",
                    "description_en",
                    "link_text_en",
                )
            },
        ),
        (
            "Ссылка",
            {
                "fields": (
                    "link_url",
                )
            },
        ),
    )

@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "reason",
        "is_active",
    )
    list_editable = (
        "is_active",
    )
    list_filter = (
        "is_active",
        "date",
    )
    search_fields = (
        "reason",
    )
    date_hierarchy = "date"
    ordering = (
        "date",
    )

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service",
        "preferred_date",
        "contact",
        "status",
        "created_at",
    )
    list_editable = (
        "status",
    )
    list_filter = (
        "status",
        "service",
        "preferred_date",
        "created_at",
    )
    search_fields = (
        "name",
        "phone",
        "email",
        "messenger",
        "message",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Клиент",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                    "messenger",
                )
            },
        ),
        (
            "Запись",
            {
                "fields": (
                    "service",
                    "preferred_date",
                    "message",
                    "consent",
                )
            },
        ),
        (
            "Обработка заявки",
            {
                "fields": (
                    "status",
                    "admin_comment",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Контакт")
    def contact(self, obj):
        return obj.phone or obj.email or obj.messenger or "Не указан"


admin.site.site_header = "Управление сайтом фотографа"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Панель управления"