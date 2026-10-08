# CC-lineart

A line-art skill for drawing icons in a hand-drawn ink + watercolor style, inspired by claude.com.

## Install

Copy this folder into your agent's skills directory (e.g. `~/.claude/skills/cc-lineart`).

```bash
# Debian/Ubuntu
sudo apt-get install librsvg2-bin imagemagick && pip install Pillow
# macOS
brew install librsvg imagemagick && pip install Pillow
```

## Commands

```bash
python3 -I scripts/lineart.py list
python3 -I scripts/lineart.py render mac -o out/mac.svg --size lg
python3 -I scripts/lineart.py lint out/mac.svg
python3 -I scripts/lineart.py preview out/mac.svg -o out/sheet.png
```

MIT
