#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps


DEFAULT_CANVAS_SIZE = 500
DEFAULT_PADDING = 10
DEFAULT_OUTPUT_SUFFIX = "_png_500"

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
}


def ask_for_source_folder() -> Path:
    while True:
        user_input = input("Enter source folder: ").strip()

        if not user_input:
            print("Please enter a folder path.")
            continue

        source_dir = Path(user_input).expanduser().resolve()

        if not source_dir.exists():
            print(f"The folder does not exist: {source_dir}")
            continue

        if not source_dir.is_dir():
            print(f"The specified path is not a folder: {source_dir}")
            continue

        return source_dir


def ask_yes_no(question: str, default: bool = False) -> bool:
    default_hint = "y/N" if not default else "Y/n"

    while True:
        answer = input(f"{question} ({default_hint}): ").strip().lower()

        if not answer:
            return default

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please answer with y or n.")


def should_skip_file(path: Path, include_mosaics: bool) -> bool:
    name = path.name.lower()

    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return True

    if not include_mosaics and "mosaic" in name:
        return True

    return False


def resize_logo_to_canvas(
    source_path: Path,
    target_path: Path,
    canvas_size: int = DEFAULT_CANVAS_SIZE,
    padding: int = DEFAULT_PADDING,
    upscale: bool = False,
) -> None:
    inner_size = canvas_size - (padding * 2)

    if inner_size <= 0:
        raise ValueError("Padding is too large for the selected canvas size.")

    with Image.open(source_path) as img:
        img = ImageOps.exif_transpose(img)

        if getattr(img, "is_animated", False):
            img.seek(0)

        img = img.convert("RGBA")

        original_width, original_height = img.size
        largest_side = max(original_width, original_height)

        if largest_side == 0:
            raise RuntimeError(f"Invalid image size: {source_path}")

        scale = inner_size / largest_side

        if not upscale:
            scale = min(scale, 1.0)

        new_width = max(1, round(original_width * scale))
        new_height = max(1, round(original_height * scale))

        resized = img.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS,
        )

        canvas = Image.new(
            "RGBA",
            (canvas_size, canvas_size),
            (0, 0, 0, 0),
        )

        x = (canvas_size - new_width) // 2
        y = (canvas_size - new_height) // 2

        canvas.alpha_composite(resized, (x, y))

        target_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(target_path, "PNG", optimize=True)

        with Image.open(target_path) as saved_img:
            if saved_img.size != (canvas_size, canvas_size):
                raise RuntimeError(
                    f"Output file has {saved_img.size[0]}x{saved_img.size[1]}px "
                    f"instead of {canvas_size}x{canvas_size}px: {target_path}"
                )


def convert_folder(
    source_dir: Path,
    output_dir: Path,
    canvas_size: int = DEFAULT_CANVAS_SIZE,
    padding: int = DEFAULT_PADDING,
    upscale: bool = False,
    include_mosaics: bool = False,
) -> None:
    processed = 0
    skipped = 0
    failed = 0

    if output_dir.exists():
        print(f"Deleting old output folder: {output_dir}")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for source_path in source_dir.rglob("*"):
        if not source_path.is_file():
            continue

        if should_skip_file(source_path, include_mosaics):
            skipped += 1
            continue

        relative_path = source_path.relative_to(source_dir)
        target_relative_path = relative_path.with_suffix(".png")
        target_path = output_dir / target_relative_path

        try:
            resize_logo_to_canvas(
                source_path=source_path,
                target_path=target_path,
                canvas_size=canvas_size,
                padding=padding,
                upscale=upscale,
            )
            processed += 1
            print(f"OK: {relative_path} -> {target_relative_path}")

        except Exception as exc:
            failed += 1
            print(f"ERROR: {relative_path}: {exc}")

    print()
    print("Done.")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Output folder: {output_dir.resolve()}")


def main() -> None:
    print("PNG converter for local image folders")
    print("All supported images will be converted to PNG and placed on a transparent 500x500px canvas.")
    print()

    source_dir = ask_for_source_folder()
    output_dir = source_dir.parent / f"{source_dir.name}{DEFAULT_OUTPUT_SUFFIX}"

    include_mosaics = ask_yes_no(
        "Should files with 'mosaic' in the name also be processed?",
        default=False,
    )

    upscale = ask_yes_no(
        "Should smaller logos be upscaled?",
        default=False,
    )

    print()
    print(f"Source folder: {source_dir}")
    print(f"Output folder: {output_dir}")
    print(f"Canvas: {DEFAULT_CANVAS_SIZE}x{DEFAULT_CANVAS_SIZE}px")
    print(f"Padding: {DEFAULT_PADDING}px")
    print()

    convert_folder(
        source_dir=source_dir,
        output_dir=output_dir,
        canvas_size=DEFAULT_CANVAS_SIZE,
        padding=DEFAULT_PADDING,
        upscale=upscale,
        include_mosaics=include_mosaics,
    )


if __name__ == "__main__":
    main()
