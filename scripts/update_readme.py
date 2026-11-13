#!/usr/bin/env python3
"""Refresh the merged-PR counts and the "Recently merged" list in README.md.

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
from pathlib import Path

USER = "sohailshk"
README = Path(__file__).resolve().parent.parent / "README.md"
RECENT = 5

COUNT_RE = re.compile(r"(<!-- n:([\w.-]+/[\w.-]+) -->)\d*(<!-- /n -->)")
RECENT_RE = re.compile(
    r"(<!-- recent-merged:start -->\n).*?(<!-- recent-merged:end -->)", re.S
)


def search(query, per_page=100):
    params = {"q": query, "per_page": per_page, "sort": "updated", "order": "desc"}
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
        return json.load(response)


def merged_count(repo):
    return search(f"repo:{repo} is:pr is:merged author:{USER}", per_page=1)["total_count"]


def recent_lines():
    items = search(f"is:pr is:merged author:{USER} -user:{USER}")["items"]
    items.sort(key=lambda item: item["pull_request"].get("merged_at") or "", reverse=True)
    lines = []
    for item in items[:RECENT]:
        repo = item["repository_url"].split("/repos/", 1)[1]
        title = item["title"].replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"- [{repo}#{item['number']}]({item['html_url']}) {title}")
    return lines


def main():
    text = README.read_text()
    try:
        repos = sorted({match.group(2) for match in COUNT_RE.finditer(text)})
        counts = {repo: merged_count(repo) for repo in repos}
        lines = recent_lines()
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
        print(f"GitHub API request failed, leaving README unchanged: {error}")
        return 0

    updated = COUNT_RE.sub(lambda m: f"{m.group(1)}{counts[m.group(2)]}{m.group(3)}", text)
    if lines:
        block = "\n".join(lines) + "\n"
        updated = RECENT_RE.sub(lambda m: m.group(1) + block + m.group(2), updated)

    if updated == text:
        print("README already up to date")
    else:
        README.write_text(updated)
        print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
