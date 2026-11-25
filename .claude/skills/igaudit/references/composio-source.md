# Live data through Composio

Use this path when Composio's Instagram tools are available in the session and the person's Instagram Business or Creator account is connected. Live API data is the source of truth. It replaces Tier B and Tier C screenshots and removes reading errors.

## Check the connection first

Search Composio for the Instagram toolkit. If it reports no active connection, offer the connect link and continue with screenshots while the person decides. Personal accounts cannot connect; tell them to switch to a professional account.

## Calls, in order

| Step | Action | Calls | Feeds |
|---|---|---|---|
| 1 | `INSTAGRAM_GET_USER_INFO` with `ig_user_id: "me"` | 1 | Name, photo, follower count. No bio or website: ask for those |
| 2 | `INSTAGRAM_GET_IG_USER_MEDIA` with `ig_user_id: "me"`, `limit: 100`, `since` = 90 days ago | 1 to 4 | Consistency, format mix, likes, comments, saves, shares |
| 3 | `INSTAGRAM_GET_USER_INSIGHTS` with `period: "day"`, last 30 completed days: `reach, views, total_interactions, accounts_engaged, profile_links_taps` | 1 | E1, G2 |
| 4 | Same action, the 30 days before that | 1 | E2, G2 trend |
| 5 | Same action, `follower_count, follows_and_unfollows`, last 30 days | 1 | G1, G3 |
| 6 | `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` with `metric: ["reach"]` for the 25 most recent posts | up to 25 | E4 spread |

About 31 calls. Paginate step 2 on `paging.cursors.after`.

On step 2, request these fields so you skip per-post insight calls for engagement:

```
id,timestamp,media_type,media_product_type,caption,permalink,like_count,comments_count,saved_count,shares_count,view_count
```

## Rules for API data

- **Empty means not assessed.** Meta returns an empty result, not zero, when data is unavailable. `follower_count` and `follows_and_unfollows` come back empty under 100 followers.
- **Skip the last 48 hours** in insight windows. Meta delays metrics by up to two days. Post dates use real time.
- **Score carousels on the parent post.** Meta returns no insights for carousel children.
- **Do not request `impressions` or `plays`.** Meta retired both in April 2025. Use `views`.
- **Stop on rate-limit errors.** Error code 80002 means the account's daily quota is spent. Score what you have and mark the rest not assessed. Do not retry in a loop.
- **Use median ER per post** for E1 when you have per-post reach: `(likes + comments + saves + shares) / reach × 100`. Report which method you used.

## Cite the source

Add one line under the headline: "Source: live Instagram data via Composio" or "Source: screenshots you sent." Scores from the two sources can differ by a few points; say so if the person compares them.
