# The Microcap Minute Classroom - Style Guide (binding for every chapter)

## Who you are writing for
A curious 12-13 year old in India who has never bought a US stock. They are smart,
they read English well, and they have zero patience for being talked down to.
Explain every concept like you would to them: short sentences, everyday words,
and an analogy from normal life (school, cricket, a kirana store, a tiffin,
pocket money) before any jargon. When a technical word must appear, define it in
the same sentence. Example register: "A balance sheet is a photo of everything a
company owns and owes, taken on one particular day."

The subject matter is US-listed companies and SEC filings. The reader's context
is Indian: where a rupee figure helps intuition, give it in brackets next to the
dollar figure (rough conversion is fine, say "about"). Examples must be US
companies (Apple is our running example), never Indian ones, except when
explicitly comparing systems (e.g. "in India you know promoter disclosures; in
America the closest thing is...").

## Hard rules
- NO em-dashes or en-dashes anywhere. Use commas, colons, or full stops.
- Never name or reference any data vendor other than StockAnalysis.com
  (?ref=MICROCAPMINUTE referral links), StockCharts.com, SEC.gov/EDGAR, and our
  own pages (themicrocapminute.in, themicrocapinvestor.github.io/smart-investor-tracker/*).
- Never give a buy/sell opinion on any company. Teach the method, always.
- Every module ends with this exact disclosure line:
  "*StockAnalysis.com links in this module carry The Microcap Minute's referral
  code. Nothing in this module is investment advice or a recommendation.*"
- Honesty beats excitement: if a technique often fails, say so plainly.

## Chapter structure (fixed)
Every chapter is a markdown file, 600-900 words, with this front matter:

```
---
layout: default
title: <chapter title>
module: <module number, e.g. 3>
chapter: <chapter number within module>
permalink: /m01/c03/
---
```

Then, in order:
1. `<div class="crumb"><a href="/mm-classroom/">Classroom</a> / <a href="/mm-classroom/m01/">Module N: name</a> / Chapter M</div>`
   (adjust module number and name)
2. H1: the chapter title.
3. A `div.learn` block: "**What you will learn**" with 3-5 bullets.
4. The body: concept in plain words, then a worked example on a real company
   (default: Apple; vary with Microsoft, Nvidia, Coca-Cola, Tesla where the
   point needs variety), using screenshots from the manifest.
5. A `div.try` block: "**Try it yourself**" - one concrete 10-minute exercise
   the reader can do free online (usually on SEC.gov or StockAnalysis).
6. A `div.takeaways` block: "**Key takeaways**" - 3-5 bullets.
7. "**Read one real thing**": one link to a real filing or page, with one line
   on what to notice in it.
8. A `div.pager` with prev/next chapter links (within the module; last chapter
   links next to the module index).

## Screenshots
Use ONLY filenames from assets/shots/MANIFEST.md (they are being captured
exactly to that list). Embed with:
`![one-line alt description]({{ "/assets/shots/FILENAME" | relative_url }})`
and follow the image with one sentence telling the reader what to notice.
2-4 screenshots per chapter. If the manifest lacks a shot you want, pick the
closest one; do not invent filenames.

## Module index page
Each module also has one index file `m01.md` (etc.) with front matter
(layout: default, title: Module N - name, permalink: /m01/) containing: the
module crumb, H1, a 2-3 sentence module intro, and an ordered list of its
chapters with one-line descriptions and links.

## What good looks like
Read any page of zerodha.com/varsity for tone, then make it shorter, warmer,
and aimed a few years younger. Varsity for the US filings world, written by
someone who respects a kid's intelligence.
