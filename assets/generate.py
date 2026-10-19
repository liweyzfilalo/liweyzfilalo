"""Génère les SVG du README de profil (bannière, cartes projets, pied de page) en clair et sombre."""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', 'SF Mono', Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0b0f0d", bg2="#101714", card="#0f1512", border="#1f2b25", text="#ecf3ef",
                 muted="#93a39a", faint="#5b6b62", accent="#5fd38d", dot="#1b2621", chip="#16201b"),
    "light": dict(bg="#f7faf8", bg2="#eef4f0", card="#ffffff", border="#dbe5df", text="#0f1a14",
                  muted="#4f5f56", faint="#8a9990", accent="#1f7a4d", dot="#dfe8e2", chip="#f0f5f2"),
}


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------------- bannière
def header(t, mode):
    a = t["accent"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Thomas Delhay, développeur">
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{t['dot']}"/></pattern>
  <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="60"/></filter>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="{t['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{t['bg']}"/></linearGradient>
  <clipPath id="r"><rect width="1200" height="320" rx="22"/></clipPath>
  <style>
    .b1,.b2,.b3{{transform-box:fill-box;transform-origin:center}}
    .b1{{animation:m1 14s ease-in-out infinite alternate}}
    .b2{{animation:m2 18s ease-in-out infinite alternate}}
    .b3{{animation:m3 16s ease-in-out infinite alternate}}
    @keyframes m1{{to{{transform:translate(160px,40px) scale(1.15)}}}}
    @keyframes m2{{to{{transform:translate(-180px,-30px) scale(.9)}}}}
    @keyframes m3{{to{{transform:translate(90px,-60px) scale(1.2)}}}}
    .in{{animation:in 1s cubic-bezier(.2,.7,.2,1)}}
    .d1{{animation-duration:1.3s}} .d2{{animation-duration:1.7s}} .d3{{animation-duration:2.1s}}
    @keyframes in{{from{{opacity:0;transform:translateY(14px)}}}}
    .cur{{animation:blink 1.1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .ping{{transform-origin:center;transform-box:fill-box;animation:ping 2.2s ease-out infinite}}
    @keyframes ping{{from{{transform:scale(1);opacity:.7}}to{{transform:scale(2.8);opacity:0}}}}
  </style>
</defs>
<g clip-path="url(#r)">
  <rect width="1200" height="320" fill="{t['bg']}"/>
  <rect width="1200" height="320" fill="url(#dots)"/>
  <g filter="url(#blur)">
    <circle class="b1" cx="230" cy="60" r="150" fill="{a}" fill-opacity="{.34 if mode == 'dark' else .22}"/>
    <circle class="b2" cx="1000" cy="250" r="170" fill="#3b82f6" fill-opacity="{.30 if mode == 'dark' else .18}"/>
    <circle class="b3" cx="720" cy="30" r="120" fill="#a78bfa" fill-opacity="{.26 if mode == 'dark' else .16}"/>
  </g>
  <rect width="1200" height="320" fill="url(#fade)"/>
  <rect x=".5" y=".5" width="1199" height="319" rx="21.5" fill="none" stroke="{t['border']}"/>
</g>
<g font-family="{FONT}">
  <g class="in">
    <rect x="80" y="78" width="252" height="32" rx="16" fill="{t['card']}" stroke="{t['border']}"/>
    <circle class="ping" cx="101" cy="94" r="5" fill="{a}"/>
    <circle cx="101" cy="94" r="5" fill="{a}"/>
    <text x="115" y="99.5" font-size="14" font-weight="600" fill="{t['muted']}">En ce moment : Velora Musique</text>
  </g>
  <text class="in d1" x="76" y="186" font-size="74" font-weight="800" letter-spacing="-2.5" fill="{t['text']}">Thomas Delhay</text>
  <text class="in d2" x="80" y="228" font-size="24" font-weight="500" fill="{t['muted']}">Développeur · <tspan fill="{a}" font-weight="700">BTS SIO option SLAM</tspan></text>
  <g class="in d3" font-family="{MONO}" font-size="16" fill="{t['faint']}">
    <text x="80" y="268"><tspan fill="{a}">❯</tspan> web · windows · android · de l'interface au serveur<tspan class="cur" fill="{a}"> ▍</tspan></text>
  </g>
</g>
</svg>"""


# ---------------------------------------------------------------- cartes projets
ICONS = {
    # tracés 24x24 (style trait)
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="14" y1="4" x2="10" y2="20"/>',
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9z"/><path d="M12 12v6"/><path d="m9 15 3-3 3 3"/>',
}

PROJECTS = [
    dict(slug="musique", icon="music", color="#3b82f6", title="Velora Musique", tag="EN LIGNE",
         lines=["Streaming musical complet : lecteur HLS,", "recommandations et radio automatique."],
         chips=["React", "Fastify", "Supabase", "Electron"], link="velora-musique.vercel.app"),
    dict(slug="protect", icon="shield", color="#f59e0b", title="Velora Protect", tag="EN LIGNE",
         lines=["Secrets, failles, sauvegardes vérifiées et", "preuve d'antériorité (RFC 3161 + Bitcoin)."],
         chips=["Python", "Sécurité", "OSV.dev", "CLI"], link="velora-protect.vercel.app"),
    dict(slug="ide", icon="code", color="#a78bfa", title="Velora IDE", tag="BUREAU",
         lines=["Éditeur de code inspiré de Cursor,", "avec panneau IA intégré."],
         chips=["Electron", "React", "TypeScript", "Monaco"], link="appli Windows"),
    dict(slug="drive", icon="cloud", color="#22d3ee", title="Velora Drive", tag="EN LIGNE",
         lines=["Un drive personnel façon Google Drive :", "comptes, espaces privés, partage."],
         chips=["Node.js", "Supabase", "Netlify"], link="velora-drive.netlify.app"),
]


def card(p, t, mode):
    c = p["color"]
    W, H = 580, 230
    chips, x = [], 32
    for ch in p["chips"]:
        w = 18 + len(ch) * 7.6
        chips.append(f'<rect x="{x}" y="166" width="{w:.0f}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="183.5" text-anchor="middle" font-size="12.5" font-weight="600" fill="{t["muted"]}">{escape(ch)}</text>')
        x += w + 8
    desc = "".join(f'<text x="32" y="{118 + i * 24}" font-size="16" fill="{t["muted"]}">{escape(l)}</text>' for i, l in enumerate(p["lines"]))
    tagw = 16 + len(p["tag"]) * 7.4
    glow = .30 if mode == "dark" else .16
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p['title'])}">
<defs>
  <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{c}" stop-opacity="{glow}"/><stop offset=".6" stop-color="{c}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{c}" stop-opacity="0"/><stop offset=".5" stop-color="{c}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <style>
    .sweep{{animation:sw 6s ease-in-out infinite}}
    @keyframes sw{{0%{{transform:translateX(-{W}px)}}60%,100%{{transform:translateX({W}px)}}}}
    .pulse{{animation:pu 3.5s ease-in-out infinite alternate}}
    @keyframes pu{{from{{opacity:.55}}to{{opacity:1}}}}
  </style>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{t['card']}"/>
  <rect class="pulse" width="{W}" height="{H}" fill="url(#glow)"/>
  <rect class="sweep" y="0" width="{W}" height="2" fill="url(#edge)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{t['border']}"/>
<g font-family="{FONT}">
  <rect x="32" y="30" width="44" height="44" rx="12" fill="{c}" fill-opacity="{.16 if mode == 'dark' else .12}"/>
  <g transform="translate(42 40)" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[p['icon']]}</g>
  <text x="92" y="60" font-size="23" font-weight="750" letter-spacing="-.4" fill="{t['text']}">{escape(p['title'])}</text>
  <rect x="{W - 32 - tagw:.0f}" y="38" width="{tagw:.0f}" height="24" rx="12" fill="{c}" fill-opacity=".14"/>
  <text x="{W - 32 - tagw / 2:.0f}" y="54" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1" fill="{c}">{p['tag']}</text>
  {desc}
  {''.join(chips)}
  <text x="{W - 32}" y="183.5" text-anchor="end" font-size="13" font-weight="600" fill="{c}">{escape(p['link'])} →</text>
</g>
</svg>"""


# ---------------------------------------------------------------- séparateur / pied de page
def footer(t, mode):
    a = t["accent"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-label="Merci de votre visite">
<defs>
  <linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="#3b82f6"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  <style>
    .wv{{animation:wv 9s linear infinite}} .wv2{{animation:wv 13s linear infinite reverse}}
    @keyframes wv{{to{{transform:translateX(-600px)}}}}
  </style>
</defs>
<g opacity="{.9 if mode == 'dark' else .8}">
  <path class="wv" d="M0 70 Q150 40 300 70 T600 70 T900 70 T1200 70 T1500 70 T1800 70 V120 H0 Z" fill="url(#w)" opacity=".35"/>
  <path class="wv2" d="M0 85 Q150 60 300 85 T600 85 T900 85 T1200 85 T1500 85 T1800 85 V120 H0 Z" fill="url(#w)" opacity=".55"/>
</g>
<text x="600" y="38" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="600" fill="{t['muted']}">Merci de votre visite ✦</text>
</svg>"""


for mode, t in THEMES.items():
    write(f"header-{mode}.svg", header(t, mode))
    write(f"footer-{mode}.svg", footer(t, mode))
    for p in PROJECTS:
        write(f"{p['slug']}-{mode}.svg", card(p, t, mode))
print("ok", sorted(os.listdir(OUT)))
