"""Generate animated SVGs for the kimdoodoo12 profile README.

Usage: python gen_svgs.py <output assets dir>
"""
import html
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

MONO = "'JetBrains Mono','D2Coding','Consolas','Menlo',monospace"
SANS = "'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Segoe UI',sans-serif"


def kt(*ts):
    return ";".join(f"{t:.4f}" for t in ts)


def visible(a, b, dur):
    """Discrete opacity animation: visible during [a, b) of a dur-second loop."""
    if a <= 0:
        vals, keys = "1;0", kt(0, b / dur)
    elif b >= dur:
        vals, keys = "0;1", kt(0, a / dur)
    else:
        vals, keys = "0;1;0", kt(0, a / dur, b / dur)
    return (f'<animate attributeName="opacity" calcMode="discrete" values="{vals}" '
            f'keyTimes="{keys}" dur="{dur}s" repeatCount="indefinite"/>')


def text_width(s, fs):
    w = 0.0
    for ch in s:
        if "가" <= ch <= "힣":
            w += 0.95 * fs
        else:
            w += 0.6 * fs
    return w


# ---------------------------------------------------------------- header (isekai opening)
def once(attr, frm, to, begin, dur):
    """One-shot animation that keeps its end state (plays once per page load)."""
    return (f'<animate attributeName="{attr}" from="{frm}" to="{to}" begin="{begin}s" '
            f'dur="{dur}s" fill="freeze"/>')


def rise_in(begin):
    return (f'<animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" '
            f'begin="{begin}s" dur="0.7s" fill="freeze"/>' + once("opacity", 0, 1, begin, 0.7))


def magic_circle(cx, cy):
    def draw(r, begin):
        c = 2 * math.pi * r
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#67e8f9" stroke-width="2" '
                f'stroke-dasharray="{c:.0f}" stroke-dashoffset="{c:.0f}">'
                f'{once("stroke-dashoffset", f"{c:.0f}", 0, begin, 0.8)}</circle>')

    def star(r, rot, begin):
        pts = " ".join(f"{cx + r * math.cos(math.radians(rot + k * 120)):.1f},"
                       f"{cy + r * math.sin(math.radians(rot + k * 120)):.1f}" for k in range(3))
        per = 3 * r * math.sqrt(3)
        return (f'<polygon points="{pts}" fill="none" stroke="#a5f3fc" stroke-width="1.5" '
                f'stroke-dasharray="{per:.0f}" stroke-dashoffset="{per:.0f}">'
                f'{once("stroke-dashoffset", f"{per:.0f}", 0, begin, 0.7)}</polygon>')

    rr = 96
    runes = ("public static void main · SELECT * FROM world · git commit -m isekai · "
             "while(alive) learn() · ")
    return f'''
  <g>
    {draw(112, 0.1)}{draw(80, 0.35)}{star(80, -90, 0.6)}{star(80, 90, 0.75)}
    <path id="rune" d="M {cx - rr} {cy} a {rr} {rr} 0 1 1 {2 * rr} 0 a {rr} {rr} 0 1 1 {-2 * rr} 0" fill="none"/>
    <g opacity="0">{once("opacity", 0, 1, 0.5, 0.5)}
      <text font-size="10.5" fill="#67e8f9"><textPath href="#rune" xlink:href="#rune">{runes}</textPath></text>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>
    </g>
  </g>'''


def header():
    W, H = 900, 280
    CX, CY = W / 2, 140
    FLASH = 1.3

    random.seed(7)
    stars = "".join(
        f'<circle cx="{random.uniform(20, W - 20):.0f}" cy="{random.uniform(15, 150):.0f}" '
        f'r="{random.uniform(0.8, 2.2):.1f}" fill="#fff">'
        f'<animate attributeName="opacity" values="0.15;0.95;0.15" dur="{random.uniform(2, 5):.1f}s" '
        f'begin="{random.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(26))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b1026"/><stop offset="0.55" stop-color="#4c1d95"/><stop offset="1" stop-color="#f472b6"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fde68a"/><stop offset="0.5" stop-color="#fbbf24"/><stop offset="1" stop-color="#fde68a"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="#05060f"/>

  <!-- the other world (revealed by the flash) -->
  <g opacity="0">{once("opacity", 0, 1, FLASH + 0.1, 0.4)}
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    {stars}
    <circle cx="815" cy="44" r="24" fill="#fef3c7" opacity="0.9" filter="url(#glow)"/>
    <circle cx="858" cy="76" r="9" fill="#bae6fd" opacity="0.85" filter="url(#glow)"/>
    <path d="M0 {H} L0 232 L90 196 L170 226 L260 184 L350 222 L430 200 L520 230 L610 190 L700 220 L800 186 L{W} 214 L{W} {H} Z" fill="#2e1065" opacity="0.85"/>
    <path d="M0 {H} L0 252 L120 230 L240 256 L380 236 L520 258 L660 238 L780 256 L{W} 240 L{W} {H} Z" fill="#1e1b4b"/>
  </g>

  <!-- summoning circle: full strength in the dark, then fades behind the title -->
  <g filter="url(#glow)">
    {once("opacity", 1, 0.22, FLASH + 0.2, 0.6)}
    {magic_circle(CX, CY)}
  </g>

  <rect width="{W}" height="{H}" fill="#fff" opacity="0">
    <animate attributeName="opacity" values="0;1;0" begin="{FLASH}s" dur="0.8s" fill="freeze"/>
  </rect>

  <g font-family="{SANS}" text-anchor="middle">
    <g opacity="0">{rise_in(FLASH + 0.6)}
      <rect x="{CX - 34}" y="44" width="68" height="26" rx="13" fill="#000" fill-opacity="0.35" stroke="#fde68a"/>
      <text x="{CX}" y="62" font-size="14" font-weight="700" fill="#fde68a">제1화</text>
    </g>
    <g opacity="0">{rise_in(FLASH + 1.0)}
      <text x="{CX}" y="152" font-size="46" font-weight="900" fill="url(#gold)" filter="url(#glow)">어둠의 개발자가 되고 싶어서!</text>
    </g>
    <g opacity="0">{rise_in(FLASH + 2.4)}
      <text x="{CX}" y="204" font-size="15" fill="#e9d5ff" letter-spacing="2">— 두두 (doodoo) —</text>
    </g>
  </g>
  </g>
</svg>
'''


# ---------------------------------------------------------------- annealing
def annealing():
    W, H, D = 800, 320, 10
    N = 400
    LX, LW, TOP, AMP = 50, 600, 95, 150

    def energy(t):
        return (0.55 * math.sin(2 * math.pi * 2.3 * t + 0.4)
                + 0.35 * math.sin(2 * math.pi * 5.1 * t + 1.3)
                + 0.18 * math.sin(2 * math.pi * 9.7 * t)
                + 1.6 * (t - 0.7) ** 2)

    raw = [energy(i / (N - 1)) for i in range(N)]
    lo, hi = min(raw), max(raw)
    E = [(e - lo) / (hi - lo) for e in raw]
    gmin = E.index(0.0)

    def px(i):
        return LX + LW * i / (N - 1)

    def py(i):
        return TOP + AMP * (1 - E[i])  # SVG y grows downward: low energy = low on screen

    # Real simulated annealing on the curve; pick a seed that finds the global min.
    frames = None
    for seed in range(1000):
        rng = random.Random(seed)
        i = 15
        path = [i]
        T, steps = 1.0, 60
        alpha = (0.003 / T) ** (1 / steps)
        for _ in range(steps):
            for _ in range(25):
                reach = max(2, int(N * 0.35 * T))
                j = min(N - 1, max(0, i + rng.randint(-reach, reach)))
                dE = E[j] - E[i]
                if dE < 0 or rng.random() < math.exp(-dE / (T * 0.6)):
                    i = j
            path.append(i)
            T *= alpha
        # final greedy descent so the ball settles exactly in the basin bottom
        while True:
            nb = [k for k in (i - 1, i + 1) if 0 <= k < N]
            best = min(nb, key=lambda k: E[k])
            if E[best] >= E[i]:
                break
            i = best
        path.append(i)
        if i == gmin and len(set(path[:15])) > 8:
            frames = path
            break
    assert frames, "no seed found"

    # build hop keyframes (with an arc between consecutive positions)
    move_end = 7.4
    pts, keys = [], []
    n = len(frames) - 1
    for f in range(n):
        a, b = frames[f], frames[f + 1]
        t0 = move_end * f / n
        t1 = move_end * (f + 1) / n
        ax, ay, bx, by = px(a), py(a) - 11, px(b), py(b) - 11
        hop = min(70, abs(bx - ax) * 0.35 + 4)
        pts += [(ax, ay), ((ax + bx) / 2, max(80, min(ay, by) - hop))]
        keys += [t0, (t0 + t1) / 2]
    fx, fy = px(frames[-1]), py(frames[-1]) - 11
    pts += [(fx, fy), (fx, fy)]
    keys += [move_end, D]
    vals = ";".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    ktimes = ";".join(f"{k / D:.4f}" for k in keys)

    curve = " ".join(f"{px(i):.1f},{py(i):.1f}" for i in range(0, N, 2))
    area = f"{LX},{TOP + AMP + 30} {curve} {LX + LW},{TOP + AMP + 30}"
    m = move_end / D

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>
    <linearGradient id="land" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6366f1" stop-opacity="0.45"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></linearGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="#fbbf24" stop-opacity="0.9"/><stop offset="1" stop-color="#fbbf24" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  <text x="28" y="38" font-size="15" fill="#94a3b8">schedule_optimization / simulated_annealing.py</text>
  <text x="28" y="62" font-size="13" fill="#64748b">energy = 공강 + 하루 수업 편차   (15~18학점 제약)</text>

  <polygon points="{area}" fill="url(#land)"/>
  <polyline points="{curve}" fill="none" stroke="#a5b4fc" stroke-width="3" stroke-linejoin="round"/>

  <g opacity="0">{visible(move_end, D, D)}
    <circle cx="{fx:.1f}" cy="{fy + 11:.1f}" r="34" fill="url(#glow)"/>
    <text x="{fx:.1f}" y="{TOP + AMP + 26}" font-size="14" fill="#fde68a" text-anchor="middle">global minimum ✓ 공강 최소 시간표</text>
  </g>

  <circle r="10" fill="#f97316" stroke="#fff" stroke-width="2">
    <animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{ktimes}" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="fill" values="#ef4444;#f97316;#a78bfa;#38bdf8;#38bdf8" keyTimes="0;{m * 0.3:.4f};{m * 0.65:.4f};{m:.4f};1" dur="{D}s" repeatCount="indefinite"/>
  </circle>

  <!-- thermometer -->
  <text x="712" y="62" font-size="13" fill="#94a3b8" text-anchor="middle">T</text>
  <rect x="700" y="74" width="24" height="190" rx="12" fill="#1e293b" stroke="#334155"/>
  <rect x="705" y="79" width="14" height="180" rx="7" fill="#ef4444">
    <animate attributeName="height" values="180;12;12" keyTimes="0;{m:.4f};1" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="y" values="79;247;247" keyTimes="0;{m:.4f};1" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="fill" values="#ef4444;#a78bfa;#38bdf8;#38bdf8" keyTimes="0;{m * 0.5:.4f};{m:.4f};1" dur="{D}s" repeatCount="indefinite"/>
  </rect>
  <text x="745" y="88" font-size="12" fill="#fca5a5">hot</text>
  <text x="745" y="262" font-size="12" fill="#7dd3fc">cool</text>

  <text x="28" y="300" font-size="13" fill="#64748b">accept if ΔE &lt; 0  or  rand() &lt; e^(−ΔE / T)</text>
</svg>
'''


# ---------------------------------------------------------------- auction
def auction():
    W, H, D = 800, 320, 10
    first_bid, closing, strike = 1.2, 5.6, 7.0

    prices = [(0, "10,000"), (1.2, "11,000"), (2.0, "13,000"), (2.9, "15,000"),
              (3.8, "18,000"), (4.8, "21,000"), (6.1, "24,000")]
    timers = [(0, "24:00:00", "#94a3b8"), (1.2, "23:59:59", "#e2e8f0"), (2.4, "17:42:10", "#e2e8f0"),
              (3.6, "09:15:33", "#e2e8f0"), (closing, "02:59:12", "#f87171"), (6.4, "00:00:04", "#f87171"),
              (strike, "00:00:00", "#f87171")]
    states = [(0, "경매 대기", "#64748b"), (first_bid, "경매 진행 중", "#22c55e"),
              (closing, "마감 임박", "#ef4444"), (strike, "낙찰 완료", "#eab308")]
    bids = [(1.2, "+1,000"), (2.0, "+2,000"), (2.9, "+2,000"), (3.8, "+3,000"), (4.8, "+3,000"), (6.1, "+3,000")]

    def seq(items, render):
        out = []
        for k, item in enumerate(items):
            a = item[0]
            b = items[k + 1][0] if k + 1 < len(items) else D
            out.append(f'<g opacity="0">{visible(a, b, D)}{render(item)}</g>')
        return "".join(out)

    price_svg = seq(prices, lambda p: f'<text x="400" y="150" font-size="44" font-weight="800" fill="#fde68a">{p[1]}<tspan font-size="22" fill="#fcd34d"> 원</tspan></text>')
    timer_svg = seq(timers, lambda t: f'<text x="400" y="222" font-size="30" font-weight="700" fill="{t[2]}">{t[1]}</text>')
    state_svg = seq(states, lambda s: (
        f'<rect x="64" y="236" width="{text_width(s[1], 15) + 28:.0f}" height="30" rx="15" fill="{s[2]}" fill-opacity="0.18" stroke="{s[2]}"/>'
        f'<text x="78" y="256" font-size="15" fill="{s[2]}" font-family="{SANS}" font-weight="700">{s[1]}</text>'))

    bubbles = []
    for t, label in bids:
        k = kt(0, t / D, (t + 0.9) / D, 1)
        bubbles.append(f'''
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="{kt(0, t / D, (t + 0.1) / D, (t + 0.9) / D, 1)}" dur="{D}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -46;0 -46" keyTimes="{k}" dur="{D}s" repeatCount="indefinite"/>
    <rect x="640" y="140" width="120" height="34" rx="17" fill="#22c55e"/>
    <text x="700" y="163" font-size="16" font-weight="700" fill="#052e16" text-anchor="middle">{label}</text>
  </g>''')

    s0, s1 = strike - 0.5, strike
    gavel_k = kt(0, s0 / D, (s0 + 0.3) / D, s1 / D, (s1 + 0.25) / D, 1)
    stamp_k = kt(0, s1 / D, (s1 + 0.25) / D, (s1 + 0.4) / D, 1)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c1917"/><stop offset="1" stop-color="#3b1d0f"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  <text x="28" y="38" font-size="15" fill="#a8a29e">social-auction-platform / 이음 옥션</text>
  <text x="28" y="62" font-size="13" fill="#78716c">첫 입찰 순간부터 24시간 · SSE 실시간 현재가 · 경매별 입찰 큐</text>

  <!-- product card -->
  <rect x="50" y="84" width="300" height="196" rx="16" fill="#292524" stroke="#44403c"/>
  <g transform="translate(150 108)">
    <rect x="0" y="34" width="100" height="74" rx="6" fill="#f472b6"/>
    <rect x="-8" y="20" width="116" height="22" rx="5" fill="#ec4899"/>
    <rect x="42" y="20" width="16" height="88" fill="#fde68a"/>
    <path d="M50 20 C30 -6 14 8 44 20 M50 20 C70 -6 86 8 56 20" fill="none" stroke="#fde68a" stroke-width="6" stroke-linecap="round"/>
  </g>
  {state_svg}

  <text x="400" y="104" font-size="14" fill="#a8a29e" font-family="{SANS}">현재가</text>
  {price_svg}
  <text x="400" y="186" font-size="14" fill="#a8a29e" font-family="{SANS}">남은 시간</text>
  {timer_svg}
  <g opacity="0">{visible(0, first_bid, D)}<text x="400" y="256" font-size="13" fill="#78716c" font-family="{SANS}">첫 입찰을 기다리는 중…</text></g>
  {"".join(bubbles)}

  <!-- gavel -->
  <g transform="translate(700 250)">
    <g>
      <animateTransform attributeName="transform" type="rotate" values="0;0;-35;-35;8;0" keyTimes="{gavel_k}" dur="{D}s" repeatCount="indefinite"/>
      <rect x="-6" y="-80" width="12" height="70" rx="5" fill="#a16207" transform="rotate(-40)"/>
      <rect x="-30" y="-108" width="60" height="30" rx="7" fill="#ca8a04" transform="rotate(-40)"/>
    </g>
    <rect x="-40" y="0" width="80" height="14" rx="5" fill="#57534e"/>
  </g>
  <g transform="translate(200 165)">
    <g opacity="0">
      <animate attributeName="opacity" values="0;0;1;1;1" keyTimes="{stamp_k}" dur="{D}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="scale" values="0;0;1.3;1;1" keyTimes="{kt(0, s1 / D, (s1 + 0.25) / D, (s1 + 0.4) / D, 1)}" dur="{D}s" repeatCount="indefinite"/>
      <g transform="rotate(-12)">
        <rect x="-82" y="-36" width="164" height="72" rx="12" fill="#1c1917" fill-opacity="0.88" stroke="#ef4444" stroke-width="4"/>
        <text x="0" y="14" font-size="40" font-weight="900" fill="#ef4444" text-anchor="middle" font-family="{SANS}">낙찰!</text>
      </g>
    </g>
  </g>
</svg>
'''


# ---------------------------------------------------------------- status window (isekai)
def shadow_avatar(cx, cy, s):
    """Hooded hacker x 'shadow' rogue behind a laptop; local origin = face center."""
    rng = random.Random(11)
    glyphs = "01{}<>/;=#$"
    rain = []
    for k in range(9):
        x = -104 + k * 26 + rng.uniform(-4, 4)
        col = "".join(f'<tspan x="{x:.0f}" dy="15">{html.escape(rng.choice(glyphs))}</tspan>' for _ in range(22))
        d = rng.uniform(4, 7)
        rain.append(
            f'<text y="-120" font-size="12" fill="#a78bfa" opacity="{rng.uniform(0.18, 0.4):.2f}">{col}'
            f'<animateTransform attributeName="transform" type="translate" values="0 -150;0 0" dur="{d:.1f}s" '
            f'begin="-{rng.uniform(0, d):.1f}s" repeatCount="indefinite"/></text>')

    def eye(ex, flip, lit):
        pts = [(-12, -3), (4, -1), (11, 4), (-4, 3)]  # inner corner dips: glare
        d = " ".join(f"{ex + flip * x},{y}" for x, y in pts)
        if not lit:  # lost in the hood's shadow: only a faint outline
            return f'<polygon transform="translate(0 2)" points="{d}" fill="#1a0505" stroke="#7f1d1d" stroke-width="0.8" opacity="0.3"/>'
        return f'''
      <ellipse cx="{ex}" cy="3" rx="22" ry="12" fill="#ef4444" opacity="0.6" filter="url(#lightblur)">
        <animate attributeName="opacity" values="0.5;0.9;0.5" dur="2.4s" repeatCount="indefinite"/>
      </ellipse>
      <path d="M{ex - 26} 3 L{ex + 26} 3" stroke="#f87171" stroke-width="2.2" stroke-linecap="round" filter="url(#eyeglow)">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/>
      </path>
      <g transform="translate(0 2)"><g>
        <animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 0.1;1 1" keyTimes="0;0.94;0.97;1" dur="5s" repeatCount="indefinite"/>
        <polygon points="{d}" fill="#fca5a5" filter="url(#eyeglow)"/>
        <ellipse cx="{ex + flip * 1.5}" cy="1" rx="1.6" ry="3.2" fill="#450a0a"/>
      </g></g>'''

    flicker = "0.55;0.9;0.6;1;0.7;0.95;0.55"

    return f'''
  <defs>
    <radialGradient id="dark-aura"><stop offset="0" stop-color="#6d28d9" stop-opacity="0.5"/><stop offset="0.6" stop-color="#3b0764" stop-opacity="0.2"/><stop offset="1" stop-color="#3b0764" stop-opacity="0"/></radialGradient>
    <linearGradient id="hood-in" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#1c1426"/></linearGradient>
    <linearGradient id="screenlight" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#c4b5fd" stop-opacity="0.45"/><stop offset="1" stop-color="#c4b5fd" stop-opacity="0"/></linearGradient>
    <clipPath id="rain-area"><ellipse cy="32" rx="108" ry="118"/></clipPath>
    <filter id="lightblur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
    <filter id="eyeglow" x="-100%" y="-200%" width="300%" height="500%">
      <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-200%" y="-50%" width="500%" height="200%">
      <feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g transform="translate({cx} {cy}) scale({s})">
    <ellipse cy="20" rx="110" ry="130" fill="url(#dark-aura)"/>
    <g clip-path="url(#rain-area)">{"".join(rain)}</g>


    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -1.5;0 0" dur="3s" repeatCount="indefinite"/>
      <!-- long coat over a hoodie -->
      <path d="M-92 150 L-74 74 Q-64 54 -30 48 L30 48 Q64 54 74 74 L92 150 Z" fill="#07070d"/>
      <path d="M-28 48 L28 48 L32 150 L-32 150 Z" fill="#1a1726"/>
      <path d="M-28 48 L-36 150 M28 48 L36 150" stroke="#2a2238" stroke-width="2.5"/>
      <path d="M-40 40 L-50 64 L-26 52 Z M40 40 L50 64 L26 52 Z" fill="#14111f" stroke="#3b0764" stroke-width="1.2"/>

      <!-- hoodie hood (rounded) -->
      <path d="M-54 36 Q-64 -38 -12 -74 Q0 -80 12 -74 Q64 -38 54 36 Q40 54 0 56 Q-40 54 -54 36 Z" fill="#14121c" stroke="#2e1065" stroke-width="1.5"/>
      <path d="M-34 4 Q-36 -36 0 -44 Q36 -36 34 4 Q30 32 0 40 Q-30 32 -34 4 Z" fill="url(#hood-in)" stroke="#221c2e" stroke-width="5"/>
      <path d="M-30 -24 Q0 -46 30 -24 L24 -12 L16 -22 L8 -8 L0 -22 L-8 -8 L-16 -22 L-24 -12 Z" fill="#05050a"/>
      {eye(-14, 1, True)}{eye(14, -1, False)}
      <path d="M-32 10 Q0 4 32 10 L29 28 Q0 44 -29 28 Z" fill="#111018" stroke="#2e1065" stroke-width="1"/>
      <!-- hoodie strings -->
      <path d="M-12 44 Q-14 58 -16 72 M12 44 Q14 58 16 72" stroke="#d4d4d8" stroke-width="2" fill="none"/>
      <path d="M-44 -36 Q-30 -62 -8 -72" stroke="#4c1d95" stroke-width="2" fill="none" opacity="0.6"/>

      <!-- laptop glow lighting the face from below -->
      <path d="M-54 78 L54 78 L28 2 L-28 2 Z" fill="url(#screenlight)" filter="url(#lightblur)">
        <animate attributeName="opacity" values="{flicker}" dur="1.6s" repeatCount="indefinite"/>
      </path>
    </g>

    <!-- laptop (we see the back of the lid) -->
    <path d="M-62 78 L62 78 L68 140 L-68 140 Z" fill="#15131f" stroke="#4c1d95" stroke-width="1.5"/>
    <path d="M-74 140 L74 140 L78 148 L-78 148 Z" fill="#26223a"/>
    <text x="0" y="116" font-size="20" font-weight="700" fill="#c084fc" text-anchor="middle" filter="url(#softglow)">&lt;/&gt;
      <animate attributeName="opacity" values="{flicker}" dur="1.6s" repeatCount="indefinite"/>
    </text>
  </g>'''


def character():
    W, H = 800, 460
    OPEN = 0.2  # status window opens
    sy = 190

    talk = ["왜 안 되지…", "아 여기구나!", "버그는 어둠 속에서 벤다.", "OK, it works!"]
    TD = 8
    by = sy - 58
    bubbles = "".join(
        f'<g opacity="0">{visible(i * TD / len(talk), (i + 1) * TD / len(talk), TD)}'
        f'<text x="144" y="{by + 27}" font-size="15" fill="#0f172a" text-anchor="middle" font-family="{SANS}" font-weight="700">{t}</text></g>'
        for i, t in enumerate(talk))

    info = [("이름", "두두 (doodoo)", 310, 150), ("칭호", "「졸업을 앞둔 전생자」", 545, 150),
            ("직업", "백엔드 · 데이터 모험가", 310, 176), ("레벨", "Lv. 졸업 직전", 545, 176)]
    info_svg = "".join(
        f'<text x="{x}" y="{y}" font-size="14" font-family="{SANS}"><tspan fill="#67e8f9">{k}</tspan>'
        f'<tspan fill="#f1f5f9" font-weight="700" dx="10">{v}</tspan></text>' for k, v, x, y in info)

    stats = [("지구력", "STA", 100, "MAX", "#f97316"), ("게임", "GAME", 90, "90", "#22c55e"),
             ("영어 회화", "ENG", 70, "70", "#38bdf8"), ("일본어 회화", "JPN", 55, "55", "#f472b6"),
             ("혼잣말", "TALK", 95, "95", "#a78bfa")]
    BX, BW, Y0, DY = 440, 230, 200, 25
    rows = []
    for i, (label, abbr, val, shown, color) in enumerate(stats):
        y = Y0 + i * DY
        rows.append(f'''
    <text x="310" y="{y + 12}" font-size="14" fill="#e2e8f0" font-family="{SANS}">{label}</text>
    <text x="{BX - 10}" y="{y + 12}" font-size="11" fill="#64748b" text-anchor="end">{abbr}</text>
    <rect x="{BX}" y="{y}" width="{BW}" height="13" rx="3" fill="#0b1026" stroke="#1e3a5f"/>
    <rect x="{BX}" y="{y}" width="0" height="13" rx="3" fill="{color}">
      <animate attributeName="width" from="0" to="{BW * val / 100:.0f}" begin="{OPEN + 0.6 + i * 0.2:.2f}s" dur="0.9s" fill="freeze"/>
    </rect>
    <text x="{BX + BW + 12}" y="{y + 12}" font-size="13" font-weight="700" fill="{color}">{shown}</text>''')
    y = Y0 + len(stats) * DY
    rows.append(f'''
    <text x="310" y="{y + 12}" font-size="14" fill="#e2e8f0" font-family="{SANS}">약점</text>
    <text x="{BX - 10}" y="{y + 12}" font-size="11" fill="#64748b" text-anchor="end">WEAK</text>
    <text x="{BX}" y="{y + 12}" font-size="14" font-weight="700" fill="#f87171">??? <tspan fill="#94a3b8" font-weight="400" font-family="{SANS}">아직 발견되지 않음</tspan>
      <animate attributeName="x" values="{BX};{BX + 3};{BX - 2};{BX};{BX}" keyTimes="0;0.04;0.08;0.12;1" dur="2.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.3;1;1" keyTimes="0;0.05;0.1;1" dur="2.5s" repeatCount="indefinite"/>
    </text>''')

    skills = [("심연 탐색", "버그가 숨은 가장 깊은 곳까지 파고들어 끝내 찾아낸다"),
              ("그림자 행군", "아무도 모르게, 그러나 끝까지 나아간다"),
              ("불사의 심장", "몇 번을 쓰러져도 다시 일어나 끝내 완성한다")]
    sk = "".join(
        f'<text x="310" y="{386 + i * 21}" font-size="13" font-family="{SANS}">'
        f'<tspan fill="#fbbf24">◆</tspan> <tspan fill="#f1f5f9" font-weight="700">{name}</tspan>'
        f'<tspan fill="#94a3b8"> — {desc}</tspan></text>'
        for i, (name, desc) in enumerate(skills))

    def bracket(x, y, dx, dy):
        return f'<path d="M{x} {y + dy * 18} L{x} {y} L{x + dx * 18} {y}" fill="none" stroke="#a5f3fc" stroke-width="3"/>'

    WX, WY, WW, WH = 16, 74, W - 32, H - 90
    MCY = WY + WH / 2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <filter id="glow" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="#070b1d"/>

  <!-- system toast -->
  <g opacity="0">
    {once("opacity", 0, 1, OPEN + 1.8, 0.4)}
    <animateTransform attributeName="transform" type="translate" from="0 -20" to="0 0" begin="{OPEN + 1.8}s" dur="0.4s" fill="freeze"/>
    <rect x="120" y="16" width="560" height="38" rx="8" fill="#0e7490" fill-opacity="0.35" stroke="#67e8f9"/>
    <text x="400" y="40" font-size="14" fill="#cffafe" text-anchor="middle" font-family="{SANS}">[시스템] <tspan fill="#fde68a" font-weight="700">상태창</tspan>이 활성화되었습니다.</text>
  </g>

  <!-- status window: unfolds vertically from its center -->
  <g transform="translate(0 {MCY})"><g>
    <animateTransform attributeName="transform" type="scale" values="1 0.02;1 0.02;1 1" keyTimes="0;0.3;1" begin="{OPEN}s" dur="0.5s" fill="freeze"/>
    <g transform="translate(0 {-MCY})">
    <rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="10" fill="#0ea5e9" fill-opacity="0.07" stroke="#67e8f9" stroke-width="1.5" filter="url(#glow)"/>
    {bracket(WX + 6, WY + 6, 1, 1)}{bracket(WX + WW - 6, WY + 6, -1, 1)}
    {bracket(WX + 6, WY + WH - 6, 1, -1)}{bracket(WX + WW - 6, WY + WH - 6, -1, -1)}
    <text x="44" y="110" font-size="16" font-weight="700" fill="#a5f3fc" font-family="{SANS}" filter="url(#glow)">◆ 상태창</text>
    <text x="{W - 44}" y="110" font-size="12" fill="#22d3ee" text-anchor="end" opacity="0.7">STATUS WINDOW</text>
    <line x1="40" y1="122" x2="{W - 40}" y2="122" stroke="#67e8f9" stroke-opacity="0.35"/>

    <g opacity="0">{once("opacity", 0, 1, OPEN + 0.5, 0.4)}
      <rect x="34" y="{by}" width="220" height="40" rx="12" fill="#f8fafc"/>
      <path d="M136 {by + 39} L144 {by + 52} L152 {by + 39} Z" fill="#f8fafc"/>
      {bubbles}
      {shadow_avatar(144, 272, 0.82)}
      <text x="144" y="424" font-size="13" fill="#94a3b8" text-anchor="middle" font-family="{SANS}">취미: 게임 · 영어/일본어 회화</text>

      <line x1="282" y1="136" x2="282" y2="{WY + WH - 20}" stroke="#1e3a5f" stroke-dasharray="4 4"/>
      {info_svg}
      {"".join(rows)}
      <text x="310" y="364" font-size="13" font-weight="700" fill="#67e8f9" font-family="{SANS}">고유 스킬</text>
      {sk}
    </g>
    </g>
  </g></g>
</svg>
'''


# ---------------------------------------------------------------- slang funnel
def funnel():
    W, H, D = 800, 360, 10
    CX, TOPY, BOTY, TOPHW, BOTHW = 290, 80, 255, 170, 40
    gates = [(135, "① 빈도 · 불용어 필터", "6,423"), (195, "② Reddit 문맥 × LLM 판정", "3,293"),
             (250, "③ 사람 검수", "384")]

    def hw(y):
        return TOPHW - (TOPHW - BOTHW) * (y - TOPY) / (BOTY - TOPY)

    poly = f"{CX - TOPHW},{TOPY} {CX + TOPHW},{TOPY} {CX + BOTHW},{BOTY} {CX - BOTHW},{BOTY}"
    gate_svg = []
    for gy, label, num in gates:
        gate_svg.append(
            f'<line x1="{CX - hw(gy):.0f}" y1="{gy}" x2="{CX + hw(gy):.0f}" y2="{gy}" stroke="#fbbf24" stroke-width="2" stroke-dasharray="6 5" opacity="0.7"/>'
            f'<line x1="{CX + hw(gy) + 6:.0f}" y1="{gy}" x2="500" y2="{gy}" stroke="#475569" stroke-dasharray="2 4"/>'
            f'<text x="510" y="{gy - 4}" font-size="13" fill="#cbd5e1" font-family="{SANS}">{label}</text>'
            f'<text x="{W - 36}" y="{gy - 2}" font-size="22" font-weight="800" fill="#fde68a" text-anchor="end">{num}</text>')

    # anonymous candidates: most get filtered out at some gate
    rng = random.Random(3)
    dots = []
    fall = 1.7
    for _ in range(28):
        s = rng.uniform(0, D - fall - 0.4)
        x0 = CX + rng.uniform(-TOPHW + 15, TOPHW - 15)
        r = rng.random()
        stop = 1 if r < 0.35 else 2 if r < 0.75 else 3 if r < 0.92 else 4  # gate index, 4 = passes
        ys = [TOPY] + [g[0] for g in gates]
        ys = ys[:stop + 1]
        pts = [(x0, TOPY - 10)] + [(CX + (x0 - CX) * hw(y) / TOPHW, y) for y in ys[1:]]
        ts = [s + fall * (y - TOPY) / (BOTY - TOPY) for y in [TOPY] + ys[1:]]
        end = ts[-1]
        if stop < 4:  # rejected: pop sideways and fade
            side = -1 if x0 < CX else 1
            pts.append((pts[-1][0] + side * 30, pts[-1][1] - 12))
        else:
            pts.append((CX, BOTY + 20))
        ts.append(end + 0.35)
        vals = ";".join(f"{x:.0f} {y:.0f}" for x, y in [pts[0]] + pts + [pts[-1]])
        keys = kt(0, *(t / D for t in ts), 1)
        fade = kt(0, s / D, (s + 0.05) / D, end / D, (end + 0.35) / D, 1)
        dots.append(
            f'<circle r="4" fill="#94a3b8" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{keys}" dur="{D}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;0.9;0.9;0;0" keyTimes="{fade}" dur="{D}s" repeatCount="indefinite"/>'
            f'</circle>')

    # named words: real examples from the dataset
    approved = [("goat", 0.6), ("sick", 3.4), ("dm", 5.0), ("gif", 6.4)]
    chips, slot_x = [], 168
    TRAY_Y = 292
    for word, s in approved:
        w = len(word) * 9 + 22
        tx = slot_x
        slot_x += w + 10
        t1, t2 = s + fall, s + fall + 0.5
        vals = f"{CX - w / 2:.0f} {TOPY - 26};{CX - w / 2:.0f} {TOPY - 26};{CX - w / 2:.0f} {BOTY - 12};{tx} {TRAY_Y};{tx} {TRAY_Y}"
        chips.append(
            f'<g opacity="0">{visible(s, D, D)}'
            f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt(0, s / D, t1 / D, t2 / D, 1)}" dur="{D}s" repeatCount="indefinite"/>'
            f'<rect width="{w}" height="24" rx="12" fill="#22c55e"/>'
            f'<text x="{w / 2}" y="17" font-size="14" font-weight="700" fill="#052e16" text-anchor="middle">{word}</text></g>')

    # "cap": every sampled context was market cap / salary cap -> dropped by the LLM gate
    cs = 1.9
    cw = 3 * 9 + 22
    g2 = gates[1][0]
    tg = cs + fall * (g2 - TOPY) / (BOTY - TOPY)
    cap_vals = (f"{CX - cw / 2:.0f} {TOPY - 26};{CX - cw / 2:.0f} {TOPY - 26};{CX - cw / 2:.0f} {g2 - 24};"
                f"{CX - cw / 2 - 20:.0f} {g2 - 40};{70} {g2 + 40};{70} {g2 + 40}")
    cap_k = kt(0, cs / D, tg / D, (tg + 0.15) / D, (tg + 0.8) / D, 1)
    cap = f'''
  <g opacity="0">{visible(cs, tg + 3.2, D)}
    <animateTransform attributeName="transform" type="translate" values="{cap_vals}" keyTimes="{cap_k}" dur="{D}s" repeatCount="indefinite"/>
    <rect width="{cw}" height="24" rx="12" fill="#ef4444"/>
    <text x="{cw / 2}" y="17" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">cap</text>
  </g>
  <g opacity="0">{visible(tg + 0.8, tg + 3.2, D)}
    <text x="24" y="{g2 + 84}" font-size="12" fill="#fca5a5" font-family="{SANS}">문맥 60개 전부</text>
    <text x="24" y="{g2 + 100}" font-size="12" fill="#fca5a5">"market cap" ✗</text>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#052e2b"/><stop offset="1" stop-color="#0f172a"/></linearGradient>
    <linearGradient id="fn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2dd4bf" stop-opacity="0.08"/><stop offset="1" stop-color="#2dd4bf" stop-opacity="0.3"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  <text x="28" y="36" font-size="15" fill="#99f6e4">english-inssa-data-pipeline / 졸업 작품</text>
  <text x="28" y="58" font-size="13" fill="#5eead4" opacity="0.7" font-family="{SANS}">사전에만 있는 슬랭 말고, 진짜 쓰이는 슬랭만 골라내기</text>

  <polygon points="{poly}" fill="url(#fn)" stroke="#2dd4bf" stroke-width="2" stroke-linejoin="round"/>
  <text x="510" y="{TOPY + 4}" font-size="12" fill="#64748b" font-family="{SANS}">Wiktionary 슬랭 후보 + Reddit 댓글 2개월치</text>
  {"".join(gate_svg)}
  {"".join(dots)}

  <rect x="150" y="{TRAY_Y - 8}" width="290" height="40" rx="10" fill="#0f172a" stroke="#22c55e" stroke-dasharray="4 3"/>
  <text x="450" y="{TRAY_Y + 18}" font-size="12" fill="#86efac">service dataset</text>
  {"".join(chips)}
  {cap}

  <text x="28" y="{H - 14}" font-size="12" fill="#5eead4" opacity="0.75">Reservoir Sampling · gpt-4.1-nano (temp 0, JSON schema) · pytest 43 · CI 품질 게이트</text>
</svg>
'''


for name, fn in [("header.svg", header), ("character.svg", character), ("funnel.svg", funnel),
                 ("annealing.svg", annealing), ("auction.svg", auction)]:
    (OUT / name).write_text(fn(), encoding="utf-8")
    print("wrote", OUT / name)
