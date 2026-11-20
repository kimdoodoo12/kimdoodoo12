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
      <text x="{CX}" y="198" font-size="17" font-weight="700" fill="#e9d5ff" letter-spacing="6" filter="url(#glow)">THE DEVELOPER IN SHADOW</text>
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

    talk = ["I am… ACID.", "코드 속에 숨어 코드를 사냥하는 자…",
            "버그가 시작된다.", "오늘 밤은… 콘솔이 붉군."]
    TD = 2 * len(talk)
    by = sy - 58
    bubbles = "".join(
        f'<g opacity="0">{visible(i * TD / len(talk), (i + 1) * TD / len(talk), TD)}'
        f'<text x="144" y="{by + 26}" font-size="{min(15, 212 / text_width(t, 1)):.1f}" fill="#0f172a" text-anchor="middle" font-family="{SANS}" font-weight="700">{t}</text></g>'
        for i, t in enumerate(talk))

    info = [("이름", "두두 (doodoo)", 310, 150), ("칭호", "「졸업을 앞둔 전생자」", 545, 150),
            ("직업", "백엔드 · 데이터 모험가", 310, 176), ("레벨", "Lv. 졸업 직전 (25)", 545, 176)]
    info_svg = "".join(
        f'<text x="{x}" y="{y}" font-size="14" font-family="{SANS}"><tspan fill="#67e8f9">{k}</tspan>'
        f'<tspan fill="#f1f5f9" font-weight="700" dx="10">{v}</tspan></text>' for k, v, x, y in info)

    stats = [("체력", "HP", 100, "MAX", "#f97316"), ("집중력", "FOC", 70, "70", "#22c55e"),
             ("디버깅", "DBG", 80, "80", "#a78bfa"), ("학습력", "LRN", 80, "80", "#38bdf8"),
             ("다국어", "POLY", 60, "60", "#f472b6")]
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
    <text x="{BX}" y="{y + 12}" font-size="14" font-weight="700" fill="#f87171">??? <tspan fill="#94a3b8" font-weight="400">404: Weakness Not Found</tspan>
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
      <rect x="26" y="{by}" width="236" height="40" rx="12" fill="#f8fafc"/>
      <path d="M136 {by + 39} L144 {by + 52} L152 {by + 39} Z" fill="#f8fafc"/>
      {bubbles}
      {shadow_avatar(144, 272, 0.82)}

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



for name, fn in [("header.svg", header), ("character.svg", character)]:
    (OUT / name).write_text(fn(), encoding="utf-8")
    print("wrote", OUT / name)

