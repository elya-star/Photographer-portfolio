import logging
import os

import requests


logger = logging.getLogger(__name__)


def send_telegram_booking_notification(booking_request):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not bot_token or not chat_id:
        logger.warning(
            "Telegram notification skipped: "
            "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing."
        )
        return False

    service_title = (
        str(booking_request.service)
        if booking_request.service
        else "Не выбрана"
    )

    preferred_date = (
        booking_request.preferred_date.strftime("%d.%m.%Y")
        if booking_request.preferred_date
        else "Не указана"
    )

    text = (
        "📷 Новая заявка на фотосессию\n\n"
        f"Имя: {booking_request.name}\n"
        f"Телефон: {booking_request.phone or 'Не указан'}\n"
        f"Email: {booking_request.email or 'Не указан'}\n"
        f"Мессенджер: {booking_request.messenger or 'Не указан'}\n"
        f"Услуга: {service_title}\n"
        f"Дата: {preferred_date}\n\n"
        "Сообщение:\n"
        f"{booking_request.message or 'Не указано'}\n\n"
        f"ID заявки: {booking_request.pk}"
    )

    url = (
        f"https://api.telegram.org/"
        f"bot{bot_token}/sendMessage"
    )

    try:
        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )

        response.raise_for_status()

        return True

    except requests.RequestException:
        logger.exception(
            "Failed to send Telegram booking notification."
        )
        return False