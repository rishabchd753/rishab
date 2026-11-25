# Audit Your Instagram for Free

A Claude skill that scores your Instagram business profile out of 100 and hands you five fixes, ranked by impact.

**Want a report now?** Run an instant audit at [tryposty.net](https://tryposty.net). TryPosty connects to your account and scores it in about a minute.

## How it scores

| Category | Points | Checks |
|---|---|---|
| Engagement | 35 | Interaction rate on reach, monthly trend, saves and shares, spread across posts |
| Posting consistency | 25 | Frequency, recency, evenness of spacing |
| Profile | 20 | Bio, link, call to action, photo, searchable name |
| Growth | 15 | Follower growth, reach trend, follows per account reached |
| Format mix | 5 | Reels, carousels and images |

The skill scores the data it can see. Skip a step and you get a partial score, reported out of the points it assessed. Missing data never counts as zero.

## Two ways to feed it data

**Live, through Composio.** Connect your Instagram Business or Creator account to [Composio](https://composio.dev) and Claude pulls 90 days of posts and 30 days of Insights straight from Instagram's API. You paste your bio, and the API supplies the rest. Use this path for the most accurate score.

**By hand, with screenshots.** Paste your bio and link, list the dates of your last 12 posts, and send two screenshots from Instagram Insights. Takes about five minutes.

| You send | Unlocks |
|---|---|
| Handle, bio, link in bio, display name | Profile, 20 points |
| Dates and formats of your last 12 posts | Consistency and format mix, 30 points |
| Insights screenshots: 30-day Overview and Followers | Engagement and growth, 50 points |

Find Insights in the Instagram app under your profile, then Professional dashboard, then Insights. Set the range to the last 30 days and keep the "vs previous 30 days" figures in frame.

## Install

**Claude apps.** Download `instagram-audit.zip` from the [latest release](../../releases/latest). In Claude, open Settings, then Capabilities, then Skills, and upload the zip.

**Claude Code.**

```bash
git clone https://github.com/TryPosty/Audit-Your-Instagram-For-Free.git ~/.claude/skills/instagram-audit
```

Then ask Claude: "Audit my Instagram."

## Requirements

You need a Business or Creator account for Insights and for the Composio connection. Switching from a personal account costs nothing in Instagram's settings. Personal accounts still get the profile and consistency scores.

Instagram withholds follower data from accounts under 100 followers, so the skill marks those growth checks as not assessed.

## Privacy

On the screenshot path, your data stays in your Claude conversation. On the Composio path, Composio holds the access token you grant and you can revoke it from your Composio dashboard or Instagram's settings. The skill sends nothing to TryPosty. It never scrapes Instagram.

## Limits

The skill covers organic posts on one profile. It skips ads, paid reach and competitor comparison, and it won't tell you to post daily if you can manage twice a week.

## Files

```
SKILL.md                         entry point Claude loads
references/scoring-rubric.md     point tables for all 17 checks
references/report-template.md    report layout and tone
references/composio-source.md    API calls for the live-data path
```

## Contributing

Spot a check that scores wrong? [Open an issue](../../issues). Pull requests on the rubric are welcome.

Built by [TryPosty](https://tryposty.net). MIT licensed.

Source: https://github.com/TryPosty/Audit-Your-Instagram-For-Free (MIT). Installed as `igaudit`; upstream skill name is `instagram-audit`.
