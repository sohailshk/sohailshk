#!/usr/bin/env python3
"""Refresh the auto-updated parts of README.md.

- the company badges at the top (merged PRs, or PRs still in review)
- the merged-PR counts in the contributions table
- the "Recently merged" list

Run daily by .github/workflows/update-readme.yml. Every request is made
before anything is written, so if the GitHub API fails the README is left
exactly as it was.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

USER = "sohailshk"
README = Path(__file__).resolve().parent.parent / "README.md"
RECENT = 5
IN_REVIEW_COLOR = "6e7681"

# Shown at the top in this order, each mapped to the GitHub organizations it
# owns. A company appears only once it has at least one PR, under "merged" if
# any PR there was merged and under "in review" otherwise.
BIG_NAMES = [
    # (label, GitHub organizations, simple-icons logo, badge color)
    ("NVIDIA", ["NVIDIA", "NVIDIA-NeMo", "NVlabs", "isaac-sim", "NVIDIA-Omniverse"], "nvidia", "76B900"),
    ("Google", ["google", "google-deepmind", "google-research", "google-ai-edge", "tensorflow", "keras-team", "jax-ml"], "google", "4285F4"),
    ("Microsoft", ["microsoft"], "", "0078D4"),
    ("Meta", ["facebookresearch", "facebook", "meta-llama"], "meta", "0467DF"),
    ("Apple", ["apple", "ml-explore"], "apple", "555555"),
    ("Intel", ["intel", "openvinotoolkit", "open-edge-platform"], "intel", "0071C5"),
    ("Amazon", ["aws", "awslabs", "autogluon"], "", "FF9900"),
    ("Alibaba", ["alibaba", "modelscope", "QwenLM"], "alibabadotcom", "FF6A00"),
    ("Hugging Face", ["huggingface"], "huggingface", "FFD21E"),
    ("PyTorch", ["pytorch"], "pytorch", "EE4C2C"),
    ("Apache", ["apache"], "apache", "D22128"),
    ("OpenCV", ["opencv"], "opencv", "5C3EE8"),
]

COUNT_RE = re.compile(r"(<!-- n:([\w.-]+/[\w.-]+) -->)\d*(<!-- /n -->)")
RECENT_RE = re.compile(r"(<!-- recent-merged:start -->\n).*?(<!-- recent-merged:end -->)", re.S)
BIG_RE = re.compile(r"(<!-- big-names:start -->\n).*?(<!-- big-names:end -->)", re.S)


def search_all(query):
    """Return every search result for query (the API caps this at 1000)."""
    items, page = [], 1
    while True:
        params = {"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "desc"}
        request = urllib.request.Request(
            "https://api.github.com/search/issues?" + urllib.parse.urlencode(params),
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": f"{USER}-profile-readme",
            },
        )
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        items += data["items"]
        if len(data["items"]) < 100 or len(items) >= min(data["total_count"], 1000):
            return items
        page += 1


def repo_of(item):
    return item["repository_url"].split("/repos/", 1)[1]


def search_link(state, orgs):
    query = f"is:pr is:{state} author:{USER} " + " ".join(f"org:{org}" for org in orgs)
    return "https://github.com/search?" + urllib.parse.urlencode({"q": query, "type": "pullrequests"})


def badge(label, message, color, logo, link, alt):
    def escape(text):
        return urllib.parse.quote(text.replace("-", "--").replace("_", "__"))

    src = f"https://img.shields.io/badge/{escape(label)}-{escape(message)}-{color}?style=for-the-badge"
    if logo:
        src += f"&logo={logo}&logoColor=white"
    return f'  <a href="{link}"><img src="{src}" alt="{alt}"></a>'


def big_names_block(merged, opened):
    merged_by_owner = Counter(repo_of(item).split("/")[0].lower() for item in merged)
    open_by_owner = Counter(repo_of(item).split("/")[0].lower() for item in opened)
    merged_badges, review_badges = [], []
    for label, orgs, logo, color in BIG_NAMES:
        n_merged = sum(merged_by_owner[org.lower()] for org in orgs)
        n_open = sum(open_by_owner[org.lower()] for org in orgs)
        if n_merged:
            merged_badges.append(badge(
                label, f"{n_merged} merged", color, logo, search_link("merged", orgs),
                f"{label}: {n_merged} merged pull requests"))
        elif n_open:
            review_badges.append(badge(
                label, f"{n_open} in review", IN_REVIEW_COLOR, logo, search_link("open", orgs),
                f"{label}: {n_open} pull requests in review"))

    parts = []
    if merged_badges:
        parts += ['<p align="center">', *merged_badges, "</p>"]
    if review_badges:
        parts += ['<p align="center"><sub>In review</sub></p>', '<p align="center">', *review_badges, "</p>"]
    return "\n".join(parts) + "\n"


def recent_lines(merged):
    newest = sorted(merged, key=lambda item: item["pull_request"].get("merged_at") or "", reverse=True)
    lines = []
    for item in newest[:RECENT]:
        title = item["title"].replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"- [{repo_of(item)}#{item['number']}]({item['html_url']}) {title}")
    return lines


def main():
    text = README.read_text()
    try:
        merged = search_all(f"is:pr is:merged author:{USER} -user:{USER}")
        opened = search_all(f"is:pr is:open author:{USER} -user:{USER}")
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
        print(f"GitHub API request failed, leaving README unchanged: {error}")
        return 0

    per_repo = Counter(repo_of(item).lower() for item in merged)
    updated = COUNT_RE.sub(lambda m: f"{m.group(1)}{per_repo[m.group(2).lower()]}{m.group(3)}", text)
    lines = recent_lines(merged)
    if lines:
        block = "\n".join(lines) + "\n"
        updated = RECENT_RE.sub(lambda m: m.group(1) + block + m.group(2), updated)
    if merged or opened:
        block = big_names_block(merged, opened)
        updated = BIG_RE.sub(lambda m: m.group(1) + block + m.group(2), updated)

    if updated == text:
        print("README already up to date")
    else:
        README.write_text(updated)
        print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
