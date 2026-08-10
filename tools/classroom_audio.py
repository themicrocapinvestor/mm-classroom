#!/usr/bin/env python3
"""
Classroom audio: one Ritu-narrated mp3 per chapter, embedded on the page.

Follows the Mark 5 weekly podcast rules exactly, by importing its engine:
  - Ritu, bulbul:v3, pace 1.0, temperature 0.6 (podcast/voice.conf is read)
  - the spoken-English transform (tickers spelled out, money to words, 10-K to
    "ten K", name respellings only in the API string)
  - the disclosure: Ritu says she is synthetic and that the words are Ayush's,
    at the start and end of every chapter
  - per-chunk cache (re-editing a paragraph re-bills only that paragraph),
    1.4s pacing, streaming endpoint, mp3 out

Usage:
  python3 tools/classroom_audio.py --dry            # every chapter: cost plan
  python3 tools/classroom_audio.py --module 1 --dry # one module: cost plan
  python3 tools/classroom_audio.py --module 1       # SPEAK module 1 (the go)
  python3 tools/classroom_audio.py                  # speak everything approved

A chapter speaks only when its front matter carries `audio: true`; the --speak
flow is: generate scripts (printed for review) -> Ayush says go -> run with
--module N. After speaking, run with --stamp N to flip audio:true into those
chapters so the page player appears.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                # mm-classroom/
MARK5 = os.path.expanduser("~/Downloads/Mark 5/scripts")
sys.path.insert(0, MARK5)
import podcast_speak as ps                                  # noqa: E402

AUDIO = os.path.join(ROOT, "assets", "audio")
RS_PER_10K = 30.0

INTRO = ("The Microcap Minute Classroom. Module {mod}, chapter {ch}: {title}. "
         "I am Ritu, a synthetic voice, and the words I am reading are Ayush "
         "Agrawal's.")
OUTRO = ("That was chapter {ch} of module {mod}. The text, the pictures and "
         "the exercise are on the lesson page. Thank you for listening.")

def chapters(module=None):
    out = []
    for fn in sorted(os.listdir(ROOT)):
        m = re.match(r"m(\d\d)-c(\d\d)\.md$", fn)
        if not m:
            continue
        if module and int(m.group(1)) != module:
            continue
        out.append((int(m.group(1)), int(m.group(2)), fn))
    return out

def title_of(text):
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else "Untitled"

def chapter_script(text, mod, ch):
    """Chapter markdown -> the spoken script (a document of its own)."""
    text = re.sub(r"^---.*?---\s*", "", text, flags=re.S)      # front matter
    text = re.sub(r"<div class=\"crumb\".*?</div>", " ", text, flags=re.S)
    text = re.sub(r"<div class=\"pager\".*?</div>", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)          # screenshots
    text = re.sub(r"\*\*Read one real thing\*\*.*$", " ", text, flags=re.S)
    body = " ".join(text.split())
    title = title_of(body)
    return (INTRO.format(mod=mod, ch=ch, title=title) + "\n\n" + body
            + "\n\n" + OUTRO.format(mod=mod, ch=ch))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=int)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--stamp", type=int, help="flip audio:true into a module's chapters")
    a = ap.parse_args()
    conf = ps.voice_conf()
    key = os.environ.get("SARVAM_API_KEY", "").strip()
    if not key and not a.dry:
        sys.exit("SARVAM_API_KEY not set; source credentials.local.env")

    if a.stamp:
        n = 0
        for mod, ch, fn in chapters(a.stamp):
            p = os.path.join(ROOT, fn)
            t = open(p).read()
            if "audio:" not in t.split("---")[1]:
                t = t.replace("permalink:", "audio: true\npermalink:", 1)
                open(p, "w").write(t)
                n += 1
        print(f"stamped audio:true into {n} chapters of module {a.stamp}")
        return

    todo = chapters(a.module)
    total_chars = 0
    for mod, ch, fn in todo:
        raw = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        script = chapter_script(raw, mod, ch)
        spoken = ps.to_speech(script, ps._tickers())
        cs = ps.chunks(spoken)
        chars = sum(len(c) for c in cs)
        total_chars += chars
        print(f"m{mod:02d}-c{ch:02d}  {len(cs)} chunks  {chars:,} chars  "
              f"~Rs {chars/10000*RS_PER_10K:.2f}  {fn}")
        if not a.dry:
            stem = os.path.join(AUDIO, f"m{mod:02d}", f"c{ch:02d}")
            os.makedirs(os.path.dirname(stem), exist_ok=True)
            open(stem + ".txt", "w").write(script)   # the transcript
            parts = []
            for i, t in enumerate(cs, 1):
                audio, cached = ps.speak(t, key, conf.get("model", "bulbul:v3"),
                                         conf.get("speaker", "ritu"),
                                         float(conf.get("pace", 1.0)),
                                         float(conf.get("temperature", 0.6)))
                parts.append(audio)
                print(f"    chunk {i}/{len(cs)} {'cached' if cached else 'spoken'}")
                if not cached:
                    ps.time.sleep(ps.PACE_S)
            ps.join_mp3(parts, stem + ".mp3")
            mb = os.path.getsize(stem + ".mp3") / 1e6
            print(f"    -> {stem}.mp3  {mb:.1f} MB")
    print(f"\nTOTAL {total_chars:,} chars, about Rs {total_chars/10000*RS_PER_10K:.2f}"
          + ("  (dry run, nothing spent)" if a.dry else ""))

if __name__ == "__main__":
    main()
