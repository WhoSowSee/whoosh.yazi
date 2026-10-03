import argparse
from datetime import datetime, timedelta, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import urllib.request


API = "https://api.github.com"
SIZE = (820, 420)
PLOT = (76, 64, 716, 304)
COLORS = {
    "light": ("#ffffff", "#24292f", "#57606a", "#eaecef", "#2f81f7", "#d0d7de", 0.12),
    "dark": ("#0d1117", "#e6edf3", "#8b949e", "#21262d", "#58a6ff", "#30363d", 0.15),
}
LANGUAGES = {
    "en": {
        "heading": "Star History",
        "title": "{repository} star history: {total:,} stars",
        "stars": "{total:,} stars",
        "months": ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
    },
    "ru": {
        "heading": "История звёзд",
        "title": "{repository} — История звёзд: {total}",
        "stars": "Звёзд: {total}",
        "months": ("янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"),
    },
}


def request_json(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "whoosh-yazi-star-history",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}/{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_history(repository):
    weeks = []
    page = 1
    while True:
        batch = request_json(
            f"repos/{repository}/stargazers/history?per_page=30&page={page}"
        )
        weeks.extend(batch)
        if len(batch) < 30:
            return weeks
        page += 1


def cumulative_series(weeks):
    daily = []
    for week in weeks:
        start = datetime.fromtimestamp(week["week"], tz=timezone.utc)
        for day, count in enumerate(week["days"]):
            if count:
                daily.append((start + timedelta(days=day), count))
    total = 0
    series = []
    for date, count in sorted(daily):
        total += count
        series.append((date, total))
    return series


def sample_series(series, limit=160):
    if len(series) <= limit:
        return series
    indices = [round(index * (len(series) - 1) / (limit - 1)) for index in range(limit)]
    return [series[index] for index in indices]


def axis_maximum(total):
    value = max(total, 5)
    magnitude = 10 ** math.floor(math.log10(value))
    return next(
        math.ceil(multiplier * magnitude)
        for multiplier in (1, 2, 2.5, 5, 10)
        if multiplier * magnitude >= value
    )


def render_svg(repository, series, created_at, theme, language="en"):
    labels = LANGUAGES[language]
    background, title, text, grid, line, axis, opacity = COLORS[theme]
    width, height = SIZE
    left, top, plot_width, plot_height = PLOT
    right, bottom = left + plot_width, top + plot_height
    total = series[-1][1] if series else 0
    start = series[0][0] if series else created_at
    end = series[-1][0] if series else start
    if end <= start:
        end = start + timedelta(days=1)
    span = (end - start).total_seconds()
    ceiling = axis_maximum(total)

    def x(date):
        return left + (date - start).total_seconds() / span * plot_width

    def y(count):
        return bottom - count / ceiling * plot_height

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title" '
        'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
        f'<title id="chart-title">{escape(labels["title"].format(repository=repository, total=total))}</title>',
        f'<rect width="{width}" height="{height}" rx="6" fill="{background}"/>',
        f'<text x="{left}" y="30" fill="{title}" font-size="17" '
        f'font-weight="600">{labels["heading"]}</text>',
        f'<text x="{right}" y="30" text-anchor="end" fill="{text}" font-size="13">'
        f'{escape(repository)} &#183; {labels["stars"].format(total=total)}</text>',
    ]
    for tick in range(6):
        count = ceiling * tick / 5
        position = y(count)
        parts.extend([
            f'<line x1="{left}" y1="{position:.1f}" x2="{right}" '
            f'y2="{position:.1f}" stroke="{grid}"/>',
            f'<text x="{left - 8}" y="{position + 4:.1f}" text-anchor="end" '
            f'fill="{text}" font-size="11">{round(count):,}</text>',
        ])
    for tick in range(5):
        date = start + (end - start) * (tick / 4)
        month = labels["months"][date.month - 1]
        if start.year != end.year:
            date_label = f"{month} {date.year}"
        elif language == "ru":
            date_label = f"{date.day:02d} {month}"
        else:
            date_label = f"{month} {date.day:02d}"
        anchor = "start" if tick == 0 else "end" if tick == 4 else "middle"
        parts.append(
            f'<text x="{x(date):.1f}" y="{bottom + 20}" text-anchor="{anchor}" '
            f'fill="{text}" font-size="11">{date_label}</text>'
        )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" '
        f'stroke="{axis}" stroke-width="1.5"/>'
    )
    points = sample_series(series) if series else [(start, 0), (end, 0)]
    coordinates = " ".join(f"{x(date):.1f},{y(count):.1f}" for date, count in points)
    area = f"{left},{bottom} {coordinates} {x(points[-1][0]):.1f},{bottom}"
    parts.extend([
        f'<polygon points="{area}" fill="{line}" fill-opacity="{opacity}"/>',
        f'<polyline points="{coordinates}" fill="none" stroke="{line}" '
        'stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>',
        f'<circle cx="{x(points[-1][0]):.1f}" cy="{y(total):.1f}" r="3.5" fill="{line}"/>',
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate local Star History SVGs.")
    parser.add_argument("--repo", required=True, help="GitHub owner/repository")
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "assets"
    )
    arguments = parser.parse_args()
    metadata = request_json(f"repos/{arguments.repo}")
    created_at = datetime.fromisoformat(metadata["created_at"].replace("Z", "+00:00"))
    series = cumulative_series(fetch_history(arguments.repo))
    charts = {
        (theme, language): render_svg(arguments.repo, series, created_at, theme, language)
        for language in LANGUAGES
        for theme in COLORS
    }
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    for (theme, language), svg in charts.items():
        suffix = "" if language == "en" else f"-{language}"
        path = arguments.output_dir / f"star-history-{theme}{suffix}.svg"
        path.write_text(svg, encoding="utf-8", newline="\n")
        print(f"Generated {path.name}: {series[-1][1] if series else 0} stars")


if __name__ == "__main__":
    main()
