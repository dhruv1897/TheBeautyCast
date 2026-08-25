TheBeautyCast — brand kit
=========================

THE LOGO IS: the Signal C + the wordmark.
File: LOGO-MASTER.svg  (dark grounds) / LOGO-MASTER-light.svg (light grounds)

Everything else in this folder is that same logo cut for a specific job. There
is one logo. The monogram and the seal are supporting marks, not alternatives.

Why this one won: it is the only mark that carries the name's meaning — a
source dot broadcasting inside an aperture that also reads as C, for cast and
broadcast. It already matches the masthead badge in your reel system, and it
reduces to a legible 16px favicon, which the seal cannot do.


WHICH FILE FOR WHICH JOB
------------------------

WEBSITE HEADER
  LOGO-MASTER.svg (dark header) or LOGO-MASTER-light.svg (light header)
  Height 32-40px. SVG, so it stays sharp on every screen.

WEBSITE FAVICON / BROWSER TAB
  favicon-16.svg under 24px · favicon.svg above · png/favicon-180.png for the
  phone home-screen icon.

WATERMARK ON REELS AND POSTS
  Dark or busy footage  ->  png/WATERMARK-lockup-cream-1400.png
  Bright footage        ->  png/WATERMARK-lockup-ink-1400.png
  Tight corner          ->  png/WATERMARK-mark-cream-600.png  / -ink-600.png

  Size it to 22-26% of frame width for the lockup, 9-11% for the mark alone.
  Place it bottom-left, 6% in from the left edge and 12% up from the bottom —
  that clears the caption, the like button, and the Reels progress bar.
  Do not change its opacity; the shadow is already baked in and tuned. Use the
  SAME position and size on every post. A watermark that moves reads as an
  afterthought; one that never moves reads as a channel.

INTRO VIDEO
  video/intro-vertical-1080x1920.mp4   Reels, TikTok, Stories
  video/intro-square-1080x1080.mp4     feed posts
  video/intro-landscape-1920x1080.mp4  YouTube, website hero
  video/intro-480.gif                  email signature, web preview

  3.0 seconds, 30fps, no audio — lay your own sound under it. Cut it straight
  onto the front of the reel; the last 5 frames are completely static so the
  cut into your first shot is clean. Add a short whoosh on the arc sweep
  (0.2-1.0s) and a soft low thump on the dot landing (0.0-0.3s) and it will
  feel twice as expensive.

INSTAGRAM PROFILE PICTURE
  png/mark-signal-avatar-1024.png — the mark alone, no wordmark. At 40px in a
  feed the words are unreadable anyway, and the mark is what people learn.

REEL MASTHEAD BADGE
  masthead-badge.svg — sits at y=184, unchanged, on every post.

REEL CLOSING FRAME
  closing-frame.svg / png/closing-frame-1080.png — handle already in place.

EMAIL SIGNATURE, DECKS, PDFs
  LOGO-MASTER-tagline-light.svg on white. In a deck cover use
  LOGO-MASTER-stacked.svg on ink.

MERCHANDISE, STAMPS, ONE-COLOUR PRINT
  LOGO-MASTER-1c-cream.svg / -1c-ink.svg — no accent, no tri-tone, survives
  embroidery, foil, and a fax machine.


COLOUR
------
  Ink         #0C0B0E   ground
  Cream       #FAF7F3   primary type
  Accent      #FF7A45   "Cast", source dot, rule — DARK GROUNDS ONLY
  Accent deep #C2572C   the same hue for light grounds
  Muted       #A8A29B   "The", secondary type on dark
  Muted deep  #6F6A64   the same role on light

The rule worth remembering: #FF7A45 on cream is only 2.4:1 contrast. It looks
fine on a screen at 200px and falls apart in print, in email, and under 40px.
Anything on a light ground uses #C2572C. Every -light file already does.


CLEAR SPACE AND MINIMUMS
------------------------
  Clear space: one source-dot diameter on all four sides. Nothing enters it.
  Minimum width, full lockup: 120px on screen, 30mm in print.
  Below that, drop the wordmark and use the mark alone.
  Never: recolour it, outline it, add a gradient, stretch it, rotate it, or
  put the bright accent on white.


TYPE
----
Inter. 900 for the wordmark, 800/600 in the seal, 500/600 for body copy.
Free from Google Fonts. Every wordmark in this kit is already cut to outlines,
so the files carry no font dependency — but you will want Inter installed for
captions, decks, and the website.


REBUILDING
----------
  src/typeset.py  pulls glyph outlines out of Inter with fontTools
  src/build.py    cuts the whole mark collection
  src/master.py   cuts the master lockup and the watermarks
  src/anim.py     renders the intro video frames and encodes the MP4s
  src/export.py   rasterises the PNGs

Change a colour constant at the top of build.py and re-run all of them to
re-cut every asset in this folder, video included.
