# enezeg — Style Guidelines

Brand system, colour palette, typography scale and design tokens for [enezeg.com](https://enezeg.com).

---

## Mark

The enezeg mark is an organic dot cluster representing an archipelago — the meaning of *enezeg* in Breton.

**Geometry — 5 dots, cascade composition:**

| dot | role | colour (dark) | colour (light) | size |
|-----|------|---------------|----------------|------|
| 1 | ghost — top-left anchor | `#ede9e0` @ 22% | `#0e0e0e` @ 22% | r 2.5 |
| 2 | small — slate | `#4464a8` | `#2e4a7a` | r 5 |
| 3 | large — dominant island | `#ede9e0` | `#0e0e0e` | r 8 |
| 4 | accent — indigo | `#4a80d4` | `#2952a3` | r 4 |
| 5 | accent ghost | `#4a80d4` @ 45% | `#2952a3` @ 45% | r 2.5 |

**SVG viewBox:** `0 0 46 46`

**Dot positions:**

```
cx="11" cy="19"   ghost
cx="17" cy="26"   slate
cx="29" cy="18"   dominant
cx="37" cy="30"   indigo
cx="29" cy="36"   indigo ghost
```

**Usage rules:**
- Never recolour individual dots outside the defined palette
- Minimum display size: 16×16px — below this use the mark without the ghost dot
- Always maintain the `0 0 46 46` viewBox — do not crop or reframe
- Favicon: mark on `#0c0f12` background, rounded rect (rx 10)

---

## Wordmark

**Typeface:** Inter 300 (Light)  
**Licence:** SIL Open Font License 1.1 — free for commercial use  
**Source:** [Google Fonts](https://fonts.google.com/specimen/Inter) or self-hosted

**Logo lockup:**
- Gap between mark and wordmark: `5px`
- Mark `margin-top: 5px` to optically centre against cap height
- Wordmark `font-size: 18px` in nav, `28px` in full logo SVG
- Text baseline `y="31"` in SVG (`viewBox="0 0 180 46"`)

**SVG files:**
- `static/enezeg-logo-light.svg` — ink wordmark, light backgrounds
- `static/enezeg-logo-dark.svg` — warm white wordmark, dark backgrounds

---

## Colour palette

All colours are defined as CSS custom properties and toggled via `[data-theme]` on `<html>`.

### Light mode

| token | value | role |
|-------|-------|------|
| `--canvas` | `#faf8f4` | page background |
| `--surface` | `#f2efe9` | cards, panels |
| `--subtle` | `#e8e4dc` | borders, dividers, hover states |
| `--ink` | `#0e0e0e` | primary text, headings |
| `--muted` | `#4a4540` | secondary text, captions |
| `--faint` | `#9a9490` | placeholders, labels |
| `--slate` | `#2e4a7a` | mark secondary dot |
| `--indigo` | `#2952a3` | primary accent, links, CTAs |
| `--indigo-tint` | `#d8e4f8` | accent backgrounds, badges |
| `--umber` | `#8a6a40` | warm accent, callouts |
| `--umber-tint` | `#f2e8d8` | warm backgrounds, notices |
| `--border` | `rgba(0,0,0,0.08)` | borders |

### Dark mode

| token | value | role |
|-------|-------|------|
| `--canvas` | `#0c0f12` | page background |
| `--surface` | `#141820` | cards, panels |
| `--subtle` | `#1e2530` | borders, dividers, hover states |
| `--ink` | `#ede9e0` | primary text, headings |
| `--muted` | `#8a8680` | secondary text, captions |
| `--faint` | `#2a3040` | placeholders, labels |
| `--slate` | `#4464a8` | mark secondary dot |
| `--indigo` | `#4a80d4` | primary accent, links, CTAs |
| `--indigo-tint` | `#1a2848` | accent backgrounds, badges |
| `--umber` | `#c49858` | warm accent, callouts |
| `--umber-tint` | `#1e180e` | warm backgrounds, notices |
| `--border` | `rgba(255,255,255,0.06)` | borders |

**Default mode:** dark. User preference stored in `localStorage` key `enezeg-theme`.

---

## Typography

### Typefaces

| face | weight | role |
|------|--------|------|
| Inter | 300 | all headings, body, UI text |
| DM Mono | 300, 400 | labels, tags, dates, code, eyebrows |

Both loaded from Google Fonts. Self-hosting recommended for production (eliminates render-blocking request).

### Type scale — minor third (×1.2), rooted at 16px

| token | size | line-height | tracking | role |
|-------|------|-------------|----------|------|
| `--text-4xl` | 52px | 1.15 | −0.025em | display |
| `--text-3xl` | 40px | 1.15 | −0.025em | hero name |
| `--text-2xl` | 32px | 1.3 | −0.015em | H1 — page title |
| `--text-xl` | 26px | 1.3 | −0.015em | H2 — section title |
| `--text-lg` | 22px | 1.55 | −0.015em | H3 — subsection |
| `--text-md` | 19px | 1.7 | 0 | lead paragraph |
| `--text-base` | 16px | 1.7 | 0 | body copy |
| `--text-sm` | 13px | 1.85 | 0 | secondary text, captions |
| `--text-xs` | 11px | 1.85 | 0.12em+ | mono labels, tags |

### Letter spacing tokens

| token | value | use |
|-------|-------|-----|
| `--tracking-tight` | −0.025em | display |
| `--tracking-snug` | −0.015em | headings |
| `--tracking-normal` | 0em | body |
| `--tracking-wide` | 0.04em | small labels |
| `--tracking-wider` | 0.12em | mono tags |
| `--tracking-widest` | 0.2em | uppercase eyebrow |

### Spacing scale — 4px base

| token | value | use |
|-------|-------|-----|
| `--space-1` | 4px | icon gap |
| `--space-2` | 8px | tight inline |
| `--space-3` | 12px | eyebrow → title |
| `--space-4` | 16px | title → bio |
| `--space-5` | 24px | bio → CTA, prose paragraphs |
| `--space-6` | 32px | nav items, card padding |
| `--space-7` | 48px | section header → content |
| `--space-8` | 64px | column gap |
| `--space-9` | 96px | hero padding |
| `--space-10` | 128px | section gap (large) |

### Prose rhythm

| token | value |
|-------|-------|
| `--prose-gap` | 20px — between paragraphs |
| `--heading-above` | 48px — space above H2 in prose |
| `--heading-below` | 16px — space below heading |
| `--section-gap` | 80px — between page sections |

---

## Component patterns

### Buttons

```css
.btn-primary  background: var(--indigo);   color: #faf8f4
.btn-ghost    border: 1px solid var(--indigo-tint);  color: var(--indigo)
```

Hover: `translateY(-1px)`, darken background.

### Tags / badges

```css
background: var(--indigo-tint);  color: var(--indigo)
font-family: var(--font-mono);   font-size: var(--text-xs)
letter-spacing: var(--tracking-wider);  text-transform: uppercase
padding: 2px 8px;  border-radius: 3px
```

### Code blocks

Inline: `var(--umber)` on `var(--surface)` background, 1px `var(--border)` border.  
Block: `var(--surface)` background, syntax theme `dracula` via Hugo.

### Cards

Border: `1px solid var(--border)` → hover `var(--slate)`.  
Hover lift: `translateY(-2px)`, `box-shadow: 0 8px 32px rgba(0,0,0,0.2)`.

---

## Layout

| value | use |
|-------|-----|
| `--max-width: 720px` | prose, single pages |
| `--max-wide: 1080px` | nav, section containers |
| `--radius: 6px` | cards, buttons, code blocks |
| Nav height | 60px, sticky |
| Section padding | 80px top/bottom |
| Hero padding | 100px top, 80px bottom |

---

## Responsive breakpoints

| breakpoint | changes |
|------------|---------|
| ≤ 768px | single column, hero mark hidden, nav compacted |
| ≤ 480px | full-width buttons, reduced hero font size |
