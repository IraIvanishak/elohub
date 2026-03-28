---
name: check-layout
description: Use Playwright MCP to visit all app routes, screenshot each, and report layout issues
---

# Check Layout

Visually inspect all SkillBoard routes using Playwright MCP and report any layout issues.

## Prerequisites

- The dev server must be running at `http://127.0.0.1:8000`
- Playwright MCP must be configured

## Instructions

1. Navigate to each of the following public routes and take a full-page screenshot:
   - `/` (Leaderboard)
   - `/login`
   - `/register`
   - `/compare`
   - `/u/anya` (sample profile — pick any seeded user if anya is unavailable)

2. For each page, use `browser_snapshot` to capture the accessibility tree and check:
   - **Navigation**: navbar renders with all expected links (SkillBoard, Leaderboard, Compare, Login/Register or Profile/Logout)
   - **Content**: main content area is not empty or broken
   - **Structure**: headings, tables, forms, and cards render with expected elements
   - **Console errors**: note any JS errors (ignore favicon 404)

3. If the user is not logged in, also log in as a demo user (e.g., `anya` / `password`) and re-check:
   - `/profile` (authenticated profile page)
   - Navbar should now show Profile/Logout instead of Login/Register

## Output Format

For each route, report:

### [Route Name] — [URL]
- **Status**: OK / Issue Found
- **Screenshot**: [link to saved screenshot]
- **Issues**: (if any) describe what looks wrong

### Summary
- Total pages checked: N
- Issues found: N
- List any recurring problems (e.g., broken CSS, missing elements, console errors)
