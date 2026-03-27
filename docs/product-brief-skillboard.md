---
title: "Product Brief: SkillBoard"
status: "complete"
created: "2026-03-27"
updated: "2026-03-27"
inputs:
  - skill-board-product-concept.md
---

# Product Brief: SkillBoard

## Executive Summary

SkillBoard is a web app that aggregates a user's achievements from various platforms (Chess.com, GitHub, and others) into a unified social profile with a numeric score, percentiles, leagues, and the ability to compare yourself with friends.

People spend thousands of hours developing skills, but those achievements remain scattered across dozens of services. Nobody sees the full picture. SkillBoard provides a single place where your skills become visible, comparable, and motivating — through friendly competition and visual progress tracking.

Currently, no product combines achievements from fundamentally different domains (chess, coding, fitness) into one profile. Partial analogs exist only within a single domain (MetaGamerScore for gaming, CodersRank for developers). SkillBoard occupies an empty niche at the intersection of gamification, social networking, and achievement tracking.

## Problem

A typical user plays chess on Chess.com, writes code on GitHub, solves problems on LeetCode — and each platform only knows its own fragment of their profile. There's no single place where you can:

- **See a holistic picture of your skills** — is a 1500 chess rating good? What about 200 stars on GitHub?
- **Compare yourself with friends** — who's stronger "overall"? Someone's better at chess but weaker at coding — and vice versa.
- **Track progress** — am I growing or stagnating? In which areas?

Today people solve this manually: screenshotting ratings, discussing in chats, comparing by eye. It's inconvenient and not motivating.

## Solution

A web app (Python + HTMX) where the user adds their usernames from various platforms to their profile, and the system:

1. **Collects data** — ratings, statistics, achievements via public APIs
2. **Normalizes into a unified system** — Power Score (0-1000) based on percentiles for each metric with a transparent formula
3. **Visualizes the profile** — skill radar chart, global percentiles, milestone-based leagues
4. **Provides social tools** — head-to-head comparisons with friends, shareable profile cards

**Key interaction:** sign up → enter your usernames → see Power Score and global percentiles → compare yourself with a friend → share your card.

## What Makes SkillBoard Special

- **Cross-domain aggregation** — the only product that combines fundamentally different skills (chess + code + more) into one profile. All existing analogs operate within a single domain.
- **Head-to-head comparison** — the most viral feature. "I beat my friend at chess, but they're stronger at coding" — content that gets shared naturally. Only shared platforms are compared to keep it fair.
- **Transparent scoring** — Power Score is based on percentiles with a publicly visible formula and breakdown by each metric. Users always see what their score is made of.
- **Zero-friction onboarding** — MVP uses public APIs from Chess.com and GitHub that don't require OAuth or API keys. Just enter a username.
- **Standalone value from the first second** — even without friends on the platform, a user sees their global percentiles ("you're in the top 10% of Chess.com players"). Social features add value but aren't required.

## Who It's For

**Primary audience:** people who actively develop skills across multiple platforms and want to see their progress and compare it with friends.

**Usage trigger:** "I want to show my friend I'm better" or "I'm curious what level I'm actually at."

**First users:** personal circle of friends — people with whom there's already a habit of comparing achievements informally.

## Success Criteria

As a pet project, the MVP is a proof of concept for the "aha moment":

- Friends added their usernames and saw their profiles
- Head-to-head comparisons generate discussions
- Users share their cards in chats
- Global percentiles provide value even without friends on the platform

Retention mechanics (notifications, weekly recap, progress tracking) are a post-MVP task.

## Scope: MVP

**Included:**
- Registration / authentication
- Adding Chess.com and GitHub usernames to profile
- Profile with Power Score, global percentiles, radar chart
- Absolute Score (% of world top) and Percentile Rank (based on known platform distributions)
- Head-to-head comparison of two users (only shared platforms)
- Shareable profile card
- Milestone-based leagues by Power Score (Bronze → Legend) — tied to global thresholds, not user count
- Periodic data sync from platforms (on-demand with caching)

**Not included in MVP:**
- Other platforms (LeetCode, Lichess, Strava, Spotify)
- Friends / follow system
- Challenges between users
- Progress timeline with historical graphs
- Weekly digest / notifications
- Embeddable SVG cards for GitHub README

## Vision

If SkillBoard works for chess + GitHub among friends, it scales in two directions:

1. **More platforms** — LeetCode, Codeforces, Lichess, Strava, Duolingo, AniList. Each new integration expands the audience and enriches the profile.
2. **More social mechanics** — friends system, challenges ("beat my rating by end of month"), weekly movers, segmented leagues (Duolingo-style with promotion/demotion), embeddable SVG cards, periodic "Wrapped" recaps.

The ultimate goal is to become the place where anyone can see their multi-domain skill profile, track progress, and compete healthily with friends.
