---
name: igaudit
description: Audit an Instagram business or creator profile and score it out of 100 across profile, posting consistency, engagement, growth and content mix, with evidence-backed findings and prioritized fixes. Use when someone asks to audit, review, grade or score their Instagram, asks what's wrong with their Instagram, or asks why their Instagram isn't growing.
---

# Instagram audit

Score an Instagram business or creator profile out of 100 across five categories, then give the person the five fixes that will move the needle most.

Read `references/scoring-rubric.md` for the point tables before scoring. Read `references/report-template.md` for the output format before writing the report.

**If Composio's Instagram tools are available, use live data.** Read `references/composio-source.md` and pull the account's data through the API. That replaces screenshots for Tiers B and C. Fall back to screenshots when no connection exists or a call fails.

## Four rules that make this audit trustworthy

**1. Never invent a metric.** If the person has not given you a number, that check is *not assessed* and its points leave the denominator. Do not estimate reach, infer engagement from follower count, guess at follower growth, or fill a gap with a typical value for their industry.

**2. Every point must trace to evidence.** When you award or withhold points, you must be able to name what you saw — a post date, a bio line, a figure from a screenshot. If you cannot, the check is not assessed.

**3. Always report coverage with the score.** Write "72 out of a possible 85 points assessed — 85% coverage", never a bare number. Below 60% coverage, do not give an overall score at all: give the category scores you do have and say plainly what is missing.

**4. Do not scrape Instagram.** Ask the person for what you need. If you have web browsing and they give you a public handle, you may look at their public profile page — but treat anything you cannot verify from it as not assessed.

## Step 1 — Collect what you can

With a live Composio connection, run the calls in `references/composio-source.md` and skip to Step 2. Ask the person to paste their bio and link in bio: Composio's user-info action returns the handle, name, photo and counts, but not the bio or website.


Show the person this table, then work with whatever they give you. Do not refuse to start because they only have Tier A.

| Tier | What to send | Time | Unlocks |
|---|---|---|---|
| **A** | Handle, bio text, link in bio, display name, and whether there's a profile photo | 1 min | Profile — 20 pts |
| **B** | Date and format (photo / carousel / reel) of their last 12 posts | 3 min | Consistency + content mix — 30 pts |
| **C** | Screenshots of Instagram Insights: the 30-day **Overview** and the **Followers** screen | 3 min | Engagement + growth — 50 pts |

For Tier C, tell them exactly where to tap: **Instagram app → their profile → Professional dashboard → Insights → set the range to "Last 30 days"**, then screenshot that screen and the Followers screen. Ask them to make sure the comparison line (the "vs previous 30 days" percentages) is visible, because several checks read it directly.

If they send a screenshot, read the actual numbers off it. If a number is cut off or illegible, say so and mark that check not assessed rather than guessing at it.

## Step 2 — Score each category

Work through `references/scoring-rubric.md` category by category. For each check, record:

- the points earned and the maximum
- `assessed` or `not assessed` (with the reason)
- the evidence — the post dates, the bio phrase, the figure you read

Use the **median**, not the average, wherever the rubric asks for a typical value. One viral reel will otherwise make a dormant account look healthy.

Two checks need your judgment rather than arithmetic — whether the bio explains the business, and whether there is a real call to action. Judge these against the business the person actually runs: "Book your next haircut" is a strong call to action for a salon and a weak one for a clothing shop. Quote the words you are judging so they can disagree with you.

## Step 3 — Calculate the score

```
earned    = sum of points earned on assessed checks
possible  = sum of maximum points on assessed checks
coverage  = possible / 100
score     = round(earned / possible × 100)      only if coverage >= 0.60
```

Never score a check zero because data was missing. Zero means you measured it and it was bad. Missing means you could not measure it. Collapsing those two is the fastest way to tell someone running a healthy account that they are failing.

## Step 4 — Write the report

Follow `references/report-template.md`. The shape is: score and coverage, the category table, three things working, five prioritized fixes, then what could not be assessed and why.

Make every fix specific to what you saw. "Post more consistently" is useless. "You posted 9 times in the first three weeks of October and nothing since Oct 24 — your reach drop tracks that gap exactly" is a fix someone can act on.

Order the five fixes by points available × ease, not by category order. Say how many points each one is worth so the person can see why it is ranked where it is.

## Scope

This skill audits organic content on a business or creator profile. It does not cover ads or paid reach, Stories analytics beyond what the Insights overview shows, competitor comparison, or personal accounts (which have no Insights at all — tell the person they need to switch to a professional account, which is free, before Tier C is possible).
