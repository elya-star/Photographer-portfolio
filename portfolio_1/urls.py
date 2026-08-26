from django.urls import path

from . import views


app_name = "portfolio"


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "portfolio/",
        views.portfolio_list,
        name="portfolio_list",
    ),
    path(
        "portfolio/<slug:category_slug>/<int:photo_id>/",
        views.photo_detail,
        name="photo_detail",
    ),
    path(
        "portfolio/<slug:slug>/",
        views.portfolio_detail,
        name="portfolio_detail",
    ),

    path("services/", views.services, name="services"),
    path("reviews/", views.reviews, name="reviews"),
    path("faq/", views.faq, name="faq"),

    path(
        "available-dates/",
        views.available_dates,
        name="available_dates",
    ),
    path(
        "booking/",
        views.booking,
        name="booking",
    ),

    path(
        "reviews/add/",
        views.add_review,
        name="add_review",
    ),

]