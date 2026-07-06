#!/usr/bin/env python3
"""
generate-affiliate-links.py

Reads all markdown files in src/content/, finds '## AFFILIATE_LINK ##' placeholders,
and replaces them with actual affiliate CTAs based on the tool(s) referenced in each article.

Usage: python3 scripts/generate-affiliate-links.py
"""

import json
import os
import re
import sys

# --- Configuration ---
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(SITE_ROOT, "src", "content")
AFFILIATE_CONFIG = os.path.join(SITE_ROOT, "src", "config", "affiliate.json")
PLACEHOLDER = "## AFFILIATE_LINK ##"

# Mapping from product names in frontmatter / titles to affiliate keys
PRODUCT_TO_KEY = {
    # Reviews
    "Cursor": "cursor",
    "Cursor AI": "cursor",
    "GitHub Copilot": "github-copilot",
    "JetBrains AI Assistant": "jetbrains",
    "JetBrains": "jetbrains",
    "ChatGPT": "openai",
    "OpenAI": "openai",
    "Notion": "notion",
    "Vercel": "vercel",
    "DigitalOcean": "digitalocean",
    "Supabase": "supabase",
    "Anthropic": "anthropic",
    "Claude": "anthropic",
    "Linear": "linear",
    "Sentry": "sentry",
    "Codeium": "codeium",
    "Cody": "cody",
    "Sourcegraph": "cody",
    "Tabnine": "tabnine",
    "LangSmith": "langsmith",
    "Langfuse": "langfuse",
    "Groq": "groq",
    "Together AI": "together",
    "Replicate": "replicate",
    "Hugging Face": "huggingface",
    "PostHog": "posthog",
    "Raycast": "raycast",
}

# For multi-tool articles, map file paths (relative to content/) to lists of affiliate keys
MULTI_TOOL_MAP = {
    "bestof/best-free-ai-code-assistants.md": ["cursor", "github-copilot", "codeium", "tabnine", "cody"],
    "bestof/best-ai-monitoring-tools.md": ["langfuse", "langsmith", "sentry", "posthog"],
    "bestof/best-ai-writing-tools-developers.md": ["notion", "raycast"],
    "bestof/best-ai-api-platforms.md": ["groq", "together", "replicate", "huggingface"],
    "bestof/best-ai-coding-assistants.md": ["cursor", "github-copilot", "codeium", "tabnine", "cody"],
    "comparisons/claude-vs-chatgpt-coding.md": ["anthropic", "openai"],
    "comparisons/cursor-vs-github-copilot.md": ["cursor", "github-copilot"],
    "comparisons/chatgpt-vs-claude-vs-gemini.md": ["openai", "anthropic"],
    "alternatives/github-copilot-alternatives.md": ["cursor", "codeium", "cody", "tabnine"],
    "alternatives/best-midjourney-alternatives.md": [],  # no affiliate links for image gen
}


def load_affiliate_config():
    with open(AFFILIATE_CONFIG, "r") as f:
        return json.load(f)


def parse_frontmatter(content):
    """Extract YAML frontmatter as a dict from markdown content."""
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        m = re.match(r'^(\w+):\s*"?([^"]*)"?', line)
        if m:
            fm[m.group(1)] = m.group(2).strip('"')
    return fm


def resolve_affiliate_keys(filepath, frontmatter, content):
    """Determine which affiliate keys apply to this article."""
    rel = os.path.relpath(filepath, CONTENT_DIR)

    # Check explicit multi-tool map first
    if rel in MULTI_TOOL_MAP:
        keys = MULTI_TOOL_MAP[rel]
        if keys:
            return keys
        # Empty list means no affiliate links for this article
        return []

    # Try product field from frontmatter
    product = frontmatter.get("product") or frontmatter.get("original_product")
    if product:
        key = PRODUCT_TO_KEY.get(product)
        if key:
            return [key]
        # Fuzzy match: check if product name is a substring of any known name
        product_lower = product.lower().replace(" ", "")
        for known_name, key in PRODUCT_TO_KEY.items():
            if known_name.lower().replace(" ", "") in product_lower or product_lower in known_name.lower().replace(" ", ""):
                return [key]

    # Fallback: scan title for known product names
    title = frontmatter.get("title", "")
    found_keys = []
    for name, key in PRODUCT_TO_KEY.items():
        if name.lower() in title.lower() and key not in found_keys:
            found_keys.append(key)
    if found_keys:
        return found_keys

    # Last resort: return all affiliate tools (for generic articles)
    return []


def generate_cta(key, affiliate_data):
    """Generate a single affiliate CTA line."""
    tool = affiliate_data[key]
    return f"👉 [Try {tool['name']} →]({tool['url']})"


def process_file(filepath, affiliate_data):
    """Process a single markdown file. Returns True if modified."""
    with open(filepath, "r") as f:
        content = f.read()

    if PLACEHOLDER not in content:
        return False

    frontmatter = parse_frontmatter(content)
    keys = resolve_affiliate_keys(filepath, frontmatter, content)

    if not keys:
        # Remove placeholder with no replacement (no relevant affiliate)
        new_content = content.replace(f"\n{PLACEHOLDER}\n", "\n")
        new_content = new_content.replace(f"\n{PLACEHOLDER}", "")
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            return True
        return False

    # Build CTA block
    cta_lines = []
    for key in keys:
        if key in affiliate_data:
            cta_lines.append(generate_cta(key, affiliate_data))

    cta_block = "\n".join(cta_lines)
    new_content = content.replace(PLACEHOLDER, cta_block)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        return True
    return False


def main():
    affiliate_data = load_affiliate_config()
    print(f"Loaded {len(affiliate_data)} affiliate programs from {AFFILIATE_CONFIG}")

    modified = 0
    skipped = 0

    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            if process_file(filepath, affiliate_data):
                rel = os.path.relpath(filepath, SITE_ROOT)
                print(f"  ✅ Updated: {rel}")
                modified += 1
            else:
                skipped += 1

    print(f"\nDone! Updated {modified} files, skipped {skipped} files (no placeholder or no match).")


if __name__ == "__main__":
    main()
