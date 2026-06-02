#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shlex
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps


DEFAULT_CANVAS_SIZE = 500
DEFAULT_PADDING = 10
DEFAULT_OUTPUT_DIR_NAME = "converted_png_500"

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


def normalize_folder(path: Path) -> Path:
    folder = path.expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError(f"The folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"The specified path is not a folder: {folder}")

    return folder


def path_from_user_input(user_input: str) -> Path:
    raw_path = Path(user_input.strip().strip("\"'")).expanduser()

    if raw_path.exists():
        return raw_path

    try:
        parts = shlex.split(user_input)
    except ValueError:
        return raw_path

    if len(parts) == 1:
        return Path(parts[0]).expanduser()

    return raw_path


def path_is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def ask_for_source_folder() -> Path:
    while True:
        user_input = input("Enter source folder: ").strip()

        if not user_input:
            print("Please enter a folder path.")
            continue

        try:
            return normalize_folder(path_from_user_input(user_input))
        except (FileNotFoundError, NotADirectoryError) as exc:
            print(exc)
            continue


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


def collect_source_files(
    source_dir: Path,
    output_dir: Path,
    include_mosaics: bool,
) -> tuple[list[Path], int, int]:
    source_files: list[Path] = []
    skipped = 0
    ignored_output_files = 0
    excluded_dirs = {
        output_dir,
        (source_dir / DEFAULT_OUTPUT_DIR_NAME).resolve(),
    }

    for source_path in source_dir.rglob("*"):
        if not source_path.is_file():
            continue

        resolved_source_path = source_path.resolve()

        if any(path_is_inside(resolved_source_path, excluded_dir) for excluded_dir in excluded_dirs):
            ignored_output_files += 1
            continue

        if should_skip_file(source_path, include_mosaics):
            skipped += 1
            continue

        source_files.append(source_path)

    return source_files, skipped, ignored_output_files


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
    clean_output: bool = True,
) -> None:
    source_dir = normalize_folder(source_dir)
    output_dir = output_dir.expanduser().resolve()

    if output_dir == source_dir:
        raise ValueError("Output folder must be different from the source folder.")

    processed = 0
    failed = 0

    if clean_output and output_dir.exists():
        print(f"Deleting old output folder: {output_dir}")
        shutil.rmtree(output_dir)

    source_files, skipped, ignored_output_files = collect_source_files(
        source_dir=source_dir,
        output_dir=output_dir,
        include_mosaics=include_mosaics,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    for source_path in source_files:
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
    print(f"Ignored existing output files: {ignored_output_files}")
    print(f"Failed: {failed}")
    print(f"Output folder: {output_dir.resolve()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert local image folders to PNG files on a transparent "
            "500x500px canvas."
        )
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        help="Folder containing the images to convert. If omitted, the script asks interactively.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help=(
            "Folder for converted images. Defaults to a "
            f"'{DEFAULT_OUTPUT_DIR_NAME}' subfolder inside the source folder."
        ),
    )
    parser.add_argument(
        "--canvas-size",
        type=int,
        default=DEFAULT_CANVAS_SIZE,
        help=f"Output canvas size in pixels. Defaults to {DEFAULT_CANVAS_SIZE}.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=DEFAULT_PADDING,
        help=f"Transparent padding in pixels. Defaults to {DEFAULT_PADDING}.",
    )
    parser.add_argument(
        "--upscale",
        action="store_true",
        help="Upscale smaller logos so they use more of the canvas.",
    )
    parser.add_argument(
        "--include-mosaics",
        action="store_true",
        help="Also process files with 'mosaic' in the filename.",
    )
    parser.add_argument(
        "--clean-output",
        action="store_true",
        help=(
            "Delete an existing custom output folder before writing. "
            "The default source subfolder is cleaned automatically."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("PNG converter for local image folders")
    print("All supported images will be converted to PNG and placed on a transparent 500x500px canvas.")
    print()

    if args.source_dir:
        source_dir = normalize_folder(args.source_dir)
        include_mosaics = args.include_mosaics
        upscale = args.upscale
    else:
        source_dir = ask_for_source_folder()

        include_mosaics = ask_yes_no(
            "Should files with 'mosaic' in the name also be processed?",
            default=False,
        )

        upscale = ask_yes_no(
            "Should smaller logos be upscaled?",
            default=False,
        )

    output_dir = args.output_dir.expanduser().resolve() if args.output_dir else source_dir / DEFAULT_OUTPUT_DIR_NAME
    clean_output = args.clean_output or args.output_dir is None

    print()
    print(f"Source folder: {source_dir}")
    print(f"Output folder: {output_dir}")
    print(f"Canvas: {args.canvas_size}x{args.canvas_size}px")
    print(f"Padding: {args.padding}px")
    print(f"Clean output folder: {'yes' if clean_output else 'no'}")
    print()

    try:
        convert_folder(
            source_dir=source_dir,
            output_dir=output_dir,
            canvas_size=args.canvas_size,
            padding=args.padding,
            upscale=upscale,
            include_mosaics=include_mosaics,
            clean_output=clean_output,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
