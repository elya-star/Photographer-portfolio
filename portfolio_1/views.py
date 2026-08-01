from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.db import transaction

from .forms import BookingRequestForm
from .models import (
    AvailableDate,
    FAQ,
    HomeSlide,
    Photo,
    PortfolioCategory,
    Review,
    Service,
    SiteSettings,
    SocialLink,
)


def get_common_context() -> dict:
    return {
        "site_settings": SiteSettings.objects.first(),
        "social_links": SocialLink.objects
        .filter(is_active=True)
        .order_by("order"),
    }


def home(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    context.update(
        {
            "slides": HomeSlide.objects.filter(
                is_active=True,
            ).order_by("order", "id"),

            "featured_categories": (
                PortfolioCategory.objects
                .filter(
                    is_active=True,
                    show_on_home=True,
                )
                .order_by("order", "title_ru")[:6]
            ),

            "services": (
                Service.objects
                .filter(is_active=True)
                .order_by("order", "title_ru")[:4]
            ),

            "reviews": (
                Review.objects
                .filter(is_active=True)
                .order_by("order", "-created_at")[:6]
            ),
        }
    )

    return render(
        request,
        "portfolio_1/home.html",
        context,
    )


def portfolio_list(request: HttpRequest) -> HttpResponse:
    categories = (
        PortfolioCategory.objects
        .filter(is_active=True)
        .annotate(
            photos_count=Count(
                "photos",
                filter=Q(photos__is_active=True),
            )
        )
        .order_by("order", "title_ru")
    )

    context = get_common_context()

    context["categories"] = categories

    return render(
        request,
        "portfolio_1/portfolio_list.html",
        context,
    )


def portfolio_detail(
    request: HttpRequest,
    slug: str,
) -> HttpResponse:
    category = get_object_or_404(
        PortfolioCategory,
        slug=slug,
        is_active=True,
    )

    photos = Photo.objects.filter(
        category=category,
        is_active=True,
    ).order_by("order", "id")

    orientation = request.GET.get("orientation", "")
    featured = request.GET.get("featured", "")

    allowed_orientations = {
        Photo.Orientation.PORTRAIT,
        Photo.Orientation.LANDSCAPE,
        Photo.Orientation.SQUARE,
    }

    if orientation in allowed_orientations:
        photos = photos.filter(
            orientation=orientation,
        )
    else:
        orientation = ""

    if featured == "1":
        photos = photos.filter(
            is_featured=True,
        )
    else:
        featured = ""

    paginator = Paginator(
        photos,
        12,
    )

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    other_categories = (
        PortfolioCategory.objects
        .filter(is_active=True)
        .exclude(pk=category.pk)
        .annotate(
            photos_count=Count(
                "photos",
                filter=Q(photos__is_active=True),
            )
        )
        .order_by("order", "title_ru")[:6]
    )

    context = get_common_context()

    context.update(
        {
            "category": category,
            "photos": page_obj,
            "page_obj": page_obj,
            "other_categories": other_categories,
            "selected_orientation": orientation,
            "featured_only": featured == "1",
            "orientation_choices": Photo.Orientation.choices,
        }
    )

    return render(
        request,
        "portfolio_1/portfolio_detail.html",
        context,
    )


def services(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    context["services"] = (
        Service.objects
        .filter(is_active=True)
        .order_by("order", "title_ru")
    )

    return render(
        request,
        "portfolio_1/services.html",
        context,
    )

def reviews(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    context["reviews"] = (
        Review.objects
        .filter(is_active=True)
        .order_by("order", "-created_at")
    )

    return render(
        request,
        "portfolio_1/reviews.html",
        context,
    )


def faq(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    context["faq_list"] = FAQ.objects.filter(
        is_active=True,
    )

    return render(
        request,
        "portfolio_1/faq.html",
        context,
    )

def available_dates(request: HttpRequest) -> HttpResponse:
    dates = (
        AvailableDate.objects
        .filter(
            is_available=True,
            date__gte=date.today(),
        )
        .order_by("date")
    )

    context = get_common_context()
    context["available_dates"] = dates

    return render(
        request,
        "portfolio_1/available_dates.html",
        context,
    )


def booking(request: HttpRequest) -> HttpResponse:
    selected_service = None
    selected_date = None

    service_id = request.GET.get("service")
    date_value = request.GET.get("date")

    if service_id and service_id.isdigit():
        selected_service = Service.objects.filter(
            pk=int(service_id),
            is_active=True,
        ).first()

    if date_value:
        selected_available_date = AvailableDate.objects.filter(
            date=date_value,
            is_available=True,
            date__gte=date.today(),
        ).first()

        if selected_available_date:
            selected_date = selected_available_date.date

    if request.method == "POST":
        form = BookingRequestForm(request.POST)

        if form.is_valid():
            booking_request = form.save()

            if booking_request.preferred_date:
                AvailableDate.objects.filter(
                    date=booking_request.preferred_date,
                    is_available=True,
                ).update(
                    is_available=False,
                )

            service_title = (
                str(booking_request.service)
                if booking_request.service
                else _("Не выбрана")
            )

            preferred_date = (
                booking_request.preferred_date.strftime("%d.%m.%Y")
                if booking_request.preferred_date
                else _("Не указана")
            )

            subject = _(
                "Новая заявка на фотосессию: %(name)s"
            ) % {
                "name": booking_request.name,
            }

            body = _(
                "Имя: %(name)s\n"
                "Телефон: %(phone)s\n"
                "Email: %(email)s\n"
                "Мессенджер: %(messenger)s\n"
                "Дата: %(date)s\n"
                "Услуга: %(service)s\n\n"
                "Сообщение:\n%(message)s"
            ) % {
                "name": booking_request.name,
                "phone": booking_request.phone or _("Не указан"),
                "email": booking_request.email or _("Не указан"),
                "messenger": (
                    booking_request.messenger
                    or _("Не указан")
                ),
                "date": preferred_date,
                "service": service_title,
                "message": booking_request.message or _("Не указано"),
            }

            contact_email = getattr(
                settings,
                "CONTACT_EMAIL",
                "",
            )

            if contact_email:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact_email],
                    fail_silently=True,
                )

            messages.success(
                request,
                _(
                    "Спасибо! Заявка успешно отправлена. "
                    "Фотограф свяжется с вами."
                ),
            )

            return redirect("portfolio:booking")

    else:
        initial_data = {}

        if selected_service:
            initial_data["service"] = selected_service

        if selected_date:
            initial_data["preferred_date"] = selected_date

        form = BookingRequestForm(
            initial=initial_data,
        )

    context = get_common_context()

    context.update(
        {
            "form": form,
            "selected_service": selected_service,
            "selected_date": selected_date,
            "today": date.today().isoformat(),
        }
    )

    return render(
        request,
        "portfolio_1/booking.html",
        context,
    )


def contacts(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    return render(
        request,
        "portfolio_1/contacts.html",
        context,
    )


def preparation_guide(request: HttpRequest) -> HttpResponse:
    context = get_common_context()

    return render(
        request,
        "portfolio_1/preparation_guide.html",
        context,
    )

def photo_detail(
    request: HttpRequest,
    category_slug: str,
    photo_id: int,
) -> HttpResponse:
    category = get_object_or_404(
        PortfolioCategory,
        slug=category_slug,
        is_active=True,
    )

    photo = get_object_or_404(
        Photo,
        pk=photo_id,
        category=category,
        is_active=True,
    )

    previous_photo = (
        Photo.objects
        .filter(
            category=category,
            is_active=True,
        )
        .filter(
            Q(order__lt=photo.order)
            | Q(
                order=photo.order,
                id__lt=photo.id,
            )
        )
        .order_by("-order", "-id")
        .first()
    )

    next_photo = (
        Photo.objects
        .filter(
            category=category,
            is_active=True,
        )
        .filter(
            Q(order__gt=photo.order)
            | Q(
                order=photo.order,
                id__gt=photo.id,
            )
        )
        .order_by("order", "id")
        .first()
    )

    related_photos = (
        Photo.objects
        .filter(
            category=category,
            is_active=True,
        )
        .exclude(pk=photo.pk)
        .order_by(
            "-is_featured",
            "order",
            "id",
        )[:6]
    )

    context = get_common_context()

    context.update(
        {
            "category": category,
            "photo": photo,
            "previous_photo": previous_photo,
            "next_photo": next_photo,
            "related_photos": related_photos,
        }
    )

    return render(
        request,
        "portfolio_1/photo_detail.html",
        context,
    )