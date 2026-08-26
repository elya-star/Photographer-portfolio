from pathlib import Path
from PIL import Image, ImageOps

MEDIA_DIR = Path("media")

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_DIMENSION = 3200

JPEG_QUALITY = 88


for path in MEDIA_DIR.rglob("*"):

    if not path.is_file():
        continue

    if path.stat().st_size <= MAX_FILE_SIZE:
        continue

    if path.suffix.lower() not in {
        ".jpg",
        ".jpeg",
    }:
        print(
            f"[ПРОПУСК] {path} "
            f"({path.stat().st_size / 1024 / 1024:.1f} MB)"
        )
        continue

    original_size = (
        path.stat().st_size / 1024 / 1024
    )

    try:
        with Image.open(path) as image:

            image = ImageOps.exif_transpose(image)

            if image.mode != "RGB":
                image = image.convert("RGB")

            width, height = image.size

            if max(width, height) > MAX_DIMENSION:

                scale = (
                    MAX_DIMENSION /
                    max(width, height)
                )

                new_size = (
                    round(width * scale),
                    round(height * scale),
                )

                image = image.resize(
                    new_size,
                    Image.Resampling.LANCZOS,
                )

            image.save(
                path,
                "JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True,
            )

        new_size = (
            path.stat().st_size / 1024 / 1024
        )

        print(
            f"[OK] {path}: "
            f"{original_size:.1f} MB"
            f" -> {new_size:.1f} MB"
        )

    except Exception as error:

        print(
            f"[ОШИБКА] {path}: {error}"
        )