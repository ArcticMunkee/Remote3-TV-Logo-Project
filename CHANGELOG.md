# Changelog

This changelog highlights user-facing changes in the Remote3 TV Logo Project.

## 2026-06-02

### Easier logo conversion

The logo resizer is now easier to use with your own image folders.

You can start it from wherever the Python file is saved and point it to any folder on your computer that contains images. The converted PNG files are placed in a new `converted_png_500` subfolder inside your selected image folder.

Basic example:

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize
```

### New DAZN custom logo set

A new `dazn-custom` logo folder was added under `misc`.

It includes DAZN channel-style icons from `dazn-1` through `dazn-60`, including alternate HD versions for many of them. These can be useful for custom channel lists, remote layouts, IPTV setups, or personal media-center shortcuts.

### Easier browsing for tools and apps

The repository now includes generated logo index files.

These files make it easier for other tools, scripts, websites, or apps to understand which logos are available and where to find them. Regular users do not need to edit these files manually, but they help keep the project easier to search and build on.

Included index files:

- `logos.json`
- `logos.csv`
- `countries.json`

### Automatic check for logo index files

GitHub now checks whether the logo index files are up to date.

If new logos are added or existing logos are renamed, the check helps catch cases where the index files were not refreshed. This keeps the repository more reliable for people who want to use the logo list in other tools.

### Clearer rights and trademark information

The project now has clearer information about logo rights, trademarks, and ownership.

The short version: the helper scripts and documentation are open source, but the TV channel logos and brand assets still belong to their respective rights holders. A dedicated `ASSET_RIGHTS.md` file explains this in more detail.

### Cleaner local project setup

Local-only Codex project instructions were removed from the public repository.

This keeps personal workspace notes out of the public project while still allowing the repository itself to stay clean and useful for everyone.
