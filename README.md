# TIDAL Downloader Next Generation (tidal-dl-ng-For-DJ)

![Release](https://img.shields.io/github/v/release/Radexito/tidal-dl-ng-For-DJ)
![License](https://img.shields.io/github/license/Radexito/tidal-dl-ng-For-DJ)
![Commit activity](https://img.shields.io/github/commit-activity/m/Radexito/tidal-dl-ng-For-DJ)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)

Multithreaded, multi-chunked TIDAL downloader with a CLI and a PySide6 GUI.
This is the actively maintained continuation of `yaronzz/tidal-dl-ng`, kept
alive and extended for DJ workflow integration (see [History and credits](#history-and-credits)).

**A paid TIDAL plan is required.** Audio quality varies up to HiRes Lossless /
TIDAL MAX 24-bit 192 kHz depending on the track. Dolby Atmos is supported.

> ⚠️ Windows Defender / antivirus may flag the packaged GUI binary. This is a
> known false positive caused by PyInstaller; see the
> [official PyInstaller statement](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md).
> Installing from source (below) avoids prebuilt binaries entirely.

![App](assets/app.png)

## What it can do

- Download tracks, videos, albums, playlists, artist discographies and mixes
- Download **your account collections** (GUI): all playlists, Favorites
  (tracks, albums, artists, videos) and Mixes & Radio, including My Mix,
  My Video Mix and My Daily Discovery
- Download your favorites from the CLI: `tdn dl_fav tracks|albums|artists|videos`
- Multithreaded and multi-chunked downloads
- Rich metadata tagging (genres, producers, composers, label, BPM where the
  TIDAL API provides them; see [docs/missing_metadata.md](docs/missing_metadata.md))
- FLAC extraction from MP4 containers (`extract_flac`)
- Lyrics, album art and cover download
- Playlist file creation, symlink mode for multi-playlist libraries
- Adjustable audio and video quality, Dolby Atmos opt-in

## Install

Not on PyPI (yet). Install directly from this repository with uv:

```bash
# CLI only (provides: tidal-dl-ng, tdn)
uv tool install git+https://github.com/Radexito/tidal-dl-ng-For-DJ

# CLI + GUI (additionally provides: tidal-dl-ng-gui, tdng)
uv tool install "tidal-dl-ng-for-dj[gui] @ git+https://github.com/Radexito/tidal-dl-ng-For-DJ"
```

`pipx` works the same way (`pipx install "tidal-dl-ng-for-dj[gui] @ git+https://github.com/Radexito/tidal-dl-ng-For-DJ"`).
For development, clone the repo and use the project's uv/poetry setup
(`make install` / `poetry install --all-extras`).

## Quick start

```bash
$ tidal-dl-ng --help

 Usage: tidal-dl-ng [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────╮
│ --version  -v                                                    │
│ --help     -h        Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────╮
│ cfg       Print or set an option. If no arguments are given,     │
│           all options are listed. To set one, pass value as the  │
│           second argument.                                       │
│ dl                                                               │
│ dl_fav    Download from a favorites collection.                  │
│ gui                                                              │
│ login                                                            │
│ logout                                                           │
╰──────────────────────────────────────────────────────────────────╯
```

First log in (opens the TIDAL OAuth device flow):

```bash
tidal-dl-ng login
```

Download by URL:

```bash
tidal-dl-ng dl https://tidal.com/browse/track/46755209
tidal-dl-ng dl https://tidal.com/browse/album/123456789
tidal-dl-ng dl https://tidal.com/browse/playlist/6f08c4a7-...
```

Download favorites collections:

```bash
tidal-dl-ng dl_fav tracks
tidal-dl-ng dl_fav albums
```

Configuration lives in the CLI (`tidal-dl-ng cfg`), e.g. quality,
`path_binary_ffmpeg`, `extract_flac`, `download_dolby_atmos`.

### GUI

```bash
tdng
```

The GUI browses your account: **Playlists**, **Favorites** (tracks, albums,
artists, videos) and **Mixes & Radio** (My Mix, My Video Mix, My Daily
Discovery). Double-click a collection to download it. Hovering a track shows
a rich metadata preview.

## Development

- `tidal_dl_ng/cli.py` and `tidal_dl_ng/gui.py` are the entry points
  (`tidal-dl-ng` / `tdn` for CLI, `tidal-dl-ng-gui` / `tdng` for GUI).
- GUI is PySide6, built with Qt Designer (`pyside6-uic` the `*.ui` files in
  `tidal_dl_ng/gui/`).
- Build targets live in the `Makefile` (`make gui-linux|gui-windows|gui-macos-dmg`).
- Feature documentation: `docs/` (metadata, hover info, playlist API, ...).

## FAQ

**macOS: "app is damaged and cannot be opened"** - unsigned app quarantine:

```bash
sudo xattr -dr com.apple.quarantine /Applications/TIDAL-Downloader-NG.app/
```

**Windows antivirus flags the GUI** - false positive from PyInstaller, see the
statement linked at the top.

**`extract_flac` fails** - your `path_binary_ffmpeg` setting is wrong; point it
at a real ffmpeg binary.

**Linux: `libxcb-cursor0` missing** - install it (Ubuntu/Debian:
`sudo apt install libxcb-cursor0`).

**Dolby Atmos** - enable `download_dolby_atmos`; Atmos items download as
Atmos files at fixed 320 kbps (quality is not adjustable for Atmos).

**Metadata shows "N/A" or "-"** - the TIDAL API does not expose that field for
the item (genres, producers, BPM, ...); not a bug. Details in
[docs/missing_metadata.md](docs/missing_metadata.md).

## History and credits

This project continues `yaronzz/tidal-dl-ng`, which was **deleted from GitHub
by its author** together with `tidal-dl` and the fork ecosystem that had grown
around it (exislow, FunWarry, jotalevi and others are gone as well). The full
history and the last surviving community contributions were preserved by
importing the most complete remaining archive, and further upstream merges
(FunWarry/Warry fixes, community PRs) were folded back in.

Big thanks to everyone who built and maintained this over the years:

- **yaronzz (Robert Honz)** - author of TIDAL Media Downloader and
  tidal-dl-ng, the original project this is based on
- **exislow** - favorites and GUI work in the earlier upstream lines
- **FunWarry / Warry** - mpegdash patch and refactors
- **jotalevi, musicalmusicalmusical, Rikrdoga, Winman486, Joshua Cantara**
  and every other contributor whose commits are part of this history

The DJ-oriented changes (integration with the DjManager desktop app, naming,
packaging under this repository) are maintained by **Radexito**.

## Disclaimer

- For educational purposes only. The author is not liable for any damage.
- Do not use this to distribute or pirate music.
- Downloading from TIDAL may be illegal in your country; check local law.
