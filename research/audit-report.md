# Dogfood QA Report

**Target:** https://devtools-pick.vercel.app
**Date:** July 6, 2026
**Scope:** Full site QA — homepage, article pages (review, comparison, alternatives, best-of), category pages, navigation, footer links, SEO, affiliate CTAs, internal links
**Tester:** Hermes Agent (automated exploratory QA)

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 2 |
| 🟠 High | 4 |
| 🟡 Medium | 3 |
| 🔵 Low | 3 |
| **Total** | **12** |

**Overall Assessment:** The site has solid content and clean design, but two critical issues — broken best-of article links and a non-rendering affiliate CTA — directly block revenue and user experience. A systemic canonical URL misconfiguration points all SEO value to a non-existent domain.

---

## Issues

### Issue #1: Best-Of Article Links All Return 404

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Category** | Functional |
| **URL** | Homepage → any Best-Of article card |

**Description:**
All five best-of article cards on the homepage link to URLs under `/bestof/` (e.g., `/bestof/best-ai-api-platforms`), but the actual Astro routes use `/best-of/` (e.g., `/best-of/best-ai-api-platforms`). This means every best-of article link from the homepage, the best-of category page, and any internal cross-links from other articles results in a 404.

**Steps to Reproduce:**
1. Navigate to https://devtools-pick.vercel.app
2. Scroll to "Best Of Lists" section
3. Click any article card (e.g., "8 Best AI API Platforms for Developers in 2026")
4. Observe 404 error page

**Expected Behavior:** Article loads with full content.

**Actual Behavior:** Vercel 404 error page. The URL mismatch is:
- Homepage links: `/bestof/best-ai-api-platforms` (❌ broken)
- Actual routes: `/best-of/best-ai-api-platforms` (✅ works)
- Same mismatch applies to all 5 best-of articles

**Impact:** 5 articles (~36% of total content) are unreachable from the homepage or category pages. This is the single biggest UX and revenue issue on the site.

---

### Issue #2: Affiliate CTA Section Renders as Literal "AFFILIATE_LINK" Text

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Category** | Functional / Content |
| **URL** | All article pages (reviews, comparisons, alternatives, best-of) |

**Description:**
Every article page contains an `<h2>` heading that reads "AFFILIATE_LINK" — a template variable that was never replaced with actual CTA content. The affiliate section appears as:
```
<h2>AFFILIATE_LINK</h2>
```
with no button, no link, and no call-to-action beneath it. This was confirmed on:
- `/reviews/cursor-review`
- `/reviews/github-copilot-review`
- `/comparisons/claude-vs-chatgpt-coding`
- `/comparisons/cursor-vs-github-copilot`
- `/alternatives/github-copilot-alternatives`
- `/best-of/best-ai-coding-assistants`

**Steps to Reproduce:**
1. Navigate to any article page
2. Scroll to the bottom of the article content (before "Related Articles")
3. Observe the literal text "AFFILIATE_LINK" rendered as a heading

**Expected Behavior:** A styled affiliate CTA box with a product link, description, and call-to-action button.

**Actual Behavior:** Raw template variable text "AFFILIATE_LINK" displayed as an `<h2>`.

**Impact:** Directly kills affiliate revenue. Users see no CTA to click through to product pages.

---

### Issue #3: Canonical URLs Point to aitools.dev Instead of devtools-pick.vercel.app

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Category** | SEO |
| **URL** | All pages (site-wide) |

**Description:**
Every page's `<link rel="canonical">` points to `https://aitools.dev/...` instead of `https://devtools-pick.vercel.app/...`. This is the site's intended production domain, but on the staging/preview deployment at devtools-pick.vercel.app, it creates a mismatch. Search engines may index the wrong URL or de-index the Vercel deployment entirely.

Confirmed on:
- Homepage: `canonical: https://aitools.dev/`
- `/reviews/cursor-review`: `canonical: https://aitools.dev/reviews/cursor-review/`
- `/comparisons/claude-vs-chatgpt-coding`: `canonical: https://aitools.dev/comparisons/claude-vs-chatgpt-coding/`
- `/about`: `canonical: https://aitools.dev/about/`

**Expected Behavior:** Canonical URLs match the actual deployment domain, or `aitools.dev` is the live domain and this Vercel URL redirects to it.

**Actual Behavior:** Canonical mismatch between the URL being served and the declared canonical.

---

### Issue #4: Social Share Links Reference aitools.dev

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Category** | Functional / SEO |
| **URL** | All article pages (Twitter, Reddit, LinkedIn share links) |

**Description:**
The Twitter, Reddit, and LinkedIn share links encode `aitools.dev` as the shared URL rather than `devtools-pick.vercel.app`. For example, on the GitHub Copilot alternatives article:
```
Twitter: https://twitter.com/intent/tweet?url=https%3A%2F%2Faitools.dev%2Falternatives%2Fgithub-copilot-alternatives%2F&text=...
Reddit: https://www.reddit.com/submit?url=https%3A%2F%2Faitools.dev%2Falternatives%2Fgithub-copilot-alternatives%2F&title=...
```

If `aitools.dev` is not yet live or doesn't resolve, shared links will lead to dead pages.

---

### Issue #5: robots.txt References Wrong Sitemap Domain

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Category** | SEO |
| **URL** | /robots.txt |

**Description:**
The `robots.txt` file contains:
```
Sitemap: https://aitools.dev/sitemap-index.xml
```
Search engines crawling `devtools-pick.vercel.app` will be directed to a sitemap on a different domain.

---

### Issue #6: OG Image Uses Relative Path

| Field | Value |
|-------|-------|
| **Severity** | 🟠 High |
| **Category** | SEO / Social |
| **URL** | All pages |

**Description:**
The `og:image` meta tag is set to `/og-default.png` (a relative path). While this works when the page is served from the root domain, social media crawlers (Facebook, Twitter, Slack) may not resolve relative paths correctly, resulting in missing preview images when links are shared.

---

### Issue #7: No Custom 404 Page

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Category** | UX |
| **URL** | Any invalid URL (e.g., /nonexistent-page) |

**Description:**
The site uses Vercel's default 404 error page, which shows a barebones error message with a link to Vercel's documentation. There is no navigation back to the homepage, no search functionality, and no suggested pages. For an affiliate site, a custom 404 with popular article links would reduce bounce rate.

**Expected Behavior:** Custom 404 page with navigation, search, and popular article suggestions.

**Actual Behavior:** Default Vercel "404: NOT_FOUND" error page.

---

### Issue #8: "Why Trust Our Reviews?" Section Has No Descriptive Text

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Category** | Content |
| **URL** | Homepage |

**Description:**
The "Why Trust Our Reviews?" section on the homepage displays three headings — "Hands-On Testing", "Transparent Disclosure", "Always Up to Date" — but no supporting paragraph text beneath them. This section appears incomplete and fails to build trust with visitors.

---

### Issue #9: All Articles Show "5 min read" — Likely Placeholder

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Category** | Content |
| **URL** | All article pages |

**Description:**
Every article tested (reviews, comparisons, alternatives, best-of) shows "5 min read" in the article header. Articles range from 800 to 2000+ words — the read time should vary. This suggests the read time is hardcoded rather than calculated.

---

### Issue #10: "Bestof" Category Badge Missing Space

| Field | Value |
|-------|-------|
| **Severity** | 🔵 Low |
| **Category** | Content |
| **URL** | /best-of/best-ai-coding-assistants (and likely other best-of articles) |

**Description:**
The category badge on best-of article pages displays "Bestof" (no space) instead of "Best Of". This appears to be a rendering issue where the category slug is used instead of the display name.

---

### Issue #11: Author Byline Shows Orphaned "A" Character

| Field | Value |
|-------|-------|
| **Severity** | 🔵 Low |
| **Category** | Visual |
| **URL** | All article pages |

**Description:**
In the article header section, there is a standalone "A" character before the "AI Tools Team" byline. This appears to be an avatar initial that is not properly styled or contained — it renders as a plain "A" rather than as a styled avatar circle.

---

### Issue #12: Homepage Article Count May Be Stale

| Field | Value |
|-------|-------|
| **Severity** | 🔵 Low |
| **Category** | Content |
| **URL** | Homepage |

**Description:**
The homepage states "14 articles · Updated weekly" in the hero section. The actual article count based on category pages is:
- Reviews: 4
- Comparisons: 3
- Alternatives: 2
- Best Of: 5
- **Total: 14**

The count is currently accurate but hardcoded rather than dynamically calculated — it will drift as content is added.

---

## Issues Summary Table

| # | Title | Severity | Category | URL |
|---|-------|----------|----------|-----|
| 1 | Best-Of article links all return 404 | 🔴 Critical | Functional | Homepage → /bestof/* |
| 2 | Affiliate CTA renders as "AFFILIATE_LINK" text | 🔴 Critical | Functional | All article pages |
| 3 | Canonical URLs point to aitools.dev | 🟠 High | SEO | All pages |
| 4 | Social share links reference aitools.dev | 🟠 High | Functional | All article pages |
| 5 | robots.txt references wrong sitemap domain | 🟠 High | SEO | /robots.txt |
| 6 | OG image uses relative path | 🟠 High | SEO/Social | All pages |
| 7 | No custom 404 page | 🟡 Medium | UX | Any invalid URL |
| 8 | "Why Trust" section lacks descriptive text | 🟡 Medium | Content | Homepage |
| 9 | All articles show "5 min read" (placeholder) | 🟡 Medium | Content | All articles |
| 10 | "Bestof" category badge missing space | 🔵 Low | Content | Best-of articles |
| 11 | Orphaned "A" in author byline | 🔵 Low | Visual | All articles |
| 12 | Hardcoded article count on homepage | 🔵 Low | Content | Homepage |

---

## Testing Coverage

### Pages Tested
- ✅ Homepage (`/`)
- ✅ Reviews category (`/reviews`)
- ✅ Comparisons category (`/comparisons`)
- ✅ Alternatives category (`/alternatives`)
- ✅ Best Of category (`/best-of`)
- ✅ Cursor AI Review (`/reviews/cursor-review`)
- ✅ GitHub Copilot Review (`/reviews/github-copilot-review`)
- ✅ Claude vs ChatGPT Coding (`/comparisons/claude-vs-chatgpt-coding`)
- ✅ Cursor vs GitHub Copilot (`/comparisons/cursor-vs-github-copilot`)
- ✅ GitHub Copilot Alternatives (`/alternatives/github-copilot-alternatives`)
- ✅ Best AI Coding Assistants (`/best-of/best-ai-coding-assistants`)
- ✅ About (`/about`)
- ✅ Privacy Policy (`/privacy`)
- ✅ Terms of Service (`/terms`)
- ✅ Affiliate Disclosure (`/affiliate-disclosure`)
- ✅ 404 error page (nonexistent URL)
- ✅ robots.txt
- ✅ sitemap-index.xml

### Features Tested
- Navigation links (header, footer)
- Article card links from homepage
- Breadcrumb navigation on articles
- Affiliate CTA sections
- Related articles links
- Social share links
- Newsletter signup form
- Category page listings
- SEO meta tags (title, description, canonical, OG)
- Heading hierarchy (H1-H3)
- Console errors (JS)
- Responsive meta viewport

### Not Tested / Out of Scope
- Mobile viewport rendering (requires viewport resize simulation not available in headless browser at this resolution)
- Newsletter form submission (no backend to test against)
- Actual affiliate link click-through destinations
- Page load performance / Core Web Vitals
- Accessibility audit (WCAG compliance)
- Social media preview rendering (requires live URL)
- RSS/Atom feed

### Blockers
- None — all pages were accessible and testable

---

## Notes

### Positive Findings
- **Clean, professional design** — The Vercel design system overhaul looks polished with consistent typography, spacing, and color palette
- **Zero console errors** — No JavaScript errors detected on any page tested
- **Good heading structure** — Proper H1→H2→H3 hierarchy on all pages
- **Meta descriptions present** — All pages have unique, descriptive meta descriptions
- **Viewport meta tag** — Responsive viewport properly configured
- **Article content quality** — Reviews and comparisons are well-structured with pros/cons, pricing tables, and comparison charts
- **Internal cross-links work** — Related articles links between reviews, comparisons, and alternatives resolve correctly (when not using the broken `/bestof/` prefix)
- **Legal pages present** — Privacy Policy, Terms of Service, and Affiliate Disclosure are all substantive and properly linked

### Recommended Priority Fix Order
1. **Fix best-of article URL routing** (Issue #1) — Highest impact, breaks 5 articles
2. **Fix affiliate CTA template rendering** (Issue #2) — Directly impacts revenue
3. **Update canonical URLs for staging domain** (Issue #3) — Important for SEO during staging
4. **Fix social share URLs** (Issue #4) — Quick fix, prevents broken shares
5. **Fix robots.txt sitemap reference** (Issue #5) — Quick fix
6. **Use absolute URL for og:image** (Issue #6) — Important for social previews

---

*Report generated by Hermes Agent using the Dogfood QA workflow.*
