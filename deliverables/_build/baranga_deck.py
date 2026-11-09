"""
Baranga 12-Week Strategic Marketing Assignment — delivered as a PowerPoint deck.
Rebuilt around the corrected artist profile: Afro-pop / rap, not an acoustic guitarist.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ---------------------------------------------------------------- palette
INK      = RGBColor(0x0C, 0x0C, 0x0F)   # near-black
COAL     = RGBColor(0x16, 0x16, 0x1B)   # card
COAL2    = RGBColor(0x1E, 0x1E, 0x25)   # card alt
GOLD     = RGBColor(0xE8, 0xB4, 0x4A)   # 7H gold
AMBER    = RGBColor(0xFF, 0xC9, 0x5C)
TEAL     = RGBColor(0x2F, 0xB6, 0xA8)
TERRA    = RGBColor(0xC8, 0x6B, 0x4A)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
MUTED    = RGBColor(0xA9, 0xA9, 0xB4)
LINE     = RGBColor(0x2C, 0x2C, 0x36)

HEAD = "Arial"          # safe, ships everywhere
BODY = "Arial"


# ---------------------------------------------------------------- text metrics
from PIL import ImageFont
import glob as _glob
_FONTS = {}
def _fontfile(bold):
    key = "b" if bold else "r"
    if key not in _FONTS:
        cand = {False: ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"],
                True: ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf"]}[bold]
        found = None
        for c in cand:
            hits = _glob.glob("/usr/share/fonts/**/%s" % c, recursive=True)
            if hits:
                found = hits[0]; break
        _FONTS[key] = found
    return _FONTS[key]

_FT = {}
def _pil(sz_pt, bold):
    f = _fontfile(bold)
    if f is None:
        return None
    key = (round(sz_pt, 1), bold)
    if key not in _FT:
        _FT[key] = ImageFont.truetype(f, max(6, int(round(sz_pt * 4))))  # 4x for precision, /4 below
    return _FT[key]

def text_width_pt(txt, sz_pt, bold=False):
    """Width in points. DejaVu is ~6% wider than Arial, so this is conservative."""
    f = _pil(sz_pt, bold)
    if f is None:
        return len(txt) * sz_pt * 0.52
    return f.getlength(txt) / 4.0 * 0.94

def wrap_lines(txt, sz_pt, bold, avail_pt):
    """Greedy word wrap; returns list of lines."""
    words = txt.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width_pt(trial, sz_pt, bold) <= avail_pt or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def para_height_pt(txt, sz_pt, bold, avail_pt, leading=1.15):
    n = len(wrap_lines(txt, sz_pt, bold, max(avail_pt, 20)))
    return n * sz_pt * leading * 1.0, n

W, H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]

# ---------------------------------------------------------------- helpers
def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = INK
    bg.line.fill.background()
    bg.shadow.inherit = False
    # keep bg behind everything
    s.shapes._spTree.remove(bg._element)
    s.shapes._spTree.insert(2, bg._element)
    return s

def no_shadow(shp):
    shp.shadow.inherit = False
    return shp

def rect(s, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE, radius=None):
    shp = s.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = radius
    return shp

def text(s, x, y, w, h, runs, size=14, color=WHITE, bold=False, font=BODY,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, leading=1.15, space_after=0,
         caps=False, italic=False):
    """runs: str | list[str] | list[(str, dict)] | list[list[(str,dict)]] (paragraphs)"""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) and runs and isinstance(runs[0], list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = leading
        p.space_after = Pt(space_after)
        items = para if isinstance(para, list) else [(para, {})]
        for txt, opt in items:
            r = p.add_run()
            r.text = txt.upper() if opt.get("caps", caps) else txt
            f = r.font
            f.name = opt.get("font", font)
            f.size = Pt(opt.get("size", size))
            f.bold = opt.get("bold", bold)
            f.italic = opt.get("italic", italic)
            f.color.rgb = opt.get("color", color)
    return tb

def bullets(s, x, y, w, items, size=12.5, gap=9, color=MUTED, dot=GOLD, dot_size=5.5,
            h=None, leading=1.2, max_bottom=None, warn=""):
    """Hanging-indent bullets. Height is measured so nothing overlaps."""
    cy = y
    text_w = w - Pt(16)
    for it in items:
        rect(s, x, cy + Pt(size * 0.45), Pt(dot_size), Pt(dot_size), fill=dot)
        hh_pt, nlines = para_height_pt(it, size, False, Emu(text_w).pt, leading)
        hh_pt *= 1.06
        tb = text(s, x + Pt(16), cy, text_w, Pt(hh_pt + size * 1.3), it, size=size, color=color,
                  leading=leading)
        cy += Pt(hh_pt) + Pt(gap)
    return cy

def chip(s, x, y, w, h, label, fill=COAL2, fg=GOLD, size=9.5, line=LINE):
    rect(s, x, y, w, h, fill=fill, line=line, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.35)
    text(s, x + Inches(0.10), y, w - Inches(0.20), h, label, size=size, color=fg,
         bold=True, anchor=MSO_ANCHOR.MIDDLE, caps=True, align=PP_ALIGN.CENTER)

def eyebrow(s, label, y=Inches(0.52), color=GOLD):
    text(s, Inches(0.85), y, Inches(9), Inches(0.28), label, size=10.5, color=color,
         bold=True, caps=True)
    rect(s, Inches(0.85), y + Inches(0.34), Inches(0.52), Pt(2.2), fill=color)

def headline(s, lines, y=Inches(1.02), size=33, w=Inches(11.6), color=WHITE):
    text(s, Inches(0.85), y, w, Inches(1.6), lines, size=size, color=color, bold=True,
         font=HEAD, leading=1.02)

def footer(s, num, label="Baranga · 12-Week Strategic Marketing Plan · 7H Music Group"):
    rect(s, Inches(0.85), Inches(6.86), Inches(11.63), Pt(0.75), fill=LINE)
    text(s, Inches(0.85), Inches(6.98), Inches(9), Inches(0.28), label, size=8.5, color=MUTED)
    text(s, Inches(11.4), Inches(6.98), Inches(1.1), Inches(0.28), f"{num:02d}", size=8.5,
         color=GOLD, bold=True, align=PP_ALIGN.RIGHT, font=HEAD)

def bullets_need(w, items, size, gap):
    """Total height (points) bullets() will occupy."""
    total = 0.0
    for it in items:
        hh, _ = para_height_pt(it, size, False, Emu(w - Pt(16)).pt, 1.2)
        total += hh * 1.06 + gap
    return total - gap

def card_need(w, title, items, title_size, body_size, tag, gap=7):
    inner_w = w - Inches(0.52)
    th, _ = para_height_pt(title, title_size, True, Emu(inner_w).pt, 1.05)
    top = Inches(0.46) if tag else Inches(0.22)
    return top + Pt(th) + Pt(7) + Pt(bullets_need(inner_w, items, body_size, gap)) + Inches(0.20)

def card(s, x, y, w, h, title, body_items, accent=GOLD, title_size=13.5, body_size=11.5,
         tag=None, gap=7):
    # fit type to the box instead of overflowing it
    _start = body_size
    while body_size > 9.9 and card_need(w, title, body_items, title_size, body_size, tag, gap) > h - Pt(4):
        body_size -= 0.4

    rect(s, x, y, w, h, fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, y, Pt(3.2), h, fill=accent)
    inner_w = w - Inches(0.52)
    if tag:
        text(s, x + Inches(0.26), y + Inches(0.20), inner_w, Inches(0.24), tag,
             size=8.5, color=accent, bold=True, caps=True)
        ty = y + Inches(0.46)
    else:
        ty = y + Inches(0.22)
    th_pt, _ = para_height_pt(title, title_size, True, Emu(inner_w).pt, 1.05)
    text(s, x + Inches(0.26), ty, inner_w, Pt(th_pt + 2), title, size=title_size,
         color=WHITE, bold=True, font=HEAD, leading=1.05)
    bullets(s, x + Inches(0.26), ty + Pt(th_pt) + Pt(7), inner_w, body_items,
            size=body_size, dot=accent, gap=gap, max_bottom=y + h - Pt(6), warn=title)

def table(s, x, y, w, col_w, rows, head_h=Inches(0.42), row_h=Inches(0.46),
          head_fill=GOLD, head_fg=INK, size=10.5, head_size=9.3, zebra=True,
          align_cols=None, bold_first_col=True, gap_pt=6, max_bottom=None):
    """rows[0] = header. col_w relative weights. Row heights grow to fit 2-line cells."""
    total = sum(col_w)
    widths = [Emu(int(w * c / total)) for c in col_w]

    def row_need(cells, sz, bold_cols):
        need = 0.0
        for i, cell in enumerate(cells):
            lines_w = Emu(widths[i] - Inches(0.26)).pt
            hh, _ = para_height_pt(cell, sz, (i == 0 and bold_cols), lines_w, 1.12)
            need = max(need, hh)
        return Pt(need) + Pt(gap_pt)

    cy = y
    # header
    hh_ = max(head_h, row_need(rows[0], head_size, True))
    rect(s, x, cy, w, hh_, fill=head_fill)
    cx = x
    for i, cell in enumerate(rows[0]):
        text(s, cx + Inches(0.13), cy, widths[i] - Inches(0.26), hh_, cell, size=head_size,
             color=head_fg, bold=True, caps=True, anchor=MSO_ANCHOR.MIDDLE, leading=1.1)
        cx += widths[i]
    cy += hh_
    for ri, row in enumerate(rows[1:]):
        spec = row_h[ri] if isinstance(row_h, (list, tuple)) else row_h
        h = max(spec, row_need(row, size, bold_first_col))
        if zebra and ri % 2 == 1:
            rect(s, x, cy, w, h, fill=COAL)
        rect(s, x, cy + h, w, Pt(0.6), fill=LINE)
        cx = x
        for i, cell in enumerate(row):
            text(s, cx + Inches(0.13), cy, widths[i] - Inches(0.26), h, cell, size=size,
                 color=WHITE if (i == 0 and bold_first_col) else MUTED,
                 bold=(i == 0 and bold_first_col), anchor=MSO_ANCHOR.MIDDLE, leading=1.12,
                 align=(align_cols or {}).get(i, PP_ALIGN.LEFT))
            cx += widths[i]
        cy += h
    if max_bottom is not None and cy > max_bottom:
        print(f"  !! table bottom {Emu(cy).inches:.2f}in > {Emu(max_bottom).inches:.2f}in")
    return cy
