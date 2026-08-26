from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.db.models import ImageField


media_root = Path(settings.MEDIA_ROOT)

uploaded = {}
uploaded_count = 0
skipped_count = 0
missing_count = 0


print("\nНачинаем перенос изображений в Cloudinary...\n")


for model in apps.get_app_config("portfolio_1").get_models():

    image_fields = [
        field
        for field in model._meta.fields
        if isinstance(field, ImageField)
    ]

    if not image_fields:
        continue

    print(f"\nМодель: {model.__name__}")

    for obj in model.objects.all():

        for field in image_fields:

            field_file = getattr(obj, field.name)

            if not field_file:
                continue

            old_name = field_file.name

            if not old_name:
                continue

            local_path = media_root / old_name

            # Если этот же файл уже переносили,
            # повторно его в Cloudinary не загружаем
            if old_name in uploaded:

                new_name = uploaded[old_name]

                if old_name != new_name:
                    setattr(obj, field.name, new_name)

                    obj.save(
                        update_fields=[field.name]
                    )

                skipped_count += 1
                continue


            # Новые файлы, уже загруженные непосредственно
            # в Cloudinary, локально существовать не будут.
            if not local_path.exists():

                print(
                    f"  [нет локально] "
                    f"{model.__name__}.{field.name}: "
                    f"{old_name}"
                )

                missing_count += 1
                continue


            try:

                storage = field.storage

                # Сохраняем непосредственно через Cloudinary storage.
                # Так upload_to не добавится второй раз.
                with local_path.open("rb") as source:

                    new_name = storage.save(
                        old_name,
                        File(source),
                    )

                uploaded[old_name] = new_name

                setattr(
                    obj,
                    field.name,
                    new_name,
                )

                obj.save(
                    update_fields=[field.name]
                )

                uploaded_count += 1

                print(
                    f"  [OK] {old_name}"
                    f" -> {new_name}"
                )

            except Exception as error:

                print(
                    f"  [ОШИБКА] "
                    f"{model.__name__}.{field.name}"
                )

                print(
                    f"           {error}"
                )


print("\n============================")
print("Перенос завершён")
print("============================")
print(f"Загружено: {uploaded_count}")
print(f"Повторных ссылок: {skipped_count}")
print(f"Не найдено локально: {missing_count}")
print("============================\n")