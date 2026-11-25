# Scoring rubric — 100 points

Five categories. Each check is `assessed` or `not assessed`; only assessed checks count toward the denominator.

| Category | Points | Needs |
|---|---|---|
| Engagement performance | 35 | Tier C |
| Posting consistency | 25 | Tier B |
| Profile optimization | 20 | Tier A |
| Account growth | 15 | Tier C |
| Content format mix | 5 | Tier B |

---

## Profile optimization — 20 points

| Check | Pts | Rule |
|---|---|---|
| P1 Bio exists | 3 | Bio is not empty |
| P2 Bio explains the business | 5 | A stranger could tell what they sell and to whom. Score 0–5, award that many points |
| P3 Link in bio | 4 | A working link is present. 4 if it goes somewhere useful (booking, menu, shop); 2 if it's just a homepage |
| P4 Clear call to action | 4 | The bio tells the reader to do something specific. Score 0–5, award `round(score × 0.8)` |
| P5 Profile photo | 2 | A photo is set and is recognizable at small size |
| P6 Name field is searchable | 2 | 2 if the display name adds searchable words beyond the handle (e.g. "Luna — Pizza, Brooklyn"); 1 if it just repeats the handle; 0 if empty |

On P2 and P4, quote the exact words you are judging. These are the two checks people argue with, and quoting makes the argument productive.

---

## Posting consistency — 25 points

From the post dates. Compute:

```
posts_30d      = posts in the last 30 days
posts_per_week = posts_30d / 30 × 7
days_since_last = today − most recent post date
gaps           = days between each consecutive pair of posts
```

Use real dates. Never judge from "the last 12 posts" without looking at *when* they were — twelve posts from 2023 is not an active account.

### C1 Frequency — 14 pts

| posts_per_week | Pts |
|---|---|
| 4 or more | 14 |
| 3 – 3.9 | 12 |
| 2 – 2.9 | 9 |
| 1 – 1.9 | 6 |
| some, under 1 | 2 |
| none | 0 |

### C2 Recency — 6 pts

| Last post | Pts |
|---|---|
| 0–3 days ago | 6 |
| 4–7 days | 5 |
| 8–14 days | 2 |
| 15+ days | 0 |

### C3 Rhythm — 5 pts

Judge how evenly the posts are spaced, independent of how often. An account posting every Tuesday scores full marks; one posting six times in a week then going quiet for a month does not.

| Spacing | Pts |
|---|---|
| Gaps are all roughly similar | 5 |
| Mostly regular, one or two outliers | 4 |
| Visibly uneven | 2 |
| Bursts and long silences | 0 |

Then: if the longest gap is more than three times the typical gap, subtract 2 (floor 0). Needs at least 4 posts to assess.

---

## Engagement performance — 35 points

Read these from the Insights Overview screenshot. If a figure isn't on the screenshot, that check is not assessed.

### E1 Interaction rate — 14 pts

```
interaction_rate = total interactions ÷ accounts reached × 100
```

| Rate | Pts |
|---|---|
| 10% or more | 14 |
| 6 – 9.9% | 12 |
| 3 – 5.9% | 9 |
| 1 – 2.9% | 5 |
| under 1% | 2 |

This uses accounts *reached*, not followers. Do not mix the two denominators, and do not compare a rate computed one way against a benchmark computed the other.

### E2 Trend — 11 pts

Instagram prints the change against the previous 30 days directly on the Insights screen. Read the interactions change.

| Change vs previous 30 days | Pts |
|---|---|
| +15% or better | 11 |
| +5 to +15% | 9 |
| −5 to +5% | 7 |
| −15 to −5% | 4 |
| worse than −15% | 1 |

If the comparison line isn't visible in the screenshot, not assessed — do not derive a trend from a single period.

### E3 Interaction quality — 6 pts

From the interactions breakdown (likes, comments, saves, shares):

```
quality = (saves + shares) ÷ total interactions
```

| quality | Pts |
|---|---|
| 0.15 or more | 6 |
| 0.08 – 0.149 | 4 |
| 0.03 – 0.079 | 2 |
| under 0.03 | 0 |

Saves and shares mean the content was useful enough to keep or pass on. Likes mean very little. A profile with high likes and near-zero saves is making content people enjoy and forget.

### E4 Spread across posts — 4 pts

From the top-posts panel: compare the best post's reach to the typical post's reach.

| Best post vs typical | Pts |
|---|---|
| under 3× | 4 |
| 3 – 5× | 3 |
| 5 – 10× | 2 |
| over 10× | 0 |

A low score here is not bad news on its own — it means one post found an audience the rest didn't. Say which post, and what was different about it.

---

## Account growth — 15 points

From the Followers screen.

### G1 Follower growth — 8 pts

```
growth = (followers now − followers 30 days ago) ÷ followers 30 days ago × 100
```

| 30-day growth | Pts |
|---|---|
| 5% or more | 8 |
| 2 – 4.9% | 7 |
| 0.5 – 1.9% | 5 |
| 0 – 0.4% | 3 |
| −2 to 0% | 1 |
| worse than −2% | 0 |

Flat growth that you measured is a 3. Growth you could not measure is not assessed. Keep these apart.

### G2 Reach trend — 4 pts

The reach change against the previous 30 days, from the Overview screen.

| Change | Pts |
|---|---|
| +10% or better | 4 |
| 0 to +10% | 3 |
| −10 to 0% | 2 |
| worse than −10% | 0 |

### G3 Follows from reach — 3 pts

```
conversion = follows ÷ accounts reached × 100
```

| conversion | Pts |
|---|---|
| 0.5% or more | 3 |
| 0.2 – 0.49% | 2 |
| 0.05 – 0.19% | 1 |
| under 0.05% | 0 |

Accounts under 100 followers don't get follower data from Instagram at all. Mark G1 and G3 not assessed and say why.

---

## Content format mix — 5 points

From the post formats. Classify each as reel, carousel, or single image.

| Mix | Pts |
|---|---|
| 3 formats, none over 80% of posts | 5 |
| 3 formats, one over 80% | 4 |
| 2 formats | 3 |
| 1 format only | 1 |

This measures format variety, which affects how Instagram distributes content. It deliberately does **not** judge subject matter. Do not dock points because a business skipped a content category you thought of — a bakery that only posts product and behind-the-scenes is not doing it wrong.

---

## Reasons a check can be not assessed

Use these words so the report is consistent:

- **No Insights data** — the person didn't send that screenshot, or the figure was illegible
- **Not enough posts** — fewer than 4 posts to judge rhythm
- **No comparison period** — the previous-period change wasn't visible
- **Under 100 followers** — Instagram withholds follower data below this
- **Personal account** — no Insights available until they switch to a professional account
