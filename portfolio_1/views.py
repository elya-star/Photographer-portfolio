from datetime import date
import calendar

from .telegram_notifications import (
    send_telegram_booking_notification,
)

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.db import transaction

from .forms import BookingRequestForm, ReviewForm
from .models import (
    AvailableDate,
    BlockedDate,
    BookingRequest,
    FAQ,
    HomeSlide,
    Photo,
    PortfolioCategory,
    Review,
    Service,
    SiteSettings,
    SocialLink,
    FeatureSlide,
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
                .order_by("order", "title_ru")[:3]
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
    context = get_common_context()
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

    feature_slides = (
        FeatureSlide.objects
        .filter(is_active=True)
        .order_by(
            "order",
            "id",
        )
    )

    context.update(
        {
            "categories": categories,
            "feature_slides": feature_slides,
        }
    )

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
    today = date.today()

    months_count = 3

    blocked_dates = set(
        BlockedDate.objects.filter(
            date__gte=today,
            is_active=True,
        ).values_list(
            "date",
            flat=True,
        )
    )

    booked_dates = set(
        BookingRequest.objects.filter(
            preferred_date__gte=today,
            status__in=[
                BookingRequest.Status.NEW,
                BookingRequest.Status.CONTACTED,
                BookingRequest.Status.CONFIRMED,
            ],
        ).values_list(
            "preferred_date",
            flat=True,
        )
    )

    calendar_months = []

    current_year = today.year
    current_month = today.month

    month_calendar = calendar.Calendar(
        firstweekday=0,
    )

    for month_offset in range(months_count):
        month_number = current_month + month_offset
        year = current_year

        while month_number > 12:
            month_number -= 12
            year += 1

        month_date = date(
            year,
            month_number,
            1,
        )

        weeks = []

        for week in month_calendar.monthdatescalendar(
            year,
            month_number,
        ):
            week_days = []

            for day_value in week:
                is_current_month = (
                    day_value.month == month_number
                )
                is_past = day_value < today
                is_blocked = day_value in blocked_dates
                is_booked = day_value in booked_dates

                is_available = (
                    is_current_month
                    and not is_past
                    and not is_blocked
                    and not is_booked
                )

                week_days.append(
                    {
                        "date": day_value,
                        "is_current_month": is_current_month,
                        "is_today": day_value == today,
                        "is_past": is_past,
                        "is_blocked": is_blocked,
                        "is_booked": is_booked,
                        "is_available": is_available,
                    }
                )

            weeks.append(week_days)

        calendar_months.append(
            {
                "date": month_date,
                "year": year,
                "month": month_number,
                "weeks": weeks,
            }
        )

    context = get_common_context()

    context.update(
        {
            "calendar_months": calendar_months,
            "today": today,
        }
    )

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
        try:
            parsed_date = date.fromisoformat(date_value)
        except ValueError:
            parsed_date = None

        if parsed_date and parsed_date >= date.today():
            is_blocked = BlockedDate.objects.filter(
                date=parsed_date,
                is_active=True,
            ).exists()

            if not is_blocked:
                selected_date = parsed_date

    if request.method == "POST":
        form = BookingRequestForm(request.POST)

        if form.is_valid():
            booking_request = form.save()

            send_telegram_booking_notification(
                booking_request
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
                    fail_silently=False,
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

    category_photos = list(
        Photo.objects.filter(
            category=category,
            is_active=True,
        ).order_by(
            "order",
            "id",
        )
    )

    lightbox_photos = [
        {
            "id": item.pk,
            "url": item.image.url,
            "title": item.title or category.title,
            "alt": (
                item.alt_text
                or item.title
                or category.title
            ),
            "detail_url": item.get_absolute_url(),
        }
        for item in category_photos
    ]

    current_photo_index = next(
        (
            index
            for index, item in enumerate(category_photos)
            if item.pk == photo.pk
        ),
        0,
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
            "category_photos": category_photos,
            "lightbox_photos": lightbox_photos,
            "current_photo_index": current_photo_index,
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

def add_review(request):
    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.is_active = False

            review.save()

            messages.success(
                request,
                "Спасибо! Ваш отзыв отправлен "
                "и появится после проверки."
            )

            return redirect(
                "portfolio:reviews"
            )

    else:
        form = ReviewForm()

    context = get_common_context()

    context["form"] = form

    return render(
        request,
        "portfolio_1/review_form.html",
        context,
    )