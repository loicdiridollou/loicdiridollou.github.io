# enezeg — Hugo Theme

A minimal, dark-first personal site theme built around the enezeg brand system.

## Features

- Dark mode by default, toggleable to light
- System preference respected on first visit
- Five sections: hero, projects, writing, about, contact
- Responsive, mobile-first
- Zero JavaScript dependencies (vanilla JS only)
- Fade-in on scroll
- Syntax highlighted code blocks
- DM Mono + Inter 300 typography

## Quick start

### 1. Add the theme

```bash
# As a git submodule (recommended)
git submodule add https://github.com/loicdiridollou/enezeg themes/enezeg

# Or copy the theme folder directly into your Hugo site
cp -r enezeg-theme themes/enezeg
```

### 2. Update hugo.toml

```toml
theme = "enezeg"

[params]
  author      = "Your Name"
  description = "Your site description"
  role        = "your · role"
  bio         = "Short hero bio."
  about       = "Longer about section text."
  contactNote = "How you like to be reached."
  email       = "you@example.com"
  github      = "yourusername"
  twitter     = "yourusername"   # optional
  linkedin    = "yourusername"   # optional
  stack       = ["Python", "Rust", "Go"]
```

### 3. Create content

```bash
# New project
hugo new projects/my-project.md

# New post
hugo new writing/my-post.md
```

### 4. Project front matter

```yaml
---
title: "my-project"
date: 2025-01-01
description: "One line description."
tag: "python"        # shown as badge
lang: "Python"       # shown in card footer
stars: 42            # optional GitHub stars
status: "active"     # active | wip | archive
github: "https://github.com/..."
---
```

### 5. Writing front matter

```yaml
---
title: "Post title"
date: 2025-01-01
description: "Optional subtitle."
tag: "quant"         # shown as badge
---
```

## Deploy to GitHub Pages

Add `.github/workflows/hugo.yml`:

```yaml
name: Deploy Hugo site

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true
      - run: hugo --minify
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

## Colour tokens

| Token           | Light       | Dark        | Role                        |
|-----------------|-------------|-------------|-----------------------------|
| `--canvas`      | `#faf8f4`   | `#0c0f12`   | Page background             |
| `--surface`     | `#f2efe9`   | `#141820`   | Cards, panels               |
| `--subtle`      | `#e8e4dc`   | `#1e2530`   | Borders, dividers           |
| `--ink`         | `#0e0e0e`   | `#ede9e0`   | Primary text                |
| `--muted`       | `#4a4540`   | `#8a8680`   | Secondary text              |
| `--slate`       | `#2e4a7a`   | `#4464a8`   | Mark secondary dot          |
| `--indigo`      | `#2952a3`   | `#4a80d4`   | Primary accent, links, CTAs |
| `--indigo-tint` | `#d8e4f8`   | `#1a2848`   | Accent backgrounds          |
| `--umber`       | `#8a6a40`   | `#c49858`   | Warm accent, callouts       |
| `--umber-tint`  | `#f2e8d8`   | `#1e180e`   | Warm backgrounds            |

## License

MIT
