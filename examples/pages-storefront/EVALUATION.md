# Track 7 Evaluation — AI-Designed Boutique E-Commerce & Marketplace Storefront

## 1. Why `CC-lineart` Solves AI E-Commerce & Storefront Design's Biggest Weakness

When an AI agent builds an **E-Commerce Storefront, Creator Shop, or Digital Marketplace**, the hardest problem is **product imagery**:
1. **No Real Product Photos**: AI coding agents cannot photograph physical goods, and external placeholder URLs (`unsplash.com`, `picsum.photos`, or `placehold.co`) either break, mismatch the brand palette, or make the shop look like a generic wireframe.
2. **Sterile White-Box Cards**: Standard e-commerce grids rely on uniform white rectangles with identical typography, stripping away all craft, warmth, and brand personality.
3. **Lifeless Empty Cart States**: When a user empties their shopping bag, most AI-generated storefronts show a bare `"Your cart is empty"` text string.

`CC-lineart` turns an AI agent into a self-sufficient **boutique art director and illustrator**:
- **Bespoke Vector Product Illustrations**: Every SKU on the shelf (*Artisan Ceramic V60 Dripper*, *Dot-Grid Field Monograph*, *Tactile Terracotta Keycap Set*, *Waxed Canvas Cable Satchel*, *Visual Architecture Prompt Deck*, and *Atelier Brass Studio Lamp*) is drawn directly in inline SVG over its own color-coded watercolor wash (`clay`, `cactus`, `sky`, `kraft`, `heather`, `olive`).
- **Tactile Merchandising Chrome**: Hand-drawn hanging **Price Tags** (`$42`, `$24`, `$68`) with punch-holes, rotated **Stamp Badges** (`BESTSELLER`, `LIMITED`, `STUDIO PICK`), and hover watercolor parallax (`transform: translate(5px, -4px) scale(1.05)`) give every product card the feel of a physical print catalog.
- **Interactive Field Bag with Illustrated Empty State**: Clicking `+ Add to Bag` updates the live subtotal and item counter; clicking `Empty bag` reveals a custom `CC-lineart` **Empty Tote Bag** illustration instead of plain text.

---

## 2. Deliverables & Automated Quality Gate (`scripts/lineart.py lint`)

| Deliverable | Dimensions / Format | Role | Lint Status |
| :--- | :--- | :--- | :--- |
| `generate_storefront.py` | Python 3 generator | Deterministic generator for the 512×512 Storefront Showcase SVG, PNG, and interactive HTML shop | N/A |
| `storefront-showcase.svg` | `512 × 512` SVG | Promo banner centerpiece (*Curated Boutique Shelf, Pour-Over Dripper, Field Monograph & Tote Bag*) | **0 warnings** |
| `storefront-showcase.png` | `512 × 512` PNG | Rasterized preview rendered on `#FAF9F5` warm cream paper | Verified |
| `marketplace-storefront.html` | Self-contained HTML5 | Interactive Boutique E-Commerce Storefront with category filtering & live shopping bag | Verified |

### `lineart.py lint` Output (`storefront-showcase.svg`)

```text
OK    no clip-art geometry found in the markup
OK    block visible: 40% of the wash shows (want ≥ 30%)
OK    color coverage: 17% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 67% (want ≤ 80%; the art should break out of the block)

0 warning(s).
```
