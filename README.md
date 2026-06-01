# Remote3 TV Logo Project

<img width="1774" height="887" alt="unfolded remote github 3" src="https://github.com/user-attachments/assets/17e9bcdd-710a-4e71-99f3-0a27b0e90a24" />

A curated TV channel logo repository optimized for use with **Unfolded Circle's Remote 3** and media center environments such as **Kodi**.

This repository is based on the original **tv-logo/tv-logos** project:

https://github.com/tv-logo/tv-logos

The original project provides a large collection of high-quality TV channel logos from around the world. Most of the credit, appreciation, and recognition belongs to the original creator and maintainer of that project. This repository would not exist without the extensive work already done there.

## Purpose of this repository

The goal of this repository is to provide TV channel logos in a format that works well for two practical use cases:

- Kodi media center interfaces
- Unfolded Circle Remote 3 channel icons

Many TV logos are available in different aspect ratios, sizes, and layouts. That works fine in some environments, but it can become problematic when the same files are used across different systems.

Kodi benefits from logos that are large enough to appear clean and sharp in media center views. The Unfolded Circle Remote 3 benefits from predictable, square image assets that fit well into button layouts, favorites, activities, and channel lists.

For that reason, the logos in this repository have been converted into a standardized **1:1 image format**.

## Creating your own icons

If you want to convert your own TV channel logos into the required 500 × 500 px PNG format, you can use the included Python helper script.

A step-by-step guide for non-technical users is available here:

[LOGO RESIZER GUIDE](LOGO%20RESIZER%20GUIDE.md)

## Image specifications

All logos in this repository should follow these specifications:

- **Format:** PNG
- **Canvas size:** 500 × 500 px
- **Background:** Transparent alpha channel
- **Visible logo size:** Maximum 480 × 480 px
- **Padding:** Minimum 10 px on each side
- **Aspect ratio:** Preserved
- **Distortion:** Not allowed

The actual logo is centered on a transparent 500 × 500 px canvas. The logo itself is scaled proportionally so that its largest side does not exceed 480 px. This ensures that no logo touches the outer edge of the image.

### Example

An original logo with a size of 1220 × 749 px is scaled proportionally to approximately 480 × 295 px and then centered on a transparent 500 × 500 px canvas.

The result is a square PNG file that keeps the original logo proportions intact.

## Why 500 × 500 px?

The 500 × 500 px format was chosen as a practical compromise between quality, compatibility, and usability.

It is large enough to look clean in Kodi and other media center interfaces, while also being predictable and suitable for Remote 3 usage.

The square format makes it easier to use the images in grid-based interfaces, button layouts, favorites, activities, and channel lists.

## Folder structure

The repository is organized by country or region inside the `tv-logos` folder.

### Example

```text
tv-logos/
  germany/
    ard-de.png
    zdf-de.png

  austria/
    orf-1-at.png

  united-kingdom/
    bbc-one-uk.png

misc/
```

The `misc` folder remains at the repository root for files that do not belong to a specific country or region. The folder structure is intentionally simple so users can quickly find logos by region or country.

## Source and conversion process

The source material comes from the original **tv-logo/tv-logos** repository.

The logos were downloaded, converted, and normalized using a Python script. The script processes the original country folders, keeps the folder structure intact, converts the files to PNG where required, and places each logo on a transparent 500 × 500 px canvas.

The conversion process follows this logic:

1. Download the original repository.
2. Extract the country folders.
3. Process all supported image files.
4. Convert all images to PNG.
5. Preserve transparency.
6. Scale each logo proportionally.
7. Limit the logo itself to 480 × 480 px.
8. Center the logo on a transparent 500 × 500 px canvas.
9. Save the result while keeping the original folder structure.

## Contribution guidelines

Contributions are welcome, as long as the uploaded files follow the technical requirements of this repository.

Before submitting new or updated logos, please make sure that every file meets the following rules:

1. File format must be PNG.
2. Image dimensions must be exactly 500 × 500 px.
3. The background must be transparent.
4. The visible logo must be centered.
5. The visible logo must not exceed 480 × 480 px.
6. The visible logo must keep its original aspect ratio.
7. The logo must not be stretched, squeezed, cropped, or distorted.
8. There should be at least 10 px of transparent padding around the logo.
9. The filename should be lowercase.
10. Words in filenames should be separated by hyphens.
11. The country or region should be represented by the correct folder.

Please do not upload low-resolution, blurry, badly cropped, artificially stretched, or visually distorted logos.

## Naming convention

Where possible, filenames should follow the naming convention used by the original project.

Recommended filename style:

channel-name-countrycode.png

Examples:

ard-de.png
zdf-de.png
bbc-one-uk.png
orf-1-at.png

Please use lowercase letters and hyphens instead of spaces.

## Recommended usage

These logos can be used for:

- Unfolded Circle Remote 3 channel icons
- Kodi channel logos
- IPTV channel lists
- Media center interfaces
- Home Assistant dashboards
- Custom remote control layouts
- Personal home media projects

The repository is primarily intended for personal and non-commercial use.

## License, asset rights, and trademarks

The source code, scripts, documentation, and repository structure are provided under the MIT License. This includes helper scripts such as `logo_resizer.py`.

The TV channel logos themselves are different. They may be protected by copyright, trademark, service mark, trade name, or other brand ownership rights and remain the property of their respective owners.

The logos are provided as a convenience for personal media center, IPTV, Home Assistant, Kodi, and Unfolded Circle Remote 3 usage. This repository does not claim ownership of the original channel logos, trademarks, channel names, or brand assets.

The MIT License does not grant rights to third-party logos or trademarks contained in `tv-logos/`, `misc/`, or other asset folders. For more details, see:

[ASSET_RIGHTS.md](ASSET_RIGHTS.md)

If you are a rights holder and want a logo removed, corrected, renamed, or attributed differently, please open an issue or contact the repository owner.

## Credit

Most of the original logo collection work was done by the creator and maintainer of the original **tv-logo/tv-logos** repository.

Original project:

tv-logo/tv-logos

Original repository:

https://github.com/tv-logo/tv-logos

This repository is only a reformatted and Remote 3 optimized version of that work.

All credit for the original logo collection belongs to the original project and its maintainer.
