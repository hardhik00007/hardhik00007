#!/usr/bin/env python3
"""Regenerate local SVG profile cards from GitHub's public API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections import Counter
from html import escape
from typing import Any

USERNAME = "hardhik00007"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

PALETTE = {
    "C++": "#c98c75",
    "Python": "#8fae9d",
    "JavaScript": "#c5b06b",
    "TypeScript": "#87a9b4",
    "Java": "#b7a18e",
    "C": "#9ba6aa",
    "HTML": "#c98c75",
    "CSS": "#9da7b4",
    "Go": "#8fae9d",
    "Rust": "#c98c75",
}
FALLBACK = "#aeb2ad"


def github_json(url: str) -> tuple[Any, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "hardhik00007-profile-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body), {key.lower(): value for key, value in response.headers.items()}
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned HTTP {exc.code}: {details[:500]}") from exc


def fetch_public_repositories() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    profile, _ = github_json(f"https://api.github.com/users/{USERNAME}")
    repositories: list[dict[str, Any]] = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{USERNAME}/repos"
            f"?type=owner&sort=updated&per_page=100&page={page}"
        )
        batch, headers = github_json(url)
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected repositories response from GitHub")

        repositories.extend(repo for repo in batch if not repo.get("private", False))
        if 'rel="next"' not in headers.get("link", ""):
            break
        page += 1

    return profile, repositories


def svg_stats(public_repos: int, forks: int, language_count: int, featured: int) -> str:
    items = [
        (public_repos, "public repositories"),
        (forks, "forks of your repos"),
        (language_count, "primary languages"),
        (featured, "featured projects"),
    ]
    width, height, padding = 980, 184, 22
    column_width = (width - 2 * padding) / len(items)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Public GitHub profile snapshot">',
        f'<rect width="{width}" height="{height}" rx="12" fill="#292b2d" stroke="#565b5d"/>',
        '<text x="22" y="29" fill="#e8e6de" font-family="Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="1.2">PUBLIC PROFILE SNAPSHOT</text>',
    ]

    for index, (value, label) in enumerate(items):
        x = padding + index * column_width
        if index:
            parts.append(f'<path d="M{x:.1f} 45V166" stroke="#565b5d"/>')
        parts.extend([
            f'<text x="{x + 10:.1f}" y="103" fill="#d7e52c" font-family="Arial,sans-serif" font-size="38" font-weight="700">{value}</text>',
            f'<text x="{x + 10:.1f}" y="130" fill="#b8bab5" font-family="Arial,sans-serif" font-size="11" letter-spacing="1.1">{escape(label.upper())}</text>',
        ])

    parts.append("</svg>")
    return "\n".join(parts)


def svg_languages(counts: Counter[str]) -> str:
    width, height = 980, 300
    top_languages = counts.most_common(6)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Primary languages used across public repositories">',
        f'<rect width="{width}" height="{height}" rx="12" fill="#292b2d" stroke="#565b5d"/>',
        '<text x="24" y="33" fill="#e8e6de" font-family="Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="1.1">PRIMARY LANGUAGE BY REPOSITORY</text>',
        '<text x="24" y="55" fill="#969a9a" font-family="Arial,sans-serif" font-size="11">Counts GitHub’s primary-language label once per public repository</text>',
    ]

    if not top_languages:
        parts.append('<text x="24" y="110" fill="#b8bab5" font-family="Arial,sans-serif" font-size="14">No language metadata is available yet.</text>')

    maximum = max((count for _, count in top_languages), default=1)
    for index, (language, count) in enumerate(top_languages):
        y = 91 + index * 32
        bar_width = int(560 * count / maximum)
        color = PALETTE.get(language, FALLBACK)
        suffix = "repo" if count == 1 else "repos"

        parts.extend([
            f'<text x="24" y="{y + 4}" fill="#e8e6de" font-family="Arial,sans-serif" font-size="13">{escape(language)}</text>',
            f'<rect x="180" y="{y - 10}" width="600" height="11" rx="5.5" fill="#45494b"/>',
            f'<rect x="180" y="{y - 10}" width="{bar_width}" height="11" rx="5.5" fill="{color}"/>',
            f'<text x="814" y="{y + 4}" fill="#b8bab5" font-family="Arial,sans-serif" font-size="12">{count} {suffix}</text>',
        ])

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    profile, repositories = fetch_public_repositories()

    # public_repos includes the special profile repository itself.
    public_repo_count = int(profile.get("public_repos", len(repositories)))
    fork_count = sum(int(repo.get("forks_count", 0)) for repo in repositories)
    primary_languages = Counter(
        str(repo["language"])
        for repo in repositories
        if repo.get("language") and repo.get("name", "").lower() != USERNAME.lower()
    )

    # One of the four selected projects is hosted under a collaborator's account.
    featured_project_count = 4

    with open(os.path.join(ASSETS, "profile-stats.svg"), "w", encoding="utf-8") as file:
        file.write(svg_stats(
            public_repo_count,
            fork_count,
            len(primary_languages),
            featured_project_count,
        ))

    with open(os.path.join(ASSETS, "languages.svg"), "w", encoding="utf-8") as file:
        file.write(svg_languages(primary_languages))

    print(
        f"Updated profile cards: {public_repo_count} public repos, "
        f"{fork_count} repo forks, {len(primary_languages)} primary languages, "
        f"{featured_project_count} featured projects."
    )


if __name__ == "__main__":
    main()
