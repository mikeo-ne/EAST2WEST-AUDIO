"""Baranga 12-Week Strategic Marketing Assignment — corrected written report (.docx)."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INK    = RGBColor(0x1A, 0x1A, 0x1F)
GOLD   = RGBColor(0x9A, 0x6B, 0x12)
MUTED  = RGBColor(0x55, 0x55, 0x5E)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
RED     = RGBColor(0x9C, 0x2F, 0x2F)
TEAL    = RGBColor(0x11, 0x6B, 0x62)

doc = Document()

# ---------------------------------------------------------------- page + base styles
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)   # A4
sec.left_margin = sec.right_margin = Inches(0.85)
sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.15

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def cell_margins(table, top=60, bottom=60, left=100, right=100):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for tag, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        el = OxmlElement(f"w:{tag}"); el.set(qn("w:w"), str(val)); el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)

def fixed_layout(table):
    tblPr = table._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)

def no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}"); el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)

def hline(paragraph, size=8, color="D8D8DE"):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "4"); bottom.set(qn("w:color"), color)
    pbdr.append(bottom); pPr.append(pbdr)

def para(text="", size=10.5, bold=False, italic=False, color=INK, space_after=7,
         align=None, space_before=0, spacing=1.15):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = spacing
    if align: p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = color
    return p

def rich(parts, size=10.5, space_after=7, spacing=1.15, space_before=0):
    """parts: list of (text, dict(bold=,italic=,color=))"""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = spacing
    for txt, opt in parts:
        r = p.add_run(txt)
        r.font.size = Pt(opt.get("size", size))
        r.bold = opt.get("bold", False)
        r.italic = opt.get("italic", False)
        r.font.color.rgb = opt.get("color", INK)
    return p

def h1(number, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{number}.  " if number else "")
    r.font.size = Pt(9); r.bold = True; r.font.color.rgb = GOLD
    r2 = p.add_run(text.upper())
    r2.font.size = Pt(13.5); r2.bold = True; r2.font.color.rgb = INK
    hline(p)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.size = Pt(10.5); r.bold = True; r.font.color.rgb = GOLD
    return p

def bullet(text, bold_lead=None, size=10.3):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.left_indent = Inches(0.26)
    if bold_lead:
        r = p.add_run(bold_lead); r.bold = True; r.font.size = Pt(size)
    r2 = p.add_run(text); r2.font.size = Pt(size)
    return p

def table(headers, rows, widths, header_fill="1A1A1F", font=9.2, head_font=8.6,
          zebra="F4F4F6", first_col_bold=True):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell_margins(t)
    no_borders(t)
    fixed_layout(t)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.width = widths[i]
        shade(c, header_fill)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(h.upper())
        r.bold = True; r.font.size = Pt(head_font); r.font.color.rgb = WHITE
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            c = cells[i]
            c.width = widths[i]
            if zebra and ri % 2 == 1:
                shade(c, zebra)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(val)
            r.font.size = Pt(font)
            r.bold = bool(first_col_bold and i == 0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def callout(title, body, fill="FBF6E9", accent=GOLD):
    t = doc.add_table(rows=1, cols=1)
    t.autofit = False
    cell_margins(t, top=120, bottom=120, left=160, right=160)
    no_borders(t)
    c = t.rows[0].cells[0]
    c.width = Inches(6.55)
    shade(c, fill)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(title)
    r.bold = True; r.font.size = Pt(9); r.font.color.rgb = accent
    p2 = c.add_paragraph()
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.12
    r2 = p2.add_run(body); r2.font.size = Pt(10)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def footer_text(text):
    for s in doc.sections:
        f = s.footer.paragraphs[0]
        f.text = ""
        f.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = f.add_run(text)
        r.font.size = Pt(7.8); r.font.color.rgb = MUTED
        r.font.name = "Calibri"

# ================================================================ COVER
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(40)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
r = p.add_run("MUSIC BUSINESS CAPSTONE  ·  7H MUSIC GROUP  ·  KAMPALA")
r.font.size = Pt(8.5); r.bold = True; r.font.color.rgb = GOLD

p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
r = p.add_run("BARANGA")
r.font.size = Pt(46); r.bold = True; r.font.color.rgb = INK

p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(6)
r = p.add_run("Artist Marketing Strategy & 12-Week Strategic Plan")
r.font.size = Pt(16); r.bold = True; r.font.color.rgb = GOLD

p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(18)
r = p.add_run("Revised edition  ·  Corrected artist positioning: Afro-pop / rap")
r.font.size = Pt(10); r.italic = True; r.font.color.rgb = MUTED

meta = doc.add_table(rows=0, cols=2)
meta.autofit = False
no_borders(meta)
fixed_layout(meta)
cell_margins(meta, top=40, bottom=40)
for k, v in [("Artist", "Baranga (7H Music Group)"),
             ("Territory", "Kampala, Uganda → East Africa and the diaspora"),
             ("Timeline", "12 weeks / 3 months, in three phases"),
             ("Prepared by", "7H Music Group — marketing and A&R"),
             ("Document status", "Revision 2 — supersedes the original acoustic-soul draft"),
             ("Companion file", "Baranga-12-Week-Strategic-Marketing-Plan.pptx (18 slides)")]:
    cells = meta.add_row().cells
    cells[0].width = Inches(1.5); cells[1].width = Inches(5.0)
    r = cells[0].paragraphs[0].add_run(k.upper())
    r.font.size = Pt(8); r.bold = True; r.font.color.rgb = GOLD
    cells[0].paragraphs[0].paragraph_format.space_after = Pt(3)
    r2 = cells[1].paragraphs[0].add_run(v)
    r2.font.size = Pt(9.5)
    cells[1].paragraphs[0].paragraph_format.space_after = Pt(3)

doc.add_page_break()

# ================================================================ CORRECTION NOTICE
h1("", "Correction notice")
rich([("The first version of this document described Baranga as a “soulful Afro-fusion singer, "
       "guitarist and songwriter” whose signature was “warm acoustic guitar”. That description is "
       "wrong, and the error was structural rather than cosmetic: it set the positioning, the "
       "competitive set, the content engine, the release schedule and the revenue plan.", {})],
     space_after=8)
rich([("Baranga is an ", {}), ("Afro-pop / rap artist", {"bold": True}),
      (". His catalogue — ", {}),
      ("Badman", {"italic": True}), (" (feat. Stando & Andrinah), ", {}),
      ("SALO", {"italic": True}), (", ", {}), ("Do you?", {"italic": True}), (", ", {}),
      ("Confirm", {"italic": True}), (" with Smokie Cee, ", {}),
      ("Party Riddim", {"italic": True}), (" and the debut album ", {}),
      ("Chapters I Never Wrote", {"italic": True}),
      (" — is built on rap verses and melodic hooks over Afro-pop production, not on acoustic "
       "instrumentalism. His label’s own roster lists him as “Afro-Pop / Rap”, and his 2026 "
       "recognition came through the UG Hip Hop Awards, where he is nominated for Rookie of the "
       "Year (“Badman”) and Album of the Year (", {}),
      ("Chapters I Never Wrote", {"italic": True}), (").", {})], space_after=10)

table(["What the draft said", "Corrected position", "Consequence for the plan"],
      [["“Soulful Afro-fusion singer, guitarist & songwriter”",
        "Afro-pop / rap artist and songwriter: rapped verses, sung hooks",
        "Credibility sits in lyricism, flow and street storytelling — delivery, not instrumentation"],
       ["Sonic signature: “warm acoustic guitar, rich vocal layers, organic percussion”",
        "Street-storytelling rap over Afro-pop production, mixed in-house by Mike 1ne",
        "Content engine becomes verses, freestyles and open-verse challenges instead of acoustic clips"],
       ["“Release the full EP in Week 9”",
        "Debut album Chapters I Never Wrote was released in October 2026",
        "The campaign extends an existing catalogue: focus single, remix, deluxe, live"],
       ["Objective: 150,000 cumulative streams by Week 12",
        "“Badman” alone has passed 290,000 streams and reached the Ugandan Top 100",
        "Target raised to 450,000 incremental streams across the 12-week window"],
       ["Competitor set included Tungi — a collaborator",
        "Peers: Joshua Baraka, Azawi, Fik Fameica, Senté",
        "Collaborators are reach assets; only non-collaborators are treated as rivals"],
       ["Visual anchor: tailored linen and an acoustic guitar strap",
        "Street-luxe earth tones, layered workwear, beaded wristpiece, Kampala backdrops",
        "Shoot list, brand rules and the merch line all rebuilt around the real visual language"]],
      [Inches(1.95), Inches(2.1), Inches(2.5)])

callout("What this means in one line",
        "Baranga tells Kampala’s story in bars and makes it sing. Every tactic in this plan follows "
        "from that sentence, and nothing in it depends on him being a guitarist.")

h1("", "Executive summary")
rich([("“Badman” proved the market exists. Two UG Hip Hop Awards 2026 nominations prove the industry "
       "noticed. The next twelve weeks convert that moment into a repeatable career rather than a "
       "single spike.", {"bold": True})], space_after=8)
para("The strategy has three moves. First, own the street-storytelling lane instead of chasing the "
     "commercial Afro-pop ladder against better-funded incumbents — a new ladder, not a climb. "
     "Second, turn award-season attention into an audience the label owns directly, so that "
     "playlist placement becomes upside rather than the business model. Third, monetise through "
     "merchandise, a filmed headline show and brand conversations while streaming revenue compounds "
     "in the background.")
para("The plan runs in three phases: weeks 1–4 fix the assets and convert nomination attention into "
     "an owned channel; weeks 5–8 release a focus single with an open-verse challenge and a regional "
     "remix; weeks 9–12 ship a deluxe edition, a merch capsule and a ticketed showcase, then audit "
     "and reinvest. Targets: 450,000 incremental streams, 3,000 owned fans, 30 serviced DJs across "
     "four stations, and roughly US$4,950 in gross campaign revenue.")

# ================================================================ 1
h1("1", "The fact base we are planning from")
para("Every target in this document is set against recorded output and verifiable placements. Where "
     "the draft relied on aspiration, this revision relies on the catalogue.")
table(["Asset", "Status", "Why it matters for the plan"],
      [["Chapters I Never Wrote", "Debut album, released 8 October 2026, seven tracks; mixed and "
        "mastered in-house by producer Mike 1ne",
        "The campaign extends an album that already exists, so week 9 is a deluxe drop rather than a "
        "first release"],
       ["“Badman” (feat. Stando & Andrinah)", "290,000+ streams; Ugandan Top 100 entry; major Spotify "
        "playlist placement",
        "The single that sets the streaming baseline and the reference sound for the focus single"],
       ["UG Hip Hop Awards 2026", "Nominated for Rookie of the Year (“Badman”) and Album of the Year "
        "(" + "Chapters I Never Wrote" + ")",
        "A nomination is an attention asset to convert. It is not a win, and the plan never claims one"],
       ["Earlier catalogue", "SALO (2024), Do you? (2025), Confirm with Smokie Cee (2025), "
        "Party Riddim (2025)",
        "Catalogue revival material for weeks 7–8; also proof of release cadence"],
       ["Collaborators", "Smokie Cee, Mr Fallback, Tungi, King Avo, Stando & Andrinah; features on "
        "“Island Kiss” and “Motion” (2026)",
        "Free reach: each partner brings an audience and a share of the promotion cost"],
       ["Label capability", "7H Music Group produces, mixes and masters in-house; four-artist roster",
        "Speed and cost control: remixes, edits and B-sides do not need external studio budget"]],
      [Inches(1.65), Inches(2.4), Inches(2.5)])

# ================================================================ 2
h1("2", "Who is Baranga? Artist profile and end-benefit")
table(["Element", "Position"],
      [["Artist identity", "Afro-pop / rap artist and songwriter from Kampala. Rapped street "
        "narratives with melodic hooks, in Luganda, English and Kampala slang."],
       ["End-benefit — “Seen & Heard”", "Listeners get their own city, hustle and heartbreak narrated "
        "back to them with confidence: proof that a Kampala kid can sound world-class without leaving "
        "the neighbourhood behind."],
       ["Sonic signature", "Punchy Afro-pop drums and warm bass under rap verses; hooks doubled with "
        "sung melody; in-house 7H production by Mike 1ne."],
       ["Lyric territory", "Ambition, loyalty, street survival and young love — named places and "
        "specific detail rather than generic romance."],
       ["Voice", "Direct, unsentimental, locally fluent. Speaks to the listener, not down at them."]],
      [Inches(1.75), Inches(4.8)])
h2("Why the old framing was expensive")
bullet("it positioned him against acoustic and soul acts whose catalogue he has never released with.", bold_lead="Wrong competitive set — ")
bullet("it invited direct comparison with artists built for live acoustic sets, where he has no track record.", bold_lead="Unwinnable comparison — ")
bullet("it buried the actual differentiator: rap lyricism and street-level narrative detail.", bold_lead="Lost differentiation — ")
h2("What the corrected framing unlocks")
bullet("rap and Afro-pop editorial playlists, hip-hop award categories, cypher and freestyle culture.", bold_lead="Access — ")
bullet("verses, open-verse challenges, reaction content, bar breakdowns — formats the audience already makes.", bold_lead="Native content — ")
bullet("features, brand work and live bookings priced on lyrical credibility, not on novelty.", bold_lead="Pricing power — ")

# ================================================================ 3
h1("3", "Audience profile")
table(["Segment", "Who they are", "How they find him", "What they want"],
      [["Core — Kampala hip-hop heads (18–28)",
        "Students, boda riders, campus and streetwear crowds in Kawempe, Bwaise, Ntinda, Kamwokya",
        "TikTok and YouTube first, then Audiomack and Spotify",
        "Bars over polish; someone who sounds like their street"],
       ["Adjacent — Afro-pop listeners (18–32)",
        "Young professionals in Kololo, Bugolobi, Ntinda, plus the diaspora",
        "Hooks and features; playlists and radio drive-time",
        "A catalogue to live with, not just one song"],
       ["Growth — East African region and diaspora",
        "Ugandans in Nairobi, Dar es Salaam, Kigali, Johannesburg and the UK",
        "Remixes, regional features, community pages",
        "A reason to claim him before the mainstream does"]],
      [Inches(1.5), Inches(1.85), Inches(1.55), Inches(1.65)])
para("The through-line across all three: they want authenticity they can verify and access they can "
     "brag about. That makes the owned channel — not the playlist — the centre of the plan.")

# ================================================================ 4
h1("4", "Brand archetypes and visual identity")
table(["Archetype", "Expression"],
      [["Primary — Creator", "Builds from his own experience: writes, records and releases at speed "
        "through in-house production. Speaks in craft, catalogue and process."],
       ["Secondary — Everyman", "The Kawempe kid who made it without leaving the neighbourhood "
        "behind. Speaks in belonging, shared struggle and local pride."]],
      [Inches(1.75), Inches(4.8)])
h2("Visual system")
bullet("asphalt black, gold, dusty tan, faded camo green, terracotta accent.")
bullet("layered workwear over camo, gold chain, and the beaded wristpiece as the one repeatable object.")
bullet("Kampala streets, rooftops, workshops, night-market light — never a blank studio.")
bullet("compressed all-caps headlines that read like a poster pasted on a wall.")
h2("Brand rules")
bullet("no acoustic-guitar imagery anywhere in the campaign; it misrepresents the music.")
bullet("every visual carries one recognisable Kampala location, named in the caption.")
bullet("face-forward and legible at thumbnail size; the name reads at 120 px.")
bullet("lyrics always appear as on-screen text, never only as audio.")
para("Merch logic follows the rules: the beaded wristpiece is the entry-price item, a camp cap and "
     "heavyweight tee carry the type system, and a limited “Chapters” print ties the drop to the "
     "album artwork.", space_before=4)

# ================================================================ 5
h1("5", "Competition and SWOT")
para("Only non-collaborators are treated as competitors. Mr Fallback, Smokie Cee, Tungi and King Avo "
     "are reach assets.")
table(["Competitor", "Strength", "Weakness", "How Baranga wins"],
      [["Joshua Baraka", "Massive regional hits; strong international playlist presence",
        "High-gloss pop production; little street-level narrative",
        "Trench-level detail and rap credibility in a lane he does not occupy"],
       ["Azawi", "Owns commercial radio rotation and corporate sponsorships",
        "Radio-pop formula; weak direct-to-fan ownership",
        "An owned fan channel, plus features-driven virality he cannot block"],
       ["Fik Fameica", "Established rap heavyweight; huge live draw",
        "Brand built on party anthems; limited introspective writing",
        "Lyric-led storytelling and album craft that outlasts a club record"],
       ["Senté", "Critically respected alté / hip-hop crossover; playlist support",
        "Small release volume; niche live footprint",
        "Higher release cadence plus a harder Afro-pop radio hook"]],
      [Inches(1.15), Inches(1.85), Inches(1.75), Inches(1.8)])
h2("Internal SWOT")
table(["", "Factors"],
      [["Strengths", "290,000+ streams on “Badman”; Ugandan Top 100 entry; two UG Hip Hop Awards "
        "nominations; in-house production and mixing; a collaborative roster."],
       ["Weaknesses", "Shallow catalogue depth; awareness concentrated in Kampala; limited live "
        "infrastructure; no owned first-party fan data at the start of the campaign."],
       ["Opportunities", "Award-season attention to convert; remix and feature culture across East "
        "Africa; brand partnerships seeking credible youth voices; a deluxe-format release."],
       ["Threats", "Playlist dependency; being pigeonholed as “just rap” by radio programmers; rival "
        "release volume in the same window; award results that do not go his way."]],
      [Inches(1.35), Inches(5.2)])
h2("Exploitation strategy")
bullet("the owned channel is live in week 3, before any paid media, so attention has somewhere to land.")
bullet("the remix and the regional feature turn collaborators’ audiences into discovery, not competition.")
bullet("the beaded wristpiece gives a single object that appears in every visual and every photo.")
bullet("in-house production means the campaign can answer a weak week with new music in days.")

# ================================================================ 6
h1("6", "Strategy and positioning (Al Ries & Jack Trout)")
h2("Climbing the existing ladder (not recommended)")
para("Competing directly for commercial Afro-pop radio means matching mass-market budgets, chasing "
     "hook gimmicks and accepting a lower rung behind Joshua Baraka, Azawi and Fik Fameica. The cost "
     "is high and the position won is weak.")
h2("Creating a new ladder (recommended)")
callout("New ladder: Kampala Street Storytelling & Afro-Pop Crossover",
        "#1 Baranga — the first voice that sounds like the streets and still fills a radio hook. "
        "Owned space: organic Kampala narrative rap with Afro-pop-scale choruses.",
        fill="F2F7F6", accent=TEAL)
table(["", "Existing ladder (commercial Afro-pop)", "New ladder (street storytelling)"],
      [["Entry cost", "Large media budgets and radio gatekeepers", "Lyricism, consistency, an owned audience"],
       ["#1 position", "Joshua Baraka", "Baranga"],
       ["Baranga’s place", "Third, chasing the market", "First, defining the category"],
       ["Proof points", "Chart position and sponsorship", "Album craft, award nominations, real locations"],
       ["Risk", "Dilution of artistic identity", "Narrow appeal if the storytelling stops being specific"]],
      [Inches(1.35), Inches(2.6), Inches(2.6)])
para("Guard rail: never trade lyric detail for a trend hook. The detail is the moat.")

# ================================================================ 7
h1("7", "Core operational tactics")
table(["Tactic", "Channel", "Detail"],
      [["Open Verse Challenge", "TikTok / Instagram", "Release the focus single instrumental and "
        "invite verses. Prize: a 7H studio day plus a feature slot. Judged on bars, not follower count."],
       ["Freestyle hub", "YouTube", "Two uploads a week — freestyle takes and bar breakdowns — plus "
        "one long-form “how I wrote it” each month. Lyric captions on every video."],
       ["Editorial pitching", "Spotify, Apple Music, Audiomack", "Pitch 30 days ahead. Target rap and "
        "Afro-pop lists explicitly rather than “Afro” catch-alls; Audiomack push for Uganda discovery."],
       ["Radio servicing", "XFM, Capital FM, NRG, KIIS", "Clean edits of “KAMPALA” and the focus "
        "single. In-studio verses and freestyles instead of acoustic reworks."],
       ["Regional remix", "East Africa", "One verse from a Nairobi or Dar es Salaam vocalist; one "
        "video; promotion split by home market. Shared cost, doubled reach."],
       ["Live and merch conversion", "Kampala", "One filmed headline showcase, a merch table and "
        "pre-order at the door. Wristpiece as entry price, tee as the margin item."]],
      [Inches(1.5), Inches(1.5), Inches(3.55)])

# ================================================================ 8
h1("8", "Campaign objectives (S.M.A.R.T.)")
table(["Objective", "Target", "Measured by"],
      [["Streaming reach", "450,000 incremental streams across Spotify, Apple Music and Audiomack "
        "in 12 weeks — on top of the 290,000+ already banked by “Badman”. Roughly US$1,500–1,800 in "
        "campaign royalties.",
        "Weekly DSP pulls, split by track and territory, against a Week 0 baseline"],
       ["Owned fan base", "3,000 members across a WhatsApp channel and Telegram room, with at least "
        "25% monthly active engagement and 1,000 opted-in numbers for drop alerts.",
        "Channel size, open rate, active members, opt-ins"],
       ["Radio and media", "30+ East African DJs serviced, rotation on four stations, two live "
        "in-studio performances, six interview or feature placements.",
        "Station logs, DJ confirmations, published clippings"],
       ["Merch and live", "US$3,450 gross: 150 merch units at UGX 55,000 (about US$15) and 120 "
        "tickets at UGX 38,000 (about US$10).",
        "Sales reconciliation, ticket counts, stock levels"],
       ["Brand equity", "Improved unaided recall among the core segment by Week 12.",
        "Two short fan polls — one at Week 1, one at Week 12"]],
      [Inches(1.3), Inches(2.95), Inches(2.3)])
para("All targets are incremental to a measured Week 0 snapshot, so the album launch is never "
     "double-counted. Exchange rates used throughout: UGX 3,700 = US$1.")

# ================================================================ 9
h1("9", "12-week execution roadmap")
table(["Wk", "Phase / focus", "Key deliverables", "Owner"],
      [["1", "Foundation", "Week 0 dashboard; clean edits ordered; press kit and bios rewritten as "
        "Afro-pop / rap", "7H management"],
       ["2", "Award season", "Seven-day nomination content series; artist call-to-action; ten press "
        "pitches", "Marketing"],
       ["3", "Ownership", "WhatsApp channel and Telegram room launched; unreleased verse as the "
        "sign-up reward", "Marketing"],
       ["4", "Distribution", "Promo pack to 30+ DJs; drive-time bookings; instrumental released for "
        "the challenge", "Radio plugger"],
       ["5", "Release", "Focus single and video released; DSP editorial live; twenty creators seeded",
        "All"],
       ["6", "Participation", "Open Verse Challenge scaled; best entries stitched daily; winner "
        "announced", "Content"],
       ["7", "Expansion", "Regional remix recorded and cleared; partner promotion begins", "A&R"],
       ["8", "Consolidation", "Freestyle series peaks; catalogue revival; remix video shot", "Content"],
       ["9", "Product", "Deluxe edition of Chapters I Never Wrote with two new tracks", "All"],
       ["10", "Revenue", "Merch capsule and one-weekend pop-up in Kamwokya or Ntinda", "Operations"],
       ["11", "Live", "Ticketed headline showcase, 150 capacity, filmed for release", "Live"],
       ["12", "Audit", "Full KPI review; festival and brand pitches; next 12-week brief", "7H management"]],
      [Inches(0.35), Inches(1.15), Inches(3.9), Inches(1.15)], font=8.8)
h2("Phase gates")
para("The focus single is not released until the owned channel passes 1,200 members, four radio spins "
     "are confirmed and the video is delivered. If a gate fails, the release slips one week rather "
     "than the media budget being spent cold.")

# ================================================================ 10
h1("10", "Revenue model")
table(["Line", "Units", "Unit price", "Gross"],
      [["Merch — tees and caps", "110", "UGX 55,000", "US$1,650"],
       ["Merch — beaded wristpieces", "120", "UGX 25,000", "US$600"],
       ["Showcase tickets", "120", "UGX 38,000", "US$1,200"],
       ["Streaming royalties", "450,000 plays", "blended rate", "US$1,500"],
       ["Total", "", "", "US$4,950"]],
      [Inches(2.5), Inches(1.1), Inches(1.2), Inches(1.1)])
para("Assume roughly a 45% margin after production, venue and media. Hold 30% of net for the next "
     "single so the plan does not restart from zero, and treat streaming as the residual rather than "
     "the business model.")

# ================================================================ 11
h1("11", "Risk register and measurement")
table(["Risk", "Likelihood", "Impact", "Mitigation"],
      [["Nomination produces attention but no conversion", "Medium", "Medium",
        "Treat it as content fuel; every post still asks for a listen"],
       ["Focus single underperforms in week one", "Medium", "High",
        "Remix and deluxe are already funded — three separate release moments"],
       ["Rap framing alienates Afro-pop programmers", "Low", "High",
        "Ship a sung-hook edit alongside the rap version and let programmers choose"],
       ["A rival saturates the same playlists", "High", "Medium",
        "Own the owned channel first; playlist placement is upside, not the model"],
       ["Merch does not clear", "Medium", "Medium",
        "Small run, pre-order model, bundle pricing"],
       ["Streaming revenue disappoints", "High", "Low",
        "Revenue leans on merch and live from day one"]],
      [Inches(1.75), Inches(0.8), Inches(0.6), Inches(3.4)])
para("Measurement runs off one dashboard reviewed every Monday: streams, owned fans, radio spins, "
     "challenge entries, revenue and recall. Monthly, a one-page note to management. In week 12, a "
     "written audit that becomes the input to the next cycle.")

# ================================================================ CLOSE
h1("", "Recommendation")
rich([("Approve the corrected positioning, rewrite every public bio, and stop describing him as a "
       "guitarist. Baranga is an Afro-pop / rap artist with a nominated debut album, a 290,000-stream "
       "single and a label that can produce in-house. The strategy that follows from that is "
       "narrower, cheaper and far more defensible than the one that followed from an acoustic-soul "
       "profile.", {})], space_after=8)
callout("The one-line brief",
        "“He tells Kampala’s story in bars, and makes it sing.”")

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
hline(p, color="D8D8DE")
para("Sources: 7H Music Group roster and roster data; 7H Music Blog (press releases, album review and "
     "award coverage, September–November 2026); Apple Music and Spotify catalogue pages for Baranga; "
     "UG Hip Hop Awards 2026 nomination material. All targets are planning figures and must be "
     "re-based on the Week 0 dashboard before execution.",
     size=8, color=MUTED, italic=True)

footer_text("Baranga · 12-Week Strategic Marketing Plan · 7H Music Group · Revision 2")

out = "/home/user/EAST2WEST-AUDIO/deliverables/Baranga-12-Week-Strategic-Marketing-Report.docx"
doc.save(out)
print("saved", out)
