from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BookingRequest, AvailableDate, Service, BlockedDate, Review


class BookingRequestForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label=_("Я согласен(на) на обработку персональных данных"),
        error_messages={
            "required": _(
                "Для отправки заявки необходимо согласиться "
                "на обработку персональных данных."
            ),
        },
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = BookingRequest

        fields = [
            "name",
            "phone",
            "email",
            "messenger",
            "service",
            "preferred_date",
            "message",
            "consent",
        ]

        labels = {
            "name": _("Ваше имя"),
            "phone": _("Телефон"),
            "email": _("Email"),
            "messenger": _("Мессенджер или социальная сеть"),
            "service": _("Услуга"),
            "preferred_date": _("Желаемая дата"),
            "message": _("Сообщение"),
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": _("Ваше имя"),
                    "autocomplete": "name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": _("Телефон"),
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Email"),
                    "autocomplete": "email",
                    "inputmode": "email",
                }
            ),

            "preferred_date": forms.DateInput(
                attrs={
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),

            "messenger": forms.TextInput(
                attrs={
                    "placeholder": _(
                        "Telegram, WhatsApp или другая социальная сеть"
                    ),
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": _("Расскажите о вашей идее"),
                    "rows": 5,
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if phone and len(phone) < 7:
            raise forms.ValidationError(
                _("Введите корректный номер телефона.")
            )

        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["service"].queryset = Service.objects.filter(
            is_active=True,
        ).order_by("order", "title_ru")

        available_dates = AvailableDate.objects.filter(
            is_available=True,
            date__gte=date.today(),
        ).order_by("date")

        for field_name, field in self.fields.items():
            if field_name == "consent":
                field.widget.attrs["class"] = "form-checkbox"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get("preferred_date")

        if not preferred_date:
            return preferred_date

        if preferred_date < date.today():
            raise forms.ValidationError(
                _("Нельзя выбрать прошедшую дату.")
            )

        is_blocked = BlockedDate.objects.filter(
            date=preferred_date,
            is_active=True,
        ).exists()

        if is_blocked:
            raise forms.ValidationError(
                _("Эта дата недоступна. Выберите другую.")
            )

        return preferred_date

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        messenger = cleaned_data.get("messenger")
        preferred_date = cleaned_data.get("preferred_date")

        if not phone and not email and not messenger:
            raise forms.ValidationError(
                _(
                    "Укажите хотя бы один способ связи: "
                    "телефон, email или мессенджер."
                )
            )
        if preferred_date:
            exists = BookingRequest.objects.filter(
                preferred_date=preferred_date,
                status__in=[
                    BookingRequest.Status.NEW,
                    BookingRequest.Status.CONTACTED,
                    BookingRequest.Status.CONFIRMED,
                ],
            ).exists()

            if exists:
                self.add_error(
                    "preferred_date",
                    _("На эту дату уже есть активная заявка.")
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["service"].queryset = Service.objects.filter(
            is_active=True,
        ).order_by("order", "title_ru")

        for field_name, field in self.fields.items():
            if field_name == "consent":
                field.widget.attrs.update({
                    "class": "form-checkbox",
                })
            else:
                field.widget.attrs.update({
                    "class": "form-control",
                })

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "client_name",
            "client_photo",
            "text_ru",
        ]

        labels = {
            "client_name": _("Ваше имя"),
            "client_photo": _("Фотография"),
            "text_ru": _("Ваш отзыв"),
        }

        widgets = {
            "client_name": forms.TextInput(
                attrs={
                    "placeholder": _("Ваше имя"),
                    "autocomplete": "name",
                }
            ),

            "text_ru": forms.Textarea(
                attrs={
                    "placeholder": _(
                        "Расскажите о ваших впечатлениях от съёмки"
                    ),
                    "rows": 7,
                }
            ),
        }