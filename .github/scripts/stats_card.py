"""Render the 'adventure log' stats card from the GitHub GraphQL API.

Usage:
  GITHUB_TOKEN=... python stats_card.py <user> <out.svg>
  python stats_card.py --sample <out.svg>      # offline, fake numbers (for design checks)
"""
import datetime as dt
import html
import json
import os
import sys
import urllib.request
from pathlib import Path

MONO = "'JetBrains Mono','D2Coding','Consolas','Menlo',monospace"
SANS = "'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Segoe UI',sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def sample():
    today = dt.date.today()
    days = [{"date": (today - dt.timedelta(days=i)).isoformat(), "contributionCount": (i * 7) % 5}
            for i in range(364, -1, -1)]
    langs = [("Python", "#3572A5", 520000), ("Java", "#b07219", 410000),
             ("JavaScript", "#f1e05a", 150000), ("HTML", "#e34c26", 60000), ("CSS", "#663399", 30000)]
    return {
        "repositories": {"totalCount": 15, "nodes": [
            {"languages": {"edges": [{"size": s, "node": {"name": n, "color": c}} for n, c, s in langs]}}]},
        "contributionsCollection": {
            "totalCommitContributions": 312,
            "contributionCalendar": {"totalContributions": 401, "weeks": [{"contributionDays": days}]},
        },
    }


def streaks(days):
    counts = [d["contributionCount"] for d in sorted(days, key=lambda d: d["date"])]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # today isn't over yet, so an empty today doesn't break the current streak
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    current = 0
    for c in reversed(tail):
        if not c:
            break
        current += 1
    return current, longest


def top_languages(repos, n=5):
    total = {}
    for repo in repos:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            size, color = total.get(name, (0, e["node"]["color"] or "#94a3b8"))
            total[name] = (size + e["size"], color)
    ranked = sorted(total.items(), key=lambda kv: -kv[1][0])
    grand = sum(s for s, _ in total.values()) or 1
    top = [(name, color, size / grand) for name, (size, color) in ranked[:n]]
    rest = 1 - sum(p for _, _, p in top)
    if rest > 0.005:
        top.append(("기타", "#475569", rest))
    return top


def render(u):
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    current, longest = streaks(days)
    stats = [
        ("최근 1년 기여", f'{cc["contributionCalendar"]["totalContributions"]:,}', "#a78bfa"),
        ("최근 1년 커밋", f'{cc["totalCommitContributions"]:,}', "#38bdf8"),
        ("연속 기록", f"{current}일", "#f97316"),
        ("최장 연속", f"{longest}일", "#fbbf24"),
        ("공개 저장소", f'{u["repositories"]["totalCount"]}', "#22c55e"),
    ]
    langs = top_languages(u["repositories"]["nodes"])
    W, H = 800, 250

    tiles = []
    for i, (label, value, color) in enumerate(stats):
        x, y = 40 + (i % 3) * 130, 92 + (i // 3) * 66
        tiles.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.2 + i * 0.12:.2f}s" dur="0.5s" fill="freeze"/>'
            f'<text x="{x}" y="{y}" font-size="12" fill="#94a3b8" font-family="{SANS}">{label}</text>'
            f'<text x="{x}" y="{y + 28}" font-size="24" font-weight="800" fill="{color}">{html.escape(value)}</text></g>')

    BX, BY, BW = 440, 96, 320
    bar, legend, x = [], [], BX
    for i, (name, color, pct) in enumerate(langs):
        w = BW * pct
        bar.append(f'<rect x="{x:.1f}" y="{BY}" width="0" height="14" fill="{color}">'
                   f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{0.4 + i * 0.15:.2f}s" dur="0.6s" fill="freeze"/></rect>')
        x += w
        lx, ly = BX + (i % 2) * 165, BY + 40 + (i // 2) * 24
        legend.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
                      f'<text x="{lx + 16}" y="{ly}" font-size="13" fill="#e2e8f0" font-family="{SANS}">{html.escape(name)}'
                      f'<tspan fill="#64748b"> {pct * 100:.1f}%</tspan></text>')

    updated = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y-%m-%d")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <filter id="glow" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="barclip"><rect x="{BX}" y="{BY}" width="{BW}" height="14" rx="7"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="#070b1d"/>
  <rect x="16" y="16" width="{W - 32}" height="{H - 32}" rx="10" fill="#0ea5e9" fill-opacity="0.07" stroke="#67e8f9" stroke-width="1.5" filter="url(#glow)"/>
  <text x="40" y="52" font-size="16" font-weight="700" fill="#a5f3fc" font-family="{SANS}" filter="url(#glow)">◆ 모험 기록</text>
  <text x="{W - 40}" y="52" font-size="11" fill="#22d3ee" text-anchor="end" opacity="0.7">ADVENTURE LOG · updated {updated}</text>
  <line x1="40" y1="64" x2="{W - 40}" y2="64" stroke="#67e8f9" stroke-opacity="0.35"/>
  {"".join(tiles)}
  <line x1="414" y1="80" x2="414" y2="{H - 36}" stroke="#1e3a5f" stroke-dasharray="4 4"/>
  <text x="{BX}" y="{BY - 10}" font-size="12" fill="#94a3b8" font-family="{SANS}">주 사용 언어</text>
  <rect x="{BX}" y="{BY}" width="{BW}" height="14" rx="7" fill="#0b1026"/>
  <g clip-path="url(#barclip)">{"".join(bar)}</g>
  {"".join(legend)}
</svg>
'''


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    who, out = sys.argv[1], Path(sys.argv[2])
    if who == "--sample":
        data = sample()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN is not set")
        data = fetch(who, token)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
