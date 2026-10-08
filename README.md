# CC-lineart

Hand-drawn ink + watercolor SVG icons for coding agents.

Bold black line art with paper-white fills over a mottled watercolor block (clay, sky, cactus, heather, plum, mineral, peach, kraft, olive). Ship as a skill folder your agent can load, or run the Python script yourself.

![Motif gallery](docs/gallery.png)

## Unofficial

Not affiliated with or endorsed by Anthropic. The drawings are original work inspired by the illustration style on [claude.com](https://claude.com). Claude is a trademark of Anthropic.

## Install

Copy this folder into your agent's skills directory and rename it if you like:

- Claude Code: `~/.claude/skills/cc-lineart`
- Cursor / other agents: wherever that product loads skills from

Then open a terminal in the folder (or pass paths to `scripts/lineart.py`).

### Requirements

- Python 3
- `rsvg-convert` (librsvg)
- ImageMagick (`magick`)
- Pillow (only for `lint`)

```bash
# Debian/Ubuntu
sudo apt-get install librsvg2-bin imagemagick
pip install Pillow

# macOS
brew install librsvg imagemagick
pip install Pillow
```

## Quick start

```bash
python3 -I scripts/lineart.py list
python3 -I scripts/lineart.py render mac -o out/mac.svg --size lg
python3 -I scripts/lineart.py render mac -o out/mac-sm.svg --size sm
python3 -I scripts/lineart.py lint out/mac.svg
python3 -I scripts/lineart.py preview out/mac.svg out/terminal.svg -o out/sheet.png
python3 -I scripts/lineart.py add draft.json   # after you draw a new motif
```

Optional T3 Code sidebar icons (writes under `~/.t3/userdata/theme-assets/claude-watercolor/` by default; override with `CC_LINEART_T3_ASSETS`):

```bash
python3 -I scripts/lineart.py t3-icon mac --project "My App" --color sky
python3 -I scripts/lineart.py assigned
```

## Draw a new motif

Read `references/art-direction.md` and `references/drawing-guide.md` first. Motifs live in `motifs/*.json` on a 64×64 grid. Use `{PAPER}` / `{INK}` tokens, render both sizes, `lint`, `preview` next to two existing motifs, revise at least once, then `add`.

For logos and banners, study `examples/t3_logo.py` and `references/calibration/t3-logo-a-vs-b.png` for technique, not coordinates.

## License

MIT © 2026 BiggerdreamStudioDavid

---

## 中文

给编程助手用的手绘墨线 + 水彩块 SVG 图标技能包。风格参考 claude.com 插画，作品为原创，**与 Anthropic 无关，非官方**。

把本目录拷进你的 agent skills 目录（例如 Claude Code 的 `~/.claude/skills/cc-lineart`），安装 `python3`、`rsvg-convert`、ImageMagick、Pillow 后即可：

```bash
python3 -I scripts/lineart.py list
python3 -I scripts/lineart.py render mac -o out/mac.svg --size lg
python3 -I scripts/lineart.py lint out/mac.svg
python3 -I scripts/lineart.py preview out/mac.svg -o out/sheet.png
```

画新图标请先读 `references/art-direction.md` 和 `references/drawing-guide.md`。可选的 T3 Code 侧栏图标用 `t3-icon`；资源目录可用环境变量 `CC_LINEART_T3_ASSETS` 覆盖。
