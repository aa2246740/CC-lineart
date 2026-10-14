# Track 6 Evaluation — AI-Designed Editorial Product Hero Landing Page

## 1. Why `CC-lineart` Transforms AI-Generated Hero Landing Pages

When AI coding agents are asked to design a SaaS or developer-product **Hero Landing Page**, they almost always hit the same visual ceiling:
1. **Generic SaaS Clichés**: Dark-mode purple/indigo mesh gradients, generic Tailwind cards, and stock Lucide icons that look indistinguishable from every other AI-generated landing page.
2. **Missing Centerpiece Artwork**: A great Hero section requires a **flagship visual centerpiece** on the right-hand column or below the fold. Without external image assets, AI agents either insert broken Unsplash URLs or weak CSS mockups.
3. **Disconnected Visual Language**: Even if an illustration is pasted in, the surrounding buttons, release badges, feature bento cards, and pricing callouts still use rigid `border-radius: 8px` CSS boxes that clash with the artwork.

`CC-lineart` solves all three problems in a single deterministic SVG + HTML pipeline:
- **Bespoke Flagship Hero Centerpiece (`hero-centerpiece.svg`)**: Synthesizes a 3-act narrative illustration (*Architect's Sketchbook & Fountain Pen → Autonomous Studio Cloud Workbench → Shipped Live UI Artifact Card*) over glazed `sky`, `peach`, and `clay` watercolor washes.
- **Interactive Self-Drawing & Palette Switcher**: Because every ink path carries `pathLength="1"` and semantic `data-step` ordering, the Hero page animates the drawing stroke-by-stroke on load and lets visitors switch live watercolor palettes (*Warm Clay & Sky*, *Sage Cactus & Oat*, *Botanical Fig & Heather*).
- **Unified Hand-Drawn Page Chrome**: Navigation underlines, release badges, primary/secondary CTA buttons, margin annotation arrows, 3-card Bento feature illustrations with hover watercolor parallax, and a 2-tier Editorial Pricing section with a tilted **Wax-Seal Stamp** (`RECOMMENDED`) all share the exact `#141413` charcoal ink and `#FFFEFA` paper vocabulary.

---

## 2. Deliverables & Automated Quality Gate (`scripts/lineart.py lint`)

| Deliverable | Dimensions / Format | Role | Lint Status |
| :--- | :--- | :--- | :--- |
| `generate_hero_page.py` | Python 3 generator | Deterministic builder for the 512×512 Hero SVG, PNG, and self-contained HTML landing page | N/A |
| `hero-centerpiece.svg` | `512 × 512` SVG | Flagship Hero illustration (*"The Sketchbook Cloud / Autonomous Studio"*) | **0 warnings** |
| `hero-centerpiece.png` | `512 × 512` PNG | Rasterized preview rendered on `#FAF9F5` warm cream paper | Verified |
| `hero-landing-page.html` | Self-contained HTML5 | Interactive Editorial Hero Landing Page (Navbar + Split Hero + 3-Card Bento + 2-Tier Pricing) | Verified |

### `lineart.py lint` Output (`hero-centerpiece.svg`)

```text
OK    no clip-art geometry found in the markup
OK    block visible: 47% of the wash shows (want ≥ 30%)
OK    color coverage: 19% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 64% (want ≤ 80%; the art should break out of the block)

0 warning(s).
```

---

## 3. Page Architecture & Reusable Patterns for AI Web Designers

1. **Editorial Split Hero (`1.08fr : 0.92fr`)**:
   - **Left Column**: Wobbly release pill badge (`v2.4 — Hand-Drawn UI Engine`), high-contrast editorial serif display headline (`Newsreader` / `Source Serif 4`), warm charcoal lead copy, primary & secondary hand-drawn CTA buttons, and handwritten (`Caveat`) margin annotations with curved `handify()` pointer arrows.
   - **Right Column**: Interactive studio canvas housing `hero-centerpiece.svg` with live stroke-draw replay (`Replay Ink Draw`) and instant watercolor glaze switching.
2. **Bento Feature Grid with Hover Watercolor Parallax**:
   - Each card embeds a custom 168×112 `CC-lineart` mini-illustration (*Zero-Template Vector Synthesis*, *Glazed Watercolor Layers*, *Deterministic Lint Gate*).
   - On `:hover`, CSS transitions shift and scale `.mini-wash` (`transform: translate(4px, -3px) scale(1.04)`) while lifting the `#FFFEFA` paper card, creating tactile print-like depth.
3. **Editorial Pricing with Wax-Seal Stamp**:
   - Replaces standard SaaS "Most Popular" pills with an authentic double-ring `wobbly_circle` terracotta **Wax-Seal Stamp** rotated `-8deg` at the top-right corner of the *Atelier Pro* tier.
