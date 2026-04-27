#!/usr/bin/env python3
"""
letter-pdf.py — enezeg letter generator (reportlab)
Usage: python letter-pdf.py --config letter.toml [--out output.pdf]
"""

import argparse
import sys
import tomllib
from datetime import date
from typing import Any

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    Paragraph,
    Spacer,
)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame

# ── Fonts ────────────────────────────────────────────────────────────────────
SANS_L, SANS, SANS_B, MONO = "PL", "PB", "PB", "PL"


def register_fonts(fd: str):
    pdfmetrics.registerFont(TTFont("PL", f"{fd}/Inter-Light.ttf"))
    pdfmetrics.registerFont(TTFont("PR", f"{fd}/Inter-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("PB", f"{fd}/Inter-Bold.ttf"))

# ── Colours ──────────────────────────────────────────────────────────────────
INK = HexColor("#0E0E0E")
MUTED = HexColor("#4A4540")
FAINT = HexColor("#9A9490")
BORDER = HexColor("#E8E4DC")
INDIGO = HexColor("#2952A3")
SLATE = HexColor("#2E4A7A")

# ── Sender ───────────────────────────────────────────────────────────────────
SENDER = {
    "name": "Loïc Diridollou",
    "title": "Quantitative Researcher",
    "email": "loic@enezeg.com",
    "website": "enezeg.com",
    "city": "New York, NY",
}

# ── Geometry ─────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch
CW = PAGE_W - 2 * MARGIN
H1 = 1.05 * inch  # page-1 header height
Hn = 0.38 * inch  # subsequent header height
FH = 0.38 * inch  # footer height


# ── Mark ─────────────────────────────────────────────────────────────────────
def draw_mark(cv, x, y, size=22):
    s = size / 46

    def dot(cx, cy, r, c, a=1.0):
        cv.saveState()
        cv.setFillColor(c)
        cv.setFillAlpha(a)
        cv.circle(x + cx * s, y + (46 - cy) * s, r * s, stroke=0, fill=1)
        cv.restoreState()

    dot(11, 19, 2.5, INK, 0.22)
    dot(17, 26, 5.0, SLATE, 1.0)
    dot(29, 18, 8.0, INK, 1.0)
    dot(37, 30, 4.0, INDIGO, 1.0)
    dot(29, 36, 2.5, INDIGO, 0.45)


def draw_wm(cv, x, y, size=14):
    cv.setFont(SANS_L, size)
    cv.setFillColor(INK)
    cv.drawString(x, y, "enezeg")


# ── Border line helper ────────────────────────────────────────────────────────
def hline(cv, y):
    cv.setStrokeColor(BORDER)
    cv.setLineWidth(0.5)
    cv.line(MARGIN, y, PAGE_W - MARGIN, y)


# ── Headers / footer ─────────────────────────────────────────────────────────
def hdr_p1(cv: rl_canvas.Canvas, doc):
    s = doc.sender
    cv.saveState()
    ms = 30
    mx = MARGIN
    my = PAGE_H - H1 + (H1 - ms) / 2
    draw_mark(cv, mx, my, ms)
    draw_wm(cv, mx + ms + 6, my + ms * 0.30, 16)
    rx = PAGE_W - MARGIN
    ny = PAGE_H - 0.42 * inch
    cv.setFont(SANS_L, 9.5)
    cv.setFillColor(INK)
    cv.drawRightString(rx, ny, s["name"])
    cv.setFont(MONO, 7)
    cv.setFillColor(FAINT)
    for i, t in enumerate([s["email"], s["website"], s["city"]]):
        cv.drawRightString(rx, ny - (i + 1) * 11, t)
    hline(cv, PAGE_H - H1)
    footer(cv, doc)
    cv.restoreState()


def hdr_pn(cv: rl_canvas.Canvas, doc):
    s = doc.sender
    cv.saveState()
    by = PAGE_H - Hn
    ty = by + (Hn - 8) / 2
    ms = 16
    draw_mark(cv, MARGIN, by + (Hn - ms) / 2, ms)
    cv.setFont(SANS_L, 9)
    cv.setFillColor(INK)
    cv.drawString(MARGIN + ms + 4, ty, "enezeg")
    cv.setFont(MONO, 7)
    cv.setFillColor(FAINT)
    cv.drawRightString(PAGE_W - MARGIN, ty, f"{s['name']}  ·  {doc.letter_date}")
    hline(cv, by)
    footer(cv, doc)
    cv.restoreState()


def footer(cv: rl_canvas.Canvas, doc):
    s = doc.sender
    cv.saveState()
    ty = (FH - 8) / 2
    hline(cv, FH)
    ms = 14
    draw_mark(cv, MARGIN, (FH - ms) / 2, ms)
    cv.setFont(SANS_L, 8)
    cv.setFillColor(INK)
    cv.drawString(MARGIN + ms + 4, ty + 1, "enezeg")
    cv.setFont(MONO, 7)
    cv.setFillColor(FAINT)
    cv.drawCentredString(PAGE_W / 2, ty + 2, s["website"])
    cv.drawRightString(PAGE_W - MARGIN, ty + 2, f"p. {cv.getPageNumber()}")
    cv.restoreState()


# ── DocTemplate ───────────────────────────────────────────────────────────────
class LetterDoc(BaseDocTemplate):
    def __init__(self, fn, sender, letter_date, **kw):
        super().__init__(fn, **kw)
        self.sender = sender
        self.letter_date = letter_date
        kw2 = dict(leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        fp1 = Frame(MARGIN, FH + 8, CW, PAGE_H - H1 - FH - 16, id="p1", **kw2)
        fpn = Frame(MARGIN, FH + 8, CW, PAGE_H - Hn - FH - 16, id="pn", **kw2)
        self.addPageTemplates(
            [
                PageTemplate(id="FirstPage", frames=[fp1], onPage=hdr_p1),
                PageTemplate(id="LaterPages", frames=[fpn], onPage=hdr_pn),
            ]
        )


# ── Styles ────────────────────────────────────────────────────────────────────
def styles():
    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "date": s(
            "D",
            fontName=MONO,
            fontSize=7.5,
            textColor=FAINT,
            leading=9,
            spaceAfter=3.5 * mm,
        ),
        "rname": s(
            "RN", fontName=SANS_B, fontSize=9, textColor=INK, leading=12, spaceAfter=3
        ),
        "rline": s(
            "RL", fontName=SANS_L, fontSize=9, textColor=MUTED, leading=12, spaceAfter=3
        ),
        "slabel": s(
            "SL", fontName=MONO, fontSize=6.5, textColor=FAINT, leading=8, spaceAfter=1
        ),
        "subject": s(
            "SU",
            fontName=SANS_L,
            fontSize=10,
            textColor=INK,
            leading=13,
            spaceAfter=2.5 * mm,
        ),
        "salut": s(
            "SA",
            fontName=SANS_L,
            fontSize=9,
            textColor=INK,
            leading=13,
            spaceAfter=3.5 * mm,
        ),
        "body": s(
            "B",
            fontName=SANS_L,
            fontSize=9,
            textColor=MUTED,
            leading=15,
            spaceAfter=3 * mm,
            alignment=TA_JUSTIFY,
        ),
        "closing": s(
            "CL",
            fontName=SANS_L,
            fontSize=9,
            textColor=INK,
            leading=13,
            spaceBefore=2.5 * mm,
            spaceAfter=8 * mm,
        ),
        "signame": s(
            "SN", fontName=SANS_L, fontSize=9, textColor=INK, leading=13, spaceAfter=1
        ),
        "sigtitle": s(
            "ST", fontName=MONO, fontSize=7, textColor=FAINT, leading=9, spaceAfter=0
        ),
        "enclabel": s(
            "EL",
            fontName=MONO,
            fontSize=7,
            textColor=FAINT,
            leading=9,
            spaceBefore=3 * mm,
            spaceAfter=2 * mm,
        ),
        "encitem": s(
            "EI",
            fontName=SANS_L,
            fontSize=8.5,
            textColor=MUTED,
            leading=11,
            spaceAfter=1,
        ),
    }


# ── Story ─────────────────────────────────────────────────────────────────────
def build_story(data, st):
    story: list[Any] = [NextPageTemplate("LaterPages")]

    def hr():
        return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=4 * mm)

    story.append(Paragraph(data.get("letter_date", ""), st["date"]))
    story.append(Spacer(1, 2 * mm))

    rb = [Paragraph(data.get("recipient_name", ""), st["rname"])]
    for address_info in data.get("recipient_address", []):
        rb.append(Paragraph(address_info, st["rline"]))
    story.append(KeepTogether(rb))  # type: ignore
    story.append(Spacer(1, 5 * mm))

    story.append(
        KeepTogether(
            [
                Paragraph("RE", st["slabel"]),
                Paragraph(data.get("subject", ""), st["subject"]),
                hr(),
            ]
        )
    )

    story.append(Paragraph(data.get("salutation", ""), st["salut"]))

    for p in data.get("paragraphs", []):
        story.append(Paragraph(p, st["body"]))

    story.append(Spacer(1, 2 * mm))
    story.append(
        KeepTogether(
            [
                Paragraph(data.get("closing", "Yours sincerely,"), st["closing"]),
                Paragraph(data.get("sender_name", ""), st["signame"]),
                Paragraph(data.get("sender_title", ""), st["sigtitle"]),
            ]
        )
    )

    encs = data.get("enclosures", [])
    if encs:
        eb = [
            Spacer(1, 4 * mm),
            HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=2 * mm),
            Paragraph("ENCLOSURES", st["enclabel"]),
        ]
        for i, e in enumerate(encs):
            eb.append(Paragraph(f"{i+1}.  {e}", st["encitem"]))
        story.append(KeepTogether(eb))
    return story


# ── Generate ──────────────────────────────────────────────────────────────────
def generate(data, sender, out):
    ld = data.get("letter_date", date.today().strftime("%B %-d, %Y"))
    d = {
        **data,
        "letter_date": ld,
        "sender_name": sender["name"],
        "sender_title": sender["title"],
    }
    doc = LetterDoc(
        out,
        sender=sender,
        letter_date=ld,
        pagesize=letter,
        leftMargin=0,
        rightMargin=0,
        topMargin=0,
        bottomMargin=0,
    )
    doc.build(build_story(d, styles()))
    print(f"\n  ✓  PDF written to {out}\n")


# ── TOML ─────────────────────────────────────────────────────────────────────
def load_toml(path):
    if not tomllib:
        sys.exit("pip install tomli")
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    letter_info = cfg.get("letter", {})
    return {
        "letter_date": letter_info.get("date", date.today().strftime("%B %-d, %Y")),
        "recipient_name": letter_info.get("recipient_name", ""),
        "recipient_address": letter_info.get("recipient_address", []),
        "subject": letter_info.get("subject", ""),
        "salutation": letter_info.get("salutation", ""),
        "paragraphs": letter_info.get("paragraphs", []),
        "closing": letter_info.get("closing", "Yours sincerely,"),
        "enclosures": letter_info.get("enclosures", []),
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-c")
    p.add_argument("--out", "-o", default="")
    p.add_argument("--fonts", "-f", required=True, help="Path to folder containing Inter-Light/Regular/Bold.ttf")
    a = p.parse_args()
    register_fonts(a.fonts)
    data = load_toml(a.config) if a.config else {}
    slug = data.get("recipient_name", "letter").lower().replace(" ", "-")
    out = a.out or f"letter-{date.today().strftime('%Y-%m-%d')}-{slug}.pdf"
    generate(data, SENDER, out)


if __name__ == "__main__":
    main()
