import sys
sys.path.insert(0, "/home/user/EAST2WEST-AUDIO/deliverables/_build")
from baranga_deck import *   # noqa
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

i = Inches
N = 0

# ============================================================ 1 · TITLE
s = slide()
N += 1
rect(s, 0, 0, i(0.30), H, fill=GOLD)
# faint right-side blocks
rect(s, i(9.6), 0, i(3.73), H, fill=COAL)
rect(s, i(9.6), 0, Pt(1.2), H, fill=LINE)
for k, (yy, hh, cc) in enumerate([(i(0.0), i(2.5), TERRA), (i(2.5), i(2.5), GOLD),
                                  (i(5.0), i(2.5), TEAL)]):
    rect(s, i(10.15), yy, i(0.55), hh, fill=cc)

text(s, i(1.0), i(0.75), i(8.0), i(0.3), "7H Music Group  ·  Music Business Capstone",
     size=11, color=GOLD, bold=True, caps=True)
text(s, i(1.0), i(1.45), i(8.4), i(2.6),
     [[("BARANGA", {"size": 78, "bold": True, "color": WHITE, "font": HEAD})],
      [("12-Week Strategic Marketing Plan", {"size": 27, "color": GOLD, "bold": True, "font": HEAD})]],
     leading=0.95, space_after=6)
rect(s, i(1.0), i(3.95), i(1.1), Pt(3), fill=TEAL)
text(s, i(1.0), i(4.35), i(8.1), i(1.3),
     "Afro-pop / rap artist. Kampala street storytelling, melodic hooks, "
     "award-nominated debut album. This is the corrected strategy — rebuilt "
     "on the artist's actual recorded work, not an acoustic-guitar profile.",
     size=14.5, color=MUTED, leading=1.35)

for k, (label, val) in enumerate([("Territory", "Kampala → East Africa"),
                                  ("Timeline", "12 weeks / 3 phases"),
                                  ("Artist", "7H Music Group roster"),
                                  ("Status", "Revised edition")]):
    x = i(1.0) + i(k * 2.12)
    text(s, x, i(5.85), i(1.95), i(0.25), label, size=9, color=GOLD, bold=True, caps=True)
    text(s, x, i(6.13), i(1.95), i(0.45), val, size=12, color=WHITE, bold=True)

# ============================================================ 2 · CORRECTIONS
s = slide(); N += 1
eyebrow(s, "Correction notice · what changed and why")
headline(s, [[("The brief called him a guitarist.", {"color": WHITE})],
             [("The catalogue says otherwise.", {"color": GOLD})]], size=31)
text(s, i(0.85), i(2.28), i(11.4), i(0.5),
     "Baranga is an Afro-pop / rap artist. His recorded work, his label's own roster page and his "
     "award nominations all point the same way — so the strategy had to move with them.",
     size=12.5, color=MUTED, leading=1.3)

rows = [["Original document said", "Corrected position", "Strategic consequence"],
        ["“Soulful Afro-fusion singer, guitarist & songwriter”",
         "Afro-pop / rap artist and songwriter; rapped verses, melodic hooks",
         "Credibility now sits in lyricism, flow and street storytelling — not instrumental performance"],
        ["Sonic signature: “warm acoustic guitar, organic percussion”",
         "Street-storytelling rap over Afro-pop production, in-house by Mike 1ne",
         "Content engine shifts to verses, freestyles and open-verse challenges instead of acoustic clips"],
        ["“Release full EP in Week 9”",
         "Debut album Chapters I Never Wrote is already out (Oct 2026)",
         "Plan becomes a campaign extension: focus single, remix, deluxe, live — not a first release"],
        ["Target: 150,000 cumulative streams by Week 12",
         "“Badman” alone has passed 290,000 streams and reached the Ugandan Top 100",
         "Target raised to 450,000 incremental streams across the 12-week window"],
        ["Competitor set included Tungi (a collaborator)",
         "Peer set: Joshua Baraka, Azawi, Fik Fameica, Senté",
         "Collabs are treated as reach assets; only non-collaborators are competitors"],
        ["Visual anchor: linen outerwear + acoustic guitar strap",
         "Street-luxe earth tones, layered workwear, beaded wristpiece, Kampala backdrops",
         "Shoot list and merch line redesigned around the actual visual language"]]
table(s, i(0.85), i(2.92), i(11.63), [2.5, 3.1, 3.9], rows,
      row_h=[i(0.52), i(0.55), i(0.55), i(0.55), i(0.62), i(0.55)],
      size=10.2, head_size=9.2)
footer(s, N)

# ============================================================ 3 · EXEC SUMMARY
s = slide(); N += 1
eyebrow(s, "Executive summary")
headline(s, [[("From one breakout record to a", {"color": WHITE})],
             [("defensible Kampala rap career.", {"color": GOLD})]], size=31)
text(s, i(0.85), i(2.30), i(5.35), i(3.85),
     [[("“Badman” proved the market exists. Two UG Hip Hop Awards 2026 nominations — Rookie of the "
        "Year and Album of the Year — prove the industry noticed. The next twelve weeks convert that "
        "momentum into a repeatable career: a focus single that travels beyond Kampala, a fan base the "
        "label owns directly, and revenue that does not depend entirely on streaming pennies.",
        {"size": 13, "color": WHITE})],
      [("Three moves define the plan: own the street-storytelling lane instead of chasing radio pop; "
        "turn award-season attention into owned audience; and monetise through merch, live and brand "
        "partnerships while streams compound.", {"size": 11.8, "color": MUTED})]],
     leading=1.35, space_after=10)

cx = i(6.55)
stat = [("290K+", "streams on “Badman”", GOLD),
        ("2", "UG Hip Hop Awards 2026 nominations", TEAL),
        ("#1", "Ugandan Top 100 chart entry", TERRA),
        ("12", "weeks, 3 phases, 1 focus single", AMBER)]
for k, (big, lab, col) in enumerate(stat):
    y = i(2.35) + i(k * 1.02)
    rect(s, cx, y, i(5.9), i(0.88), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    rect(s, cx, y, Pt(3.2), i(0.88), fill=col)
    text(s, cx + i(0.28), y, i(1.55), i(0.88), big, size=24, color=col, bold=True,
         font=HEAD, anchor=MSO_ANCHOR.MIDDLE)
    text(s, cx + i(1.85), y, i(3.85), i(0.88), lab, size=11.5, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE, leading=1.15)

text(s, i(0.85), i(6.15), i(11.4), i(0.4),
     "Recommended strategy: build a new ladder — “Kampala Street Storytelling & Afro-Pop Crossover” — "
     "rather than climb the commercial Afro-pop ladder against better-funded incumbents.",
     size=11.5, color=GOLD, bold=True)
footer(s, N)

# ============================================================ 4 · FACT BASE
s = slide(); N += 1
eyebrow(s, "Section 1 · The fact base we are planning from")
headline(s, [[("What the catalogue actually shows", {"color": WHITE})]], size=31)
text(s, i(0.85), i(2.05), i(11.3), i(0.5),
     "Every target in this plan is set against recorded output and verified placements — not aspiration.",
     size=12.5, color=MUTED)

facts = [
    ("Chapters I Never Wrote", "Album · 2026",
     ["Debut full-length, 8 October 2026 — seven tracks",
      "Produced and mixed in-house by Mike 1ne"], GOLD),
    ("“Badman” ft. Stando & Andrinah", "Single · 2025",
     ["290,000+ streams; Ugandan Top 100 entry",
      "Listed work for the Rookie of the Year nomination"], TERRA),
    ("Awards season", "UG Hip Hop Awards 2026",
     ["Album of the Year nominee — the debut album",
      "Rookie of the Year nominee — “Badman”"], TEAL),
    ("Catalogue to draw on", "Streaming",
     ["SALO · Do you? · Confirm · Party Riddim",
      "Chapters I Never Wrote (2026) · features with Smokie Cee and King Avo"], AMBER),
    ("Collaboration network", "Reach assets",
     ["Smokie Cee, Mr Fallback, Tungi, King Avo",
      "“Island Kiss” and “Motion” extend reach through 2026"], GOLD),
    ("Structural advantage", "Operations",
     ["In-house production: speed and cost control",
      "Four-artist roster makes features and remixes cheap"], TEAL),
]
for k, (title_, tag_, items, col) in enumerate(facts):
    cx_ = i(0.85) + i((k % 2) * 5.9)
    cy_ = i(2.36) + i((k // 2) * 1.44)
    card(s, cx_, cy_, i(5.73), i(1.34), title_, items, accent=col, tag=tag_,
         title_size=12.5, body_size=10.6)

footer(s, N)

# ============================================================ 5 · WHO IS BARANGA
s = slide(); N += 1
eyebrow(s, "Section 2 · Artist profile and end-benefit")
headline(s, [[("Who is Baranga?", {"color": WHITE})]], size=31)

rect(s, i(0.85), i(2.15), i(11.63), i(1.05), fill=COAL, line=GOLD, lw=1.0,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
text(s, i(1.15), i(2.15), i(10.85), i(1.05),
     [[("Artist identity   ", {"size": 9.5, "color": GOLD, "bold": True, "caps": True}),
       ("Afro-pop / rap artist and songwriter from Kampala — rapped street narratives, melodic hooks, "
        "Luganda and English.", {"size": 14, "color": WHITE, "bold": True})]],
     anchor=MSO_ANCHOR.MIDDLE, leading=1.25)

card(s, i(0.85), i(3.38), i(3.72), i(1.62), "End-benefit: “Seen & Heard”",
     ["Fans hear their own city, hustle and heartbreak told back to them with confidence."],
     accent=TERRA, tag="The promise")
card(s, i(4.72), i(3.38), i(3.72), i(1.62), "Sonic signature",
     ["Punchy Afro-pop drums under rap verses; sung hooks; in-house 7H production."],
     accent=GOLD, tag="Sound")
card(s, i(8.59), i(3.38), i(3.72), i(1.62), "Lyric territory",
     ["Ambition, loyalty, street survival, young love — named places, not generic romance."],
     accent=TEAL, tag="Content")

rect(s, i(0.85), i(5.18), i(11.63), Pt(0.75), fill=LINE)
text(s, i(0.85), i(5.24), i(5.5), i(0.3), "Why the old framing cost us", size=12, color=TERRA, bold=True)
bullets(s, i(0.85), i(5.56), i(5.35),
        ["“Guitarist” framed him against acoustic acts he has never released with",
         "It invited comparison with artists built for live acoustic sets",
         "It buried the differentiator: rap lyricism and street detail"], size=10.4, gap=6)
text(s, i(6.6), i(5.24), i(5.9), i(0.3), "What the new framing unlocks", size=12, color=TEAL, bold=True)
bullets(s, i(6.6), i(5.56), i(5.8),
        ["Entry into rap and Afro-pop playlists, award categories, freestyle culture",
         "A native content format: verses, open-verse challenges, cyphers",
         "Pricing power for features, brand work and live bookings"],
        dot=TEAL, size=10.4, gap=6)
footer(s, N)

# ============================================================ 6 · OBJECTIVES
s = slide(); N += 1
eyebrow(s, "Section 3 · Campaign objectives, S.M.A.R.T.")
headline(s, [[("Four objectives, benchmarked to the current base", {"color": WHITE})]], size=30)

obj = [("Streaming reach", "450,000", "incremental streams across Spotify, Apple Music and Audiomack "
        "in 12 weeks — on top of the 290K+ already banked by “Badman”. Roughly US$1,500–1,800 in "
        "campaign royalties.", GOLD),
       ("Owned fan base", "3,000", "members in a direct channel (WhatsApp channel + Telegram) with "
        "at least 25% monthly active engagement; 1,000 opted-in phone numbers for drop alerts.", TERRA),
       ("Radio & media", "30 DJs, 4 stations", "rotation secured for the focus single’s clean edit, plus "
        "two live in-studio performances; six interview or feature placements online and on TV.", TEAL),
       ("Merch & live", "US$3,450", "gross: 150 merch units at UGX 55,000 (~US$15) and 120 tickets at "
        "UGX 38,000 (~US$10) for one headline showcase.", AMBER)]
x0 = i(0.85)
for k, (title_, metric, desc, col) in enumerate(obj):
    x = x0 + i(k * 3.0)
    rect(s, x, i(2.05), i(2.78), i(3.15), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, i(2.05), i(2.78), Pt(3.2), fill=col)
    text(s, x + i(0.24), i(2.28), i(2.3), i(0.3), f"0{k+1}", size=10, color=col, bold=True, font=HEAD)
    text(s, x + i(0.24), i(2.58), i(2.35), i(0.3), title_, size=11.5, color=WHITE, bold=True, caps=True)
    text(s, x + i(0.24), i(2.95), i(2.35), i(0.75), metric, size=19, color=col, bold=True,
         font=HEAD, leading=1.0)
    text(s, x + i(0.24), i(3.72), i(2.32), i(1.35), desc, size=10.2, color=MUTED, leading=1.22)

rect(s, i(0.85), i(5.42), i(2.78), i(1.30), fill=COAL2, line=LINE, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
text(s, i(1.05), i(5.56), i(2.4), i(1.02),
     [[("Baseline discipline", {"size": 10.2, "color": GOLD, "bold": True})],
      [("Every target is incremental to a Week 0 snapshot of streams, followers and listeners.",
        {"size": 9.2, "color": MUTED})]],
     leading=1.2, space_after=3)
card(s, i(3.85), i(5.42), i(8.63), i(1.30), "How the objectives ladder up",
     ["Streams fund visibility → visibility fills the owned channel → the owned channel sells merch "
      "and tickets → revenue funds the next release cycle."],
     accent=TEAL, body_size=10.8)
footer(s, N)

# ============================================================ 7 · AUDIENCE
s = slide(); N += 1
eyebrow(s, "Section 4 · Audience profile")
headline(s, [[("Who we are actually talking to", {"color": WHITE})]], size=30)

card(s, i(0.85), i(2.05), i(5.6), i(2.25), "Core: Kampala hip-hop heads (18–28)",
     ["Students, boda riders, campus and streetwear crowds in Kawempe, Bwaise, Ntinda, Kamwokya",
      "Follow rap beefs, cyphers and DJ sets; trust bars over polish",
      "Discover on TikTok and YouTube, then stream on Audiomack and Spotify"],
     accent=GOLD, tag="Primary audience")
card(s, i(0.85), i(4.5), i(5.6), i(2.2), "Adjacent: Afro-pop listeners (18–32)",
     ["Kololo, Bugolobi, Ntinda young professionals and diaspora",
      "Arrive through hooks and features, stay for the catalogue",
      "Playlist-led: Spotify, Apple Music, radio drive-time"],
     accent=TERRA, tag="Secondary audience")
card(s, i(6.88), i(2.05), i(5.6), i(2.25), "Diaspora and East African region",
     ["Ugandans in Nairobi, Dar es Salaam, Kigali, Johannesburg and the UK",
      "High-value streamers and ticket buyers for future touring",
      "Reached through remixes, regional features and community pages"],
     accent=TEAL, tag="Growth audience")
card(s, i(6.88), i(4.5), i(5.6), i(2.2), "What they crave",
     ["Authenticity they can verify — places, slang, real prices",
      "Access: verses before release, private listening",
      "Momentum: backing someone early, before the mainstream"],
     accent=AMBER, tag="Motivation")
footer(s, N)

# ============================================================ 8 · ARCHETYPE
s = slide(); N += 1
eyebrow(s, "Section 5 · Brand archetypes and visual identity")
headline(s, [[("Creator first. Everyman underneath.", {"color": WHITE})]], size=30)

for k, (name, pct, desc, col) in enumerate([
        ("Creator", "Primary",
         "Builds worlds from his own experience: writes, records and releases at speed through in-house "
         "production. Speaks in craft, catalogue and process.", GOLD),
        ("Everyman", "Secondary",
         "The Kawempe kid who made it without leaving the neighbourhood behind. Speaks in belonging, "
         "shared struggle and local pride.", TERRA)]):
    x = i(0.85) + i(k * 5.85)
    rect(s, x, i(2.05), i(5.6), i(1.40), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, i(2.05), Pt(3.2), i(1.40), fill=col)
    text(s, x + i(0.28), i(2.24), i(5.0), i(0.3), name, size=19, color=WHITE, bold=True, font=HEAD)
    chip(s, x + i(1.55), i(2.28), i(1.05), i(0.30), pct, fill=COAL2, fg=col, size=8.5)
    text(s, x + i(0.28), i(2.62), i(5.05), i(0.75), desc, size=11, color=MUTED, leading=1.25)

text(s, i(0.85), i(3.78), i(5.5), i(0.3), "Visual system", size=12.5, color=GOLD, bold=True)
bullets(s, i(0.85), i(4.14), i(5.5),
        ["Palette: asphalt black, gold, dusty tan, faded camo green, terracotta accent",
         "Wardrobe: layered workwear over camo, gold chain, beaded wristpiece as the signature object",
         "Locations: Kampala streets, rooftops, workshops, night-market light — never a blank studio",
         "Type: compressed all-caps headlines that read like a poster pasted on a wall"], size=10.6)

text(s, i(6.88), i(3.78), i(5.5), i(0.3), "Non-negotiable brand rules", size=12.5, color=TEAL, bold=True)
bullets(s, i(6.88), i(4.14), i(5.5),
        ["No acoustic-guitar imagery anywhere in the campaign — it misrepresents the music",
         "Every visual carries one recognisable Kampala location, named in the caption",
         "Face-forward: the artist’s name should be legible at thumbnail size",
         "Lyrics are always on screen as text, never only as audio"], dot=TEAL, size=10.6)

rect(s, i(0.85), i(6.05), i(11.63), i(0.62), fill=COAL2, line=LINE, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
text(s, i(1.1), i(6.05), i(11.2), i(0.62),
     [[("Merch logic:  ", {"size": 10.5, "color": GOLD, "bold": True}),
       ("the beaded wristpiece becomes the entry-price product; camp-cap and heavyweight tee carry the "
        "type system; a limited “Chapters” print run ties the drop to the album artwork.",
        {"size": 10.5, "color": WHITE})]], anchor=MSO_ANCHOR.MIDDLE, leading=1.2)
footer(s, N)

# ============================================================ 9 · COMPETITORS
s = slide(); N += 1
eyebrow(s, "Section 6 · Competition and SWOT")
headline(s, [[("Four rivals, four different weaknesses", {"color": WHITE})]], size=30)
text(s, i(0.85), i(2.02), i(11.4), i(0.4),
     "Only non-collaborators are listed as competitors. Mr Fallback, Smokie Cee, Tungi and King Avo are "
     "reach assets, not rivals.", size=11.5, color=MUTED)

rows = [["Competitor", "Their strength", "Their weakness", "How Baranga wins"],
        ["Joshua Baraka", "Massive regional hits; strong international playlist presence",
         "High-gloss pop production; little street-level narrative",
         "Trench-level detail and rap credibility in a lane he does not occupy"],
        ["Azawi", "Owns commercial radio rotation and corporate sponsorships",
         "Radio-pop formula; weak direct-to-fan ownership",
         "An owned fan channel and features-driven virality he cannot block"],
        ["Fik Fameica", "Established rap heavyweight; huge live draw",
         "Brand built on party anthems; limited introspective writing",
         "Lyric-led storytelling and album craft that ages better than a club record"],
        ["Senté", "Critically respected alté / hip-hop crossover; playlist support",
         "Small release volume; niche live footprint",
         "Higher release cadence plus a harder Afro-pop radio hook"]]
table(s, i(0.85), i(2.52), i(11.63), [1.7, 3.1, 3.1, 3.5], rows,
      row_h=[i(0.52), i(0.56), i(0.52), i(0.52)], size=10.0, head_size=9.0)

# SWOT strip
text(s, i(0.85), i(5.30), i(11.4), i(0.3), "Baranga’s internal SWOT", size=12.5, color=GOLD, bold=True)
sw = [("S", "Strengths", ["290K+ streams and Top 100 entry", "Two award nominations", "In-house production"], TEAL),
      ("W", "Weaknesses", ["Shallow catalogue depth", "Kampala-concentrated awareness", "Thin live infrastructure"], TERRA),
      ("O", "Opportunities", ["Award-season attention", "Remix and feature culture", "Brand partnership budget"], GOLD),
      ("T", "Threats", ["Playlist dependency", "Rap-genre pigeonholing", "Rival release volume"], MUTED)]
for k, (letter, title_, items, col) in enumerate(sw):
    x = i(0.85) + i(k * 2.96)
    rect(s, x, i(5.66), i(2.74), i(1.02), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, x + i(0.2), i(5.72), i(0.4), i(0.3), letter, size=15, color=col, bold=True, font=HEAD)
    text(s, x + i(0.56), i(5.76), i(2.1), i(0.26), title_, size=10, color=WHITE, bold=True, caps=True)
    text(s, x + i(0.2), i(6.06), i(2.4), i(0.6), " · ".join(items), size=8.8, color=MUTED, leading=1.18)
footer(s, N)

# ============================================================ 10 · LADDER
s = slide(); N += 1
eyebrow(s, "Section 7 · Positioning (Al Ries & Jack Trout)")
headline(s, [[("Do not climb their ladder. Build one.", {"color": WHITE})]], size=30)

# left: existing ladder
rect(s, i(0.85), i(2.05), i(5.6), i(4.2), fill=COAL, line=LINE, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
text(s, i(1.15), i(2.25), i(5.0), i(0.3), "Existing ladder · commercial Afro-pop",
     size=10, color=MUTED, bold=True, caps=True)
text(s, i(1.15), i(2.58), i(5.0), i(0.3), "Entry cost: big budgets, radio gatekeepers, gimmick hooks",
     size=9.5, color=TERRA)
lad = [("1", "Joshua Baraka", GOLD, 1.0), ("2", "Azawi", GOLD, 0.86),
       ("3", "Fik Fameica", GOLD, 0.74), ("…", "Baranga — chasing", MUTED, 0.52)]
for k, (rank, name, col, wf) in enumerate(lad):
    y = i(3.05) + i(k * 0.78)
    ww = Emu(int(i(5.0) * wf))
    rect(s, i(1.15), y, ww, i(0.62), fill=COAL2 if k < 3 else INK,
         line=LINE if k < 3 else TERRA, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    text(s, i(1.32), y, i(0.45), i(0.62), rank, size=13, color=col, bold=True,
         font=HEAD, anchor=MSO_ANCHOR.MIDDLE)
    text(s, i(1.82), y, ww - i(0.8), i(0.62), name, size=12, color=WHITE if k < 3 else MUTED,
         bold=(k < 3), anchor=MSO_ANCHOR.MIDDLE)

# right: new ladder
rect(s, i(6.88), i(2.05), i(5.6), i(4.2), fill=COAL, line=GOLD, lw=1.25,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
text(s, i(7.18), i(2.25), i(5.0), i(0.3), "New ladder · Kampala street storytelling",
     size=10, color=GOLD, bold=True, caps=True)
text(s, i(7.18), i(2.58), i(5.0), i(0.3), "Entry cost: lyricism, consistency, owned audience",
     size=9.5, color=TEAL)
rect(s, i(7.18), i(3.05), i(4.7), i(1.05), fill=GOLD,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
text(s, i(7.4), i(3.05), i(4.3), i(1.05),
     [[("#1  BARANGA", {"size": 22, "color": INK, "bold": True, "font": HEAD})],
      [("First voice that sounds like the streets and still fills a radio hook",
        {"size": 10.5, "color": INK})]], anchor=MSO_ANCHOR.MIDDLE, leading=1.15, space_after=2)
bullets(s, i(7.18), i(4.30), i(4.95),
        ["Owned space: organic Kampala narrative rap with Afro-pop-scale choruses",
         "Enemy of the brand: polished, placeless pop that could come from anywhere",
         "Proof points: album craft, award nominations, in-house production, real locations",
         "Guard rail: never trade lyric detail for a trend hook — the detail is the moat"], size=10.4)
footer(s, N)

# ============================================================ 11 · TACTICS
s = slide(); N += 1
eyebrow(s, "Section 8 · Core operational tactics")
headline(s, [[("Six tactics, matched to how rap actually travels", {"color": WHITE})]], size=30)

card(s, i(0.85), i(2.02), i(3.72), i(2.16), "Open Verse Challenge",
     ["Release the single instrumental and invite verses",
      "Prize: a 7H studio day plus a feature slot",
      "Judge on bars, not on follower count"],
     accent=GOLD, tag="TikTok · owned")
card(s, i(4.72), i(2.02), i(3.72), i(2.16), "YouTube freestyle hub",
     ["Two uploads a week: freestyle takes and bar breakdowns",
      "One “how I wrote it” video a month",
      "Lyric captions on every video for the diaspora"],
     accent=TERRA, tag="YouTube · retention")
card(s, i(8.59), i(2.02), i(3.72), i(2.16), "DSP editorial strategy",
     ["Pitch 30 days ahead to Spotify and Apple",
      "Target rap and Afro-pop lists, not “Afro”",
      "Audiomack push for Uganda discovery"],
     accent=TEAL, tag="Streaming")

card(s, i(0.85), i(4.26), i(3.72), i(2.16), "Radio that respects the genre",
     ["Clean edits of “KAMPALA” and the focus single",
      "In-studio verses, never acoustic reworks",
      "XFM, Capital, NRG and KIIS drive-time"],
     accent=AMBER, tag="Radio · TV")
card(s, i(4.72), i(4.26), i(3.72), i(2.16), "Regional remix",
     ["A Nairobi or Dar es Salaam vocalist on the remix",
      "One verse, one video, promotion split by market",
      "Cost shared; reach doubled"],
     accent=GOLD, tag="East Africa")
card(s, i(8.59), i(4.26), i(3.72), i(2.16), "Live & merch conversion",
     ["One headline showcase, filmed for later release",
      "Merch table and pre-order at the door",
      "Wristpiece as entry price, tee as the margin item"],
     accent=TEAL, tag="Revenue")
footer(s, N)

# ============================================================ 12 · ROADMAP OVERVIEW
s = slide(); N += 1
eyebrow(s, "Section 9 · 12-week execution roadmap")
headline(s, [[("Three phases, one continuous story", {"color": WHITE})]], size=30)

phases = [("Weeks 1–4", "Foundation & award season",
           "Fix the record, own the narrative, convert nomination attention into an owned audience.", GOLD),
          ("Weeks 5–8", "Focus single & regional surge",
            "Drop the focus single and remix, own radio and TikTok, and push into East Africa.", TERRA),
          ("Weeks 9–12", "Live, merch & monetisation",
            "Convert attention into cash and into a repeatable live product.", TEAL)]
for k, (wk, name, desc, col) in enumerate(phases):
    x = i(0.85) + i(k * 3.95)
    rect(s, x, i(2.02), i(3.7), i(1.72), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, i(2.02), i(3.7), Pt(3.2), fill=col)
    text(s, x + i(0.22), i(2.18), i(3.2), i(0.26), wk, size=9.5, color=col, bold=True, caps=True)
    text(s, x + i(0.22), i(2.46), i(3.25), i(0.6), name, size=15.5, color=WHITE, bold=True,
         font=HEAD, leading=1.05)
    text(s, x + i(0.22), i(3.12), i(3.28), i(0.58), desc, size=10.5, color=MUTED, leading=1.22)

rows = [["Week", "Focus", "Key deliverables", "Owner"],
        ["1", "Baseline & assets", "Week 0 dashboard; clean edits; press kit rewritten as Afro-pop/rap",
         "7H mgmt"],
        ["2", "Award-season push", "Nomination content series; artist call-to-action; 10 press pitches",
         "Marketing"],
        ["3", "Fan channel launch", "WhatsApp channel + Telegram; unreleased verse as sign-up reward",
         "Marketing"],
        ["4", "Radio & DJ seeding", "Promo pack to 30+ DJs; drive-time bookings; instrumental live",
         "Radio plugger"],
        ["5", "FOCUS SINGLE DROP", "Release single + video; DSP editorial live; creator seeding",
         "All"],
        ["6", "TikTok surge", "Open Verse Challenge scaled; 20 creators briefed; winner announced",
         "Content"],
        ["7", "Regional remix", "Record and clear the East African remix; partner promo begins", "A&R"],
        ["8", "Catalogue revival", "Freestyle series peaks; older singles re-pitched to playlists",
         "Content"],
        ["9", "Deluxe drop", "Deluxe edition of Chapters I Never Wrote plus two new tracks",
         "All"],
        ["10", "Merch drop", "Wristpiece, cap and tee capsule; pop-up in Kampala",
         "Ops"],
        ["11", "Headline showcase", "Ticketed live show, filmed for release; industry guest list",
         "Live"],
        ["12", "Audit & next cycle", "Full KPI review; festival and brand pitches; next 12-week brief",
         "7H mgmt"]]
n = len(rows) - 1
table(s, i(0.85), i(3.96), i(11.63), [0.55, 1.95, 6.9, 1.3], rows,
      row_h=i(0.19), head_h=i(0.28), size=8.8, head_size=8.0, gap_pt=3,
      max_bottom=i(6.72))
footer(s, N)

# ============================================================ 13 · PHASE 1
s = slide(); N += 1
eyebrow(s, "Weeks 1–4 · Foundation and award season")
headline(s, [[("Convert the nomination into an audience we own", {"color": WHITE})]], size=28, w=i(11.4))

card(s, i(0.85), i(2.02), i(3.72), i(2.22), "Week 1 · Reset the assets",
     ["Build the Week 0 baseline: streams, saves, listeners, followers",
      "Rewrite bio and press kit as Afro-pop / rap — drop every acoustic claim",
      "Order clean edits and a radio master of “KAMPALA”"],
     accent=GOLD, tag="Fix the record")
card(s, i(4.72), i(2.02), i(3.72), i(2.22), "Week 2 · Award-season content",
     ["Seven-day content series on both nominations",
      "Artist-voiced ask: vote, then pass it on",
      "Pitch the story to 10 Ugandan outlets"],
     accent=TERRA, tag="Attention")
card(s, i(8.59), i(2.02), i(3.72), i(2.22), "Week 3 · Owned channel",
     ["Launch WhatsApp channel and Telegram room with one clear promise",
      "Sign-up reward: an unreleased verse, channel-first",
      "Target 1,200 members by end of week four"],
     accent=TEAL, tag="Ownership")
card(s, i(0.85), i(4.42), i(3.72), i(2.18), "Week 4 · Radio & DJ seeding",
     ["Clean edit, artwork and a one-line pitch",
      "30+ East African DJs serviced one by one",
      "Five in-studio verse performances booked"],
     accent=AMBER, tag="Distribution")
card(s, i(4.72), i(4.42), i(3.72), i(2.18), "Phase gate: go / no-go",
     ["Release only if: channel ≥ 1,200, four confirmed spins, video delivered",
      "Fail a gate and slip a week rather than spend cold"],
     accent=MUTED, tag="Discipline")
card(s, i(8.59), i(4.42), i(3.72), i(2.18), "Success looks like",
     ["Copy matches the music at last",
      "1,200 owned fans before any paid spend",
      "Radio ready, not radio-hoping"],
     accent=GOLD, tag="Measures")
footer(s, N)

# ============================================================ 14 · PHASE 2
s = slide(); N += 1
eyebrow(s, "Weeks 5–8 · Focus single and regional surge")
headline(s, [[("One record, everywhere at once", {"color": WHITE})]], size=28)

card(s, i(0.85), i(2.02), i(5.6), i(2.2), "Week 5 · Release",
     ["Focus single plus video on a Friday, with the channel told 48 hours early",
      "Editorial pitches already live; Audiomack and Spotify placements confirmed where possible",
      "Twenty creators seeded with the sound and a two-line brief"],
     accent=GOLD, tag="Launch")
card(s, i(6.88), i(2.02), i(5.6), i(2.2), "Week 6 · Open Verse Challenge",
     ["Instrumental released free; challenge duet format on TikTok",
      "Daily stitch of the best entries from the artist’s account",
      "Prize: 7H studio day plus a feature on the remix"],
     accent=TERRA, tag="Participation")
card(s, i(0.85), i(4.42), i(5.6), i(2.0), "Week 7 · Regional remix",
     ["Record the East African remix with a Nairobi or Dar-based vocalist",
      "Split promotion: each team owns its home market for one week",
      "Localise captions and slang per market — no copy-paste copy"],
     accent=TEAL, tag="Expansion")
card(s, i(6.88), i(4.42), i(5.6), i(2.0), "Week 8 · Depth, not noise",
     ["Winner announced; remix video shot",
      "Catalogue revival: older singles re-pitched with new artwork",
      "Two freestyle uploads a week continue without pause"],
     accent=AMBER, tag="Consolidation")

rect(s, i(0.85), i(6.55), i(11.63), i(0.5), fill=COAL2, line=LINE, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
text(s, i(1.1), i(6.55), i(11.2), i(0.5),
     [[("Phase metric:  ", {"size": 10.2, "color": GOLD, "bold": True}),
       ("220,000 incremental streams, 2,500 owned fans, 12 radio spins a week, "
        "1,500 challenge entries across TikTok and Instagram.", {"size": 10.2, "color": WHITE})]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, N)

# ============================================================ 15 · PHASE 3
s = slide(); N += 1
eyebrow(s, "Weeks 9–12 · Live, merch and monetisation")
headline(s, [[("Turn momentum into money and a repeatable show", {"color": WHITE})]], size=28, w=i(11.6))

card(s, i(0.85), i(2.02), i(3.72), i(2.25), "Week 9 · Deluxe drop",
     ["Chapters I Never Wrote (Deluxe): two new tracks plus the remix",
      "One new track is the live-set centrepiece",
      "Existing buyers get a first-listen link"],
     accent=GOLD, tag="Product")
card(s, i(4.72), i(2.02), i(3.72), i(2.25), "Week 10 · Merch capsule",
     ["Beaded wristpiece, camp cap, heavyweight tee, “Chapters” print",
      "One-weekend pop-up in Kamwokya or Ntinda",
      "UGX 55,000 tee · 25,000 wristpiece · 120,000 bundle"],
     accent=TERRA, tag="Revenue")
card(s, i(8.59), i(2.02), i(3.72), i(2.25), "Week 11 · Headline show",
     ["150-capacity venue; 120 tickets at UGX 38,000",
      "Set filmed for a week-12 live release",
      "Industry and brand guests seated, not backstage"],
     accent=TEAL, tag="Live")

# revenue math
text(s, i(0.85), i(4.48), i(5.5), i(0.3), "Week 12 · Revenue reconciliation",
     size=12.5, color=GOLD, bold=True)
rows = [["Line", "Units", "Unit price", "Gross"],
        ["Merch — tees and caps", "110", "UGX 55,000", "US$1,650"],
        ["Merch — wristpieces", "120", "UGX 25,000", "US$600"],
        ["Showcase tickets", "120", "UGX 38,000", "US$1,200"],
        ["Streaming royalties", "450,000 plays", "blended", "US$1,500"]]
table(s, i(0.85), i(4.82), i(5.55), [2.5, 1.2, 1.2, 1.0], rows,
      row_h=i(0.33), head_h=i(0.34), size=9.6, head_size=8.4)

text(s, i(6.88), i(4.48), i(5.5), i(0.3), "Then reinvest", size=12.5, color=TEAL, bold=True)
bullets(s, i(6.88), i(4.82), i(5.5),
        ["Roughly US$4,950 gross before costs — assume 45% margin after production, venue and media",
         "Hold 30% for the next single so the plan does not restart from zero",
         "Pitch festival and brand slots with the filmed live set and the KPI report",
         "Publish the audit internally: what moved, what did not, what changes next cycle"],
        dot=TEAL, size=10.2)
rect(s, i(6.88), i(6.42), i(5.6), i(0.42), fill=COAL2, line=GOLD, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.14)
text(s, i(7.08), i(6.42), i(5.2), i(0.42),
     "Targets are illustrative and must be re-based on the Week 0 dashboard.",
     size=9.2, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
footer(s, N)

# ============================================================ 16 · RISK
s = slide(); N += 1
eyebrow(s, "Section 10 · Risk register")
headline(s, [[("What could break this, and the answer to each", {"color": WHITE})]], size=29)

rows = [["Risk", "Likelihood", "Impact", "Mitigation"],
        ["Award nomination produces attention but no votes or buzz",
         "Medium", "Medium", "Treat the nomination as content fuel, not the plan: every post still asks for a listen"],
        ["Focus single underperforms in week one",
         "Medium", "High", "Remix and deluxe are already funded; the campaign has three separate release moments"],
        ["Rap framing alienates Afro-pop radio programmers",
         "Low", "High", "Ship a sung-hook edit alongside the rap version; let programmers choose"],
        ["Rival release saturates the same playlists",
         "High", "Medium", "Own the owned channel first; playlist placement is upside, not the business model"],
        ["Merch does not clear stock",
         "Medium", "Medium", "Small run, pre-order model, bundle pricing, no cash outlay beyond 150 units"],
        ["Streaming revenue disappoints",
         "High", "Low", "Revenue plan leans on merch and live from day one; royalties are the residual"]]
table(s, i(0.85), i(2.02), i(11.63), [3.6, 1.3, 1.0, 6.0], rows,
      row_h=i(0.56), head_h=i(0.42), size=10.2, head_size=8.8, gap_pt=5,
      max_bottom=i(6.74))
footer(s, N)

# ============================================================ 17 · MEASUREMENT
s = slide(); N += 1
eyebrow(s, "Section 11 · Measurement")
headline(s, [[("One dashboard, reviewed every Monday", {"color": WHITE})]], size=29)

kpi = [("Streams", "450K incremental", "Weekly DSP pulls, split by track and territory", GOLD),
       ("Owned fans", "3,000 members", "Channel size, open rate, 25% active target", TERRA),
       ("Radio", "12 spins / week", "Station logs plus DJ confirmation messages", TEAL),
       ("Engagement", "1,500 entries", "Open Verse submissions, saves and shares", AMBER),
       ("Revenue", "US$4,950 gross", "Merch, tickets and royalty statements", GOLD),
       ("Brand equity", "Unaided recall", "Two quick fan polls at week 1 and week 12", TERRA)]
for k, (name, target, how, col) in enumerate(kpi):
    x = i(0.85) + i((k % 3) * 3.95)
    y = i(2.05) + i((k // 3) * 1.90)
    rect(s, x, y, i(3.7), i(1.55), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, y, Pt(3.2), i(1.55), fill=col)
    text(s, x + i(0.26), y + i(0.20), i(3.2), i(0.26), name, size=9.5, color=col, bold=True, caps=True)
    text(s, x + i(0.26), y + i(0.50), i(3.25), i(0.42), target, size=17, color=WHITE, bold=True, font=HEAD)
    text(s, x + i(0.26), y + i(0.95), i(3.2), i(0.5), how, size=10, color=MUTED, leading=1.2)

rect(s, i(0.85), i(5.95), i(11.63), i(0.66), fill=COAL2, line=LINE, lw=0.75,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
text(s, i(1.1), i(5.95), i(11.2), i(0.66),
     [[("Reporting cadence:  ", {"size": 10.2, "color": GOLD, "bold": True}),
       ("Monday 30-minute review with 7H management; monthly one-page board note; week 12 written "
        "audit that becomes the input to the next cycle.", {"size": 10.2, "color": WHITE})]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, N)

# ============================================================ 18 · CLOSE
s = slide(); N += 1
rect(s, 0, 0, i(0.30), H, fill=GOLD)
eyebrow(s, "Close · recommendation")
headline(s, [[("Stop describing him as a guitarist.", {"color": WHITE})],
             [("Start selling the writing.", {"color": GOLD})]], size=33)
text(s, i(0.85), i(3.05), i(6.6), i(1.6),
     "Baranga is an Afro-pop / rap artist with a nominated debut album, a 290,000-stream single and a "
     "label that can produce in-house. The strategy that follows from that is narrower, cheaper and far "
     "more defensible than the one that follows from an acoustic-soul profile.",
     size=13, color=MUTED, leading=1.4)

steps = [("Now", "Approve the corrected positioning and rewrite all public bios"),
         ("Weeks 1–2", "Baseline dashboard, asset reset, award-season content live"),
         ("Weeks 3–4", "Owned channel to 1,200 fans; radio and DJ pack out"),
         ("Week 5", "Focus single release — no earlier, no later")]
for k, (when, what) in enumerate(steps):
    y = i(2.05) + i(k * 1.02)
    rect(s, i(7.95), y, i(4.53), i(0.88), fill=COAL, line=LINE, lw=0.75,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    text(s, i(8.15), y + i(0.14), i(1.4), i(0.28), when, size=9.5, color=GOLD, bold=True, caps=True)
    text(s, i(8.15), y + i(0.40), i(4.15), i(0.4), what, size=10.5, color=WHITE, leading=1.15)

rect(s, i(0.85), i(5.6), i(6.6), i(1.05), fill=COAL, line=GOLD, lw=1.0,
     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
text(s, i(1.1), i(5.6), i(6.1), i(1.05),
     [[("The one-line brief  ", {"size": 9.5, "color": GOLD, "bold": True, "caps": True})],
      [("“He tells Kampala’s story in bars, and makes it sing.”",
        {"size": 14.5, "color": WHITE, "bold": True})]],
     anchor=MSO_ANCHOR.MIDDLE, leading=1.25, space_after=2)

text(s, i(0.85), i(6.9), i(9), i(0.3),
     "Sources: 7H Music Group roster data, 7H Music Blog (Oct–Nov 2026), Apple Music and Spotify "
     "catalogue, UG Hip Hop Awards 2026 nomination material.", size=8, color=MUTED)
text(s, i(11.4), i(6.9), i(1.1), i(0.3), f"{N:02d}", size=8.5, color=GOLD, bold=True,
     align=PP_ALIGN.RIGHT, font=HEAD)

out = "/home/user/EAST2WEST-AUDIO/deliverables/Baranga-12-Week-Strategic-Marketing-Plan.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
