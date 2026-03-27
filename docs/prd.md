---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
inputDocuments:
  - docs/product-brief-skillboard.md
  - skill-board-product-concept.md
workflowType: 'prd'
classification:
  projectType: web_app
  domain: general
  complexity: low
  projectContext: greenfield
---

# Product Requirements Document — SkillBoard

**Author:** User
**Date:** 2026-03-27

## Executive Summary

SkillBoard is a web app that aggregates a user's achievements from various platforms (Chess.com, GitHub) into a unified profile with a numeric Power Score (0-1000), global percentiles, a skill radar chart, and head-to-head comparisons between users.

The product solves a specific problem: achievements are scattered across dozens of services, with no single place to see the full picture and compare yourself with friends. SkillBoard normalizes metrics from different platforms through a percentile system, combines them into a composite score, and visualizes it as a social profile.

This is a pet project. First users are a circle of friends. Tech stack: Python + HTMX. The MVP covers two platforms with public APIs (Chess.com, GitHub), enabling zero-friction onboarding — just enter a username.

### What Makes This Special

- **Cross-domain aggregation** — no existing product combines fundamentally different skills (chess + code) into one profile. MetaGamerScore, CodersRank, ChessMonitor only operate within a single domain.
- **Standalone value without network effect** — global percentiles provide value from the first second, even without friends on the platform ("you're in the top 10% of Chess.com players").
- **Head-to-head as a viral loop** — "I beat my friend at chess, but they're stronger at coding" — content that gets shared naturally.
- **Zero-friction onboarding** — public APIs without OAuth/keys, just a username.

## Project Classification

- **Project Type:** Web App (Python + HTMX, server-rendered)
- **Domain:** Social gamification / skill aggregation
- **Complexity:** Low (public APIs, no compliance requirements)
- **Project Context:** Greenfield

## Success Criteria

### User Success

- User adds usernames and sees a profile with Power Score and percentiles in < 2 minutes
- Head-to-head comparison correctly displays metrics only for shared platforms
- Shareable profile card looks appealing and contains key metrics
- Global percentiles reflect actual platform distributions

### Technical Success

- Chess.com and GitHub API responses are cached and don't exceed rate limits
- Pages render server-side via HTMX in < 500ms
- System correctly handles non-existent or private usernames

### Measurable Outcomes

- Friends (5-10 people) created profiles and connected at least one platform
- At least one head-to-head comparison generated a discussion in chat
- At least one shareable card was sent via messenger/social media

## Product Scope

### MVP — Minimum Viable Product

- Registration / authentication
- Adding Chess.com and GitHub usernames to profile
- Fetching and caching data from public APIs
- Profile: Power Score, global percentiles, radar chart
- Absolute Score (% of world top) and Percentile Rank
- Head-to-head comparison of two users (shared platforms only)
- Shareable static profile card
- Milestone-based leagues (Bronze → Legend) based on global Power Score thresholds

### Growth Features (Post-MVP)

- New platforms: LeetCode, Lichess, Codeforces, Strava
- Friends / follow system
- Progress timeline with historical graphs
- Weekly digest / notifications about rating changes
- Embeddable SVG cards for GitHub README
- Challenges between users

### Vision (Future)

- Segmented leagues (Duolingo-style, ~30 users, weekly promotion/demotion)
- Periodic "Wrapped" recaps (monthly/quarterly)
- Achievements / badges (dynamic, losable)
- Teams / guilds
- 10+ platform integrations

## User Journeys

### Journey 1: First Profile — "What's my percentile?"

**Persona:** Max, 25 years old, plays chess on Chess.com (rapid ~1400) and has a GitHub with several projects.

Max heard about SkillBoard from a friend and decided to try it. He signs up, enters his Chess.com username `maxchess97` and GitHub `maxdev97`. Within a few seconds he sees his profile: Power Score 584 (Gold), Chess.com rapid in top 15%, GitHub stars in top 40%. The radar chart shows he's stronger at chess than coding. "Oh, I didn't even realize my rating was top 15%." He screenshots the card and drops it in the group chat.

### Journey 2: Head-to-Head — "Who's better?"

**Persona:** Max (Power Score 584) vs Anna (Power Score 612).

Anna says in chat: "I passed you in Power Score." Max opens SkillBoard, selects head-to-head with Anna. He sees: he wins at chess (1400 vs 1150), but she's significantly stronger on GitHub (320 stars vs 45). Overall score: Anna 2:1. "Ok, but I'm better at chess." He shares the comparison result in chat. Friends start comparing themselves with each other.

### Journey 3: New user with one platform

**Persona:** Oleg, 28 years old, active on GitHub (500+ stars), doesn't play chess.

Oleg saw Max's card in chat. He signs up, enters only his GitHub username. He sees his profile: GitHub Power Score 720 (Platinum), top 5% by stars. The radar chart shows only GitHub metrics. He compares himself with Max — comparison works only for GitHub (the shared platform). Oleg wins on GitHub, but the overall comparison is limited to one domain. "I should start playing chess too."

### Journey 4: Edge case — non-existent username

**Persona:** Any user who made a typo entering a username.

The user enters Chess.com username `nonexistent_player_xyz`. The system makes an API request, gets a 404. It shows a clear message: "User nonexistent_player_xyz not found on Chess.com. Check the username and try again." The user corrects it and continues.

### Journey Requirements Summary

- Registration and adding platform usernames should take < 2 minutes
- Profile displays immediately after fetching data from APIs
- Head-to-head works only for shared platforms
- Users with one platform get a full profile (no empty sections)
- Username validation errors provide clear feedback
- Shareable card is generated automatically for every profile

## Web App Specific Requirements

### Technical Architecture

- **Server-side rendering:** Python backend (Django/Flask/FastAPI) + HTMX for interactivity
- **Database:** storage for users, connected platforms, cached metrics, computed scores
- **External API integration:** Chess.com (public, no keys), GitHub (public, 60 req/hr without token)
- **Caching layer:** caching API responses (1-6 hours) to reduce load on external APIs

### Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge — last 2 versions)
- Mobile-responsive design

### Authentication

- Email/password or OAuth (GitHub) for registration
- Session-based authentication

### SEO & Accessibility

- Public profiles accessible without authentication (for sharing)
- Basic semantic HTML structure
- Open Graph meta tags for link preview when sharing

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-solving MVP — the minimum set of features that proves the core value proposition (aggregation + comparison).

**Resource Requirements:** Solo developer (pet project). Python + HTMX enables fast iteration without a separate frontend.

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Journey 1 (first profile) — fully
- Journey 2 (head-to-head) — fully
- Journey 3 (one platform) — fully
- Journey 4 (edge cases) — fully

**Must-Have Capabilities:**
- Auth (registration/login)
- Platform username management (adding/removing Chess.com, GitHub usernames)
- Data fetching from Chess.com API (stats, profile)
- Data fetching from GitHub API (user, repos)
- Power Score calculation (percentile-based, weighted)
- Profile page (score, percentiles, radar chart, league badge)
- Head-to-head comparison page (shared platforms only)
- Shareable profile card (static image or HTML page)
- Username validation (checking existence on platform)
- Response caching (to stay within rate limits)

### Post-MVP Features

**Phase 2 (Social):**
- Friends / follow system
- Friends leaderboard
- Progress timeline with historical snapshots

**Phase 3 (More Platforms):**
- Lichess, LeetCode, Codeforces integrations
- Platform adapter pattern for easy addition of new sources

### Risk Mitigation Strategy

**Technical Risks:**
- API rate limits (GitHub: 60 req/hr without token) → caching for 1-6 hours, authenticated requests for higher limits
- API changes/downtime → graceful degradation, show cached data with timestamp
- Percentile accuracy → use known Chess.com distributions, for GitHub build our own based on collected users

**Market Risks:**
- Cold start (too few users for leaderboards) → milestone-based leagues instead of population-based, global percentiles work from day 1
- Retention → accepted as a post-MVP task

## Functional Requirements

### User Management

- FR1: User can register with email/password or via GitHub OAuth
- FR2: User can log into an existing account
- FR3: User can log out
- FR4: User can view and edit their profile

### Platform Integration

- FR5: User can add a Chess.com username to their profile
- FR6: User can add a GitHub username to their profile
- FR7: User can remove a connected platform from their profile
- FR8: System validates the existence of a username on the respective platform when adding
- FR9: System shows a clear error message if the username is not found

### Data Fetching & Sync

- FR10: System fetches Chess.com data (rapid/blitz/bullet ratings, puzzle rating, win/loss/draw stats) via public API
- FR11: System fetches GitHub data (public repos, followers, total stars, top languages, account age) via public API
- FR12: System caches API responses and uses cache for repeated requests within TTL
- FR13: User can manually refresh their data (rate limited)
- FR14: System shows the timestamp of the last data update

### Scoring & Analytics

- FR15: System calculates Absolute Score for each metric (% of known platform max)
- FR16: System calculates Percentile Rank for each metric based on known platform distributions
- FR17: System calculates per-platform Power Score (0-1000) based on weighted percentiles
- FR18: System calculates overall Power Score as the average of per-platform scores
- FR19: System determines milestone-based league (Unranked/Bronze/Silver/Gold/Platinum/Diamond/Legend) by Power Score

### Profile Display

- FR20: User can view their profile with Power Score, percentiles, and league
- FR21: Profile displays a skill radar chart (axes = percentiles by metric)
- FR22: Profile shows a breakdown by each platform and metric
- FR23: Public profile is accessible without authentication via URL
- FR24: User with one connected platform sees a full profile without empty sections

### Head-to-Head Comparison

- FR25: User can select another SkillBoard user for comparison
- FR26: Comparison displays metrics only for platforms shared by both users
- FR27: Comparison shows who wins on each metric and the overall score
- FR28: Comparison page is accessible via a shareable URL

### Shareable Cards

- FR29: System generates a visual profile card with key metrics (Power Score, league, per-platform scores)
- FR30: Card is accessible via URL for sharing in messengers and social media
- FR31: Card URL has Open Graph meta tags for correct preview

## Non-Functional Requirements

### Performance

- NFR1: Profile page renders in < 500ms (server-side, without fetching from external APIs)
- NFR2: Initial data fetch from platforms completes in < 5 seconds
- NFR3: Cached data returns in < 100ms

### Security

- NFR4: Passwords are stored as bcrypt/argon2 hashes
- NFR5: Sessions have expiration and secure/httponly cookies
- NFR6: Rate limiting on manual data refresh (max once per hour per user)
- NFR7: Input validation on all username fields (protection against injection)

### Scalability

- NFR8: Architecture supports adding new platforms via adapter pattern without changing core logic
- NFR9: System works correctly with 1-100 users (pet project scale)

### Reliability

- NFR10: If an external API is unavailable, system shows cached data with a timestamp of the last update
- NFR11: Invalid username doesn't break the profile — shows an error message only for the specific platform
