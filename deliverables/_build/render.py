"""Mock-render the deck to PNGs straight from the pptx (rects + text only)."""
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image, ImageDraw, ImageFont
import glob, os, math

REG = glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True)[0]
BOLD = glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf', recursive=True)[0]
S = 96/914400.0   # emu -> px at 96dpi
FT = {}
def font(pt, bold):
    k=(round(pt*2), bold)
    if k not in FT: FT[k]=ImageFont.truetype(BOLD if bold else REG, max(6,int(round(pt*96/72))))
    return FT[k]

def emu(v): return int(round(v*S))

prs = Presentation('/home/user/EAST2WEST-AUDIO/deliverables/Baranga-12-Week-Strategic-Marketing-Plan.pptx')
Wpx, Hpx = emu(prs.slide_width), emu(prs.slide_height)
os.makedirs('preview', exist_ok=True)
for idx, slide in enumerate(prs.slides, 1):
    img = Image.new('RGB', (Wpx, Hpx), (12,12,15))
    d = ImageDraw.Draw(img)
    for sh in slide.shapes:
        if sh.left is None: continue
        x,y = emu(sh.left), emu(sh.top); w,h = emu(sh.width), emu(sh.height)
        # fill
        try:
            fill = sh.fill
            if fill.type is not None and fill.type == 1:
                c = fill.fore_color.rgb
                d.rectangle([x,y,x+w,y+h], fill=(c[0],c[1],c[2]))
        except Exception: pass
        try:
            ln = sh.line
            if ln.width and ln.fill.type == 1:
                c = ln.color.rgb
                d.rectangle([x,y,x+w,y+h], outline=(c[0],c[1],c[2]), width=max(1,emu(ln.width)))
        except Exception: pass
        if not sh.has_text_frame: continue
        tf = sh.text_frame
        if not "".join(r.text for p in tf.paragraphs for r in p.runs).strip(): continue
        # layout paragraphs
        pad = emu(tf.margin_left)
        avail = w - emu(tf.margin_left) - emu(tf.margin_right)
        cy = y + emu(tf.margin_top)
        blocks=[]
        for p in tf.paragraphs:
            runs=[r for r in p.runs if r.text]
            if not runs:
                blocks.append(([],0,1.15,0,PP_ALIGN.LEFT)); continue
            sz = max((r.font.size.pt if r.font.size else 14) for r in runs)
            ls = p.line_spacing or 1.15
            al = p.alignment or PP_ALIGN.LEFT
            blocks.append((runs, sz, ls, (p.space_after.pt if p.space_after else 0), al))
        # measure total
        def wrap(runs, sz):
            # simple: treat paragraph as single style (max size/bold)
            txt="".join(r.text for r in runs)
            bold=any(r.font.bold for r in runs)
            f=font(sz,bold)
            words=txt.split(" "); lines=[]; cur=""
            for wd in words:
                t=(cur+" "+wd).strip()
                if f.getlength(t)*0.94<=avail or not cur: cur=t
                else: lines.append(cur); cur=wd
            if cur: lines.append(cur)
            return lines,bold
        total=0; layout=[]
        for runs,sz,ls,sa,al in blocks:
            if not runs: layout.append(([],sz,ls,0)); total += sz*ls*96/72; continue
            lines,bold=wrap(runs,sz)
            hin = len(lines)*sz*ls*96/72
            hin=len(lines)*sz*1.2*96/72
            layout.append((lines,sz,ls,bold)); total+=hin+sa*96/72
        anchor = tf.vertical_anchor or MSO_ANCHOR.TOP
        if anchor == MSO_ANCHOR.MIDDLE: cy = y + (h-total)//2
        elif anchor == MSO_ANCHOR.BOTTOM: cy = y + h - total - emu(tf.margin_bottom)
        for (runs,sz,ls,sa,al),(lines,_,_,bold) in zip(blocks,layout):
            if not lines: cy += sz*ls*96/72; continue
            col = runs[0].font.color.rgb if runs[0].font.color and runs[0].font.color.type==1 else (255,255,255)
            f=font(sz,bold)
            for line in lines:
                lw_ = f.getlength(line)
                lx = x+pad
                if al==PP_ALIGN.CENTER: lx = x + (w-lw_)//2
                elif al==PP_ALIGN.RIGHT: lx = x+w-pad-lw_
                d.text((lx, cy), line, font=f, fill=(col[0],col[1],col[2]))
                cy += sz*1.2*96/72
            cy += sa*96/72
    img.save(f'preview/s{idx:02d}.png')

# contact sheet 3 cols
files=sorted(glob.glob('preview/s*.png'))
cols,rows=3,math.ceil(len(files)/3)
tw,th=Wpx//2, Hpx//2
sheet=Image.new('RGB',(cols*tw+ (cols+1)*10, rows*th+(rows+1)*10),(30,30,34))
for i,f in enumerate(files):
    im=Image.open(f).resize((tw,th))
    r,c=divmod(i,cols)
    sheet.paste(im,(10+c*(tw+10), 10+r*(th+10)))
sheet.save('preview/contact.png')
print("rendered", len(files))
