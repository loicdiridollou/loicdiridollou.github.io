# enezeg.com

Personal website of [Loic Diridollou](https://enezeg.com) — built with [Hugo](https://gohugo.io) and deployed via GitHub Pages.

---

### stack

```
framework   Hugo
theme       enezeg (custom, in themes/enezeg/)
deploy      GitHub Actions → GitHub Pages
domain      enezeg.com
server      nginx (Dockerfile for local preview)
```

---

### local development

**Prerequisites:** Hugo extended ≥ 0.110.0

```bash
git clone --recurse-submodules https://github.com/loicdiridollou/loicdiridollou.github.io
cd loicdiridollou.github.io
hugo server
```

Open [http://localhost:1313](http://localhost:1313).

**With Docker:**

```bash
docker build -t enezeg .
docker run -p 8080:80 enezeg
```

Open [http://localhost:8080](http://localhost:8080).

---

### content

```
content/
  about/        _index.md
  contact/      _index.md
  projects/     _index.md + one file per project
  writing/      _index.md + one file per post
```

**New post:**

```bash
hugo new writing/my-post-title.md
```

**New project:**

```bash
hugo new projects/my-project.md
```

Front matter reference is in `themes/enezeg/README.md`.

---

### deploy

Pushes to `main` trigger the GitHub Actions workflow (`.github/workflows/`), which builds with Hugo and publishes to GitHub Pages. The custom domain `enezeg.com` is set via the `CNAME` file.

---

### theme

The `enezeg` theme lives in `themes/enezeg/`. Brand guidelines, colour tokens and typography scale are documented in [`STYLE.md`](./STYLE.md).

---

### license

Site content © Loic Diridollou. Theme source code under GPL-3.0 — see [`LICENSE`](./LICENSE).
