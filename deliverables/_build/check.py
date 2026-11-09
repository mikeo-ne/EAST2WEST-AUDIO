"""Structural self-check for the deck: bounds + estimated text overflow per textbox."""
from pptx import Presentation
from pptx.util import Emu
from PIL import ImageFont
import glob

REG = glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True)[0]
BOLD = glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf', recursive=True)[0]
CACHE = {}
def f(pt, bold):
    k = (round(pt*2), bold)
    if k not in CACHE: CACHE[k] = ImageFont.truetype(BOLD if bold else REG, max(6, round(pt*96/72)))
    return CACHE[k]

prs = Presentation('/home/user/EAST2WEST-AUDIO/deliverables/Baranga-12-Week-Strategic-Marketing-Plan.pptx')
SW, SH = prs.slide_width, prs.slide_height
issues = 0
for idx, slide in enumerate(prs.slides, 1):
    for sh in slide.shapes:
        if sh.left is None: continue
        if sh.left < -1000 or sh.top < -1000 or sh.left+sh.width > SW+1000 or sh.top+sh.height > SH+1000:
            print(f"slide {idx}: out of bounds"); issues += 1
        if not sh.has_text_frame: continue
        tf = sh.text_frame
        if not "".join(r.text for p in tf.paragraphs for r in p.runs).strip(): continue
        avail_pt = Emu(sh.width - tf.margin_left - tf.margin_right).pt
        need = 0.0
        for p in tf.paragraphs:
            runs = [r for r in p.runs if r.text]
            if not runs: need += 6; continue
            sz = max((r.font.size.pt if r.font.size else 14) for r in runs)
            bold = any(r.font.bold for r in runs)
            fnt = f(sz, bold)
            words = "".join(r.text for r in runs).split(" ")
            lines, cur = 1, ""
            for w in words:
                t = (cur + " " + w).strip()
                if fnt.getlength(t) * 0.94 <= avail_pt * 96/72 or not cur: cur = t
                else: lines += 1; cur = w
            need += lines * sz * 1.2 + (p.space_after.pt if p.space_after else 0)
        avail_h = Emu(sh.height - tf.margin_top - tf.margin_bottom).pt * 1.1
        if need > avail_h + 3:
            print(f"slide {idx}: text overflows box by {need-avail_h:.0f}pt :: "
                  f"{''.join(r.text for p in tf.paragraphs for r in p.runs)[:64]!r}")
            issues += 1
print("issues:", issues)
