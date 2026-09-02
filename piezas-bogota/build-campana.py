#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Campaña de lanzamiento · Oktoberfest Artesanal Bogotá 2026.

Genera:
  · Historia LANZAMIENTO (1080×1920)
  · Historia BOLETAS      (1080×1920)   — precios SIN servicio + nota *
  · Carrusel (4× 1080×1350):
      1) Lanzamiento   2) Boletería (precios sin servicio + nota *)
      3) Experiencias  4) Llamado a la acción (compra en Tuboleta)

Todo sobre la imagen madre del Save the Date (paleta ocaso, logo Oktoberfest con
contorno oficial). Regla del cliente: NO mostrar el valor del servicio; poner
siempre una nota al pie: «*Los valores no incluyen el servicio de Tuboleta».
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "campana-lanzamiento"
OUT.mkdir(parents=True, exist_ok=True)
BUILD = OUT / ".build"; BUILD.mkdir(exist_ok=True)

PULEP = "IZP513"
NOTA = "*Los valores no incluyen el servicio de Tuboleta."
FEATS = ["+40 Cervecerías", "+200 Cervezas por probar", "Artistas en vivo",
         "Gastronomía", "Experiencias inmersivas"]
ENTRADAS = [
    ("Cervecero Pro", [("Preventa", "$54.900"), ("Etapa 1", "$59.900"), ("Etapa 2", "$74.900"),
                       ("Etapa 3", "$86.900"), ("Etapa 4", "$99.900"), ("Etapa 5", "$112.900"),
                       ("Precio Full", "$124.900")]),
    ("Cervecero Pro + Jarro", [("Preventa", "$122.900"), ("Precio Full", "$192.900")]),
    ("De Parche", [("Preventa", "$36.900"), ("Etapa 1", "$46.900"),
                   ("Etapa 2", "$56.900"), ("Precio Full", "$66.900")]),
]


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


BANK = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/fotos-bogota")
HERO = du(REPO_AS / "hero-sunset.jpg", "image/jpeg")               # imagen madre atardecer (portada)
PH_BEER = du(BANK / "FOTOS LA TOMA-168.jpg", "image/jpeg")          # vaso de cerveza sirviéndose
PH_CROWD = du(BANK / "FOTOS LA TOMA-152.jpg", "image/jpeg")         # multitud
PH_STAGE = du(BANK / "FOTOS LA TOMA-364.jpg", "image/jpeg")         # escenario noche
PH_AERIAL = du(BANK / "FOTOS LA TOMA-098.jpg", "image/jpeg")        # aérea festival
PH_TOAST = du(BANK / "FOTOS LA TOMA-199.jpg", "image/jpeg")         # brindis con cervezas
OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
TUBO = du(WORK_AS / "tuboleta-blanco.png", "image/png")
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")


def find_chrome():
    p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(p).exists():
        return p
    raise SystemExit("No Chrome")


CHROME = find_chrome()


def base_css(w, h, objpos, photo_h, fade, dark):
    fade_css = ("""-webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 8%,#000 22%);
      mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 8%,#000 22%);""" if fade else "")
    if dark:  # boletería: fondo muy oscuro para leer la tabla
        veil = ("linear-gradient(180deg,rgba(14,11,7,.90),rgba(14,11,7,.94) 40%,rgba(14,11,7,.97))")
    else:
        top = ("rgba(20,17,11,.88) 0%,rgba(20,17,11,.5) 20%,rgba(20,17,11,.08) 36%,transparent 48%"
               if fade else
               "rgba(20,17,11,.86) 0%,rgba(20,17,11,.64) 24%,rgba(20,17,11,.34) 38%,rgba(20,17,11,.10) 50%,transparent 62%")
        veil = (f"linear-gradient(180deg,{top}),linear-gradient(0deg,rgba(10,6,2,.94) 0%,"
                "rgba(10,6,2,.82) 20%,rgba(10,6,2,.46) 42%,transparent 60%)")
    return f"""
{FONTS_CSS}
:root{{--night:#14110B;--cream:#EEE7D6;--soft:#B7AC93;--gold:#E9A72C;--ember:#E2611A}}
*{{box-sizing:border-box;margin:0}} html,body{{background:#000}}
body{{font-family:'Barlow',system-ui,sans-serif;-webkit-font-smoothing:antialiased}} img{{display:block}}
.bc{{font-family:'Barlow Condensed',Barlow,sans-serif}}
.stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:var(--night);color:var(--cream)}}
.photo{{position:absolute;inset:auto 0 0 0;height:{photo_h}px;{fade_css}}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{objpos};filter:saturate(1.1) contrast(1.03) brightness(1.1)}}
.glow{{position:absolute;inset:0;background:radial-gradient(58% 26% at 42% 40%,rgba(244,196,90,.20),transparent 72%)}}
.veil{{position:absolute;inset:0;background:{veil}}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center}}
.sello{{filter:drop-shadow(0 6px 22px rgba(0,0,0,.6))}}
.brand{{filter:drop-shadow(0 12px 30px rgba(0,0,0,.45))}}
.city{{font-weight:700;line-height:.9;letter-spacing:.085em;text-transform:uppercase;color:var(--gold);text-shadow:0 6px 34px rgba(0,0,0,.6)}}
.city span{{color:var(--cream)}}
.kicker{{font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.85)}}
.when{{font-weight:700;line-height:1;letter-spacing:.05em;text-transform:uppercase;color:var(--cream);text-shadow:0 5px 30px rgba(0,0,0,.85)}}
.place{{font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.9)}}
.pill{{display:inline-flex;align-items:center;background:var(--gold);color:#2A1B06;border-radius:999px;box-shadow:0 22px 54px -18px rgba(233,167,44,.95)}}
.pill span{{font-weight:700;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}}
.tk{{display:flex;align-items:center;justify-content:center}}
.tk .lbl{{font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--cream)}}
.tk .web{{font-weight:700;color:var(--cream)}}
.handle{{font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--soft)}}
.nota{{position:absolute;left:0;right:0;z-index:4;text-align:center;color:var(--soft);font-weight:600;letter-spacing:.04em}}
.pulep{{position:absolute;z-index:4;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--cream);text-shadow:0 2px 12px rgba(0,0,0,.9)}}
.feats-list{{display:flex;flex-direction:column;gap:0;width:100%;max-width:780px}}
.feats-list .row{{display:flex;align-items:center;gap:18px;padding:20px 6px;border-bottom:1px solid rgba(233,167,44,.28)}}
.feats-list .row:last-child{{border-bottom:0}}
.feats-list .dot{{width:14px;height:14px;background:var(--gold);transform:rotate(45deg);border-radius:2px;flex:0 0 auto}}
.feats-list .txt{{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--cream);text-align:left}}
.cats{{display:flex;flex-direction:column;gap:10px;width:100%;max-width:920px}}
.cat{{background:rgba(20,17,11,.55);border:1px solid rgba(233,167,44,.4);border-radius:14px;overflow:hidden}}
.cat-h{{font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--cream);background:rgba(233,167,44,.16);padding:11px 26px}}
.cat table{{width:100%;border-collapse:collapse}}
.cat td{{padding:9px 26px;border-top:1px solid rgba(255,255,255,.07);text-align:left}}
.cat td.et{{color:var(--cream);font-weight:600}}
.cat td.pr{{text-align:right;font-weight:700;color:var(--gold);font-family:'Barlow Condensed',sans-serif}}
"""


def stage(w, h, inner, objpos="72% center", photo_h=None, fade=False, dark=False,
          nota=False, extra="", photo=HERO):
    photo_h = photo_h or h
    corner = round(min(w, h) * 0.035)
    cfs = max(12, round(min(w, h) * 0.017))
    nota_html = f'<div class="nota" style="bottom:{round(min(w,h)*0.03)}px;font-size:{cfs}px">{NOTA}</div>' if nota else ""
    return f"""<!doctype html><meta charset="utf-8"><style>{base_css(w,h,objpos,photo_h,fade,dark)}
.pulep{{left:{corner}px;bottom:{corner}px;font-size:{cfs}px}}
{extra}</style>
<div class="stage">
  <div class="photo"><img src="{photo}" alt=""></div>
  <div class="glow"></div><div class="veil"></div>
  {inner}
  {nota_html}
  <div class="pulep">PULEP {PULEP}</div>
</div>"""


def mast(scale=1.0):
    return (f'<img class="sello" src="{LATOMA}" style="height:{round(60*scale)}px">'
            f'<img class="brand" src="{OKT}" style="width:{round(560*scale)}px;margin-top:{round(16*scale)}px">'
            f'<div class="city bc" style="font-size:{round(96*scale)}px;margin-top:{round(12*scale)}px">Bogotá <span>2026</span></div>')


def tk_lockup(sz=26):
    return (f'<div class="tk" style="gap:{round(sz*.5)}px"><span class="lbl bc" style="font-size:{sz}px">en</span>'
            f'<img src="{TUBO}" style="height:{round(sz*1.25)}px;filter:drop-shadow(0 3px 12px rgba(0,0,0,.7))">'
            f'<span class="web bc" style="font-size:{sz}px">tuboleta.com</span></div>')


def entradas_html():
    cards = []
    for name, rows in ENTRADAS:
        trs = "".join(f'<tr><td class="et bc" style="font-size:32px">{et}</td>'
                      f'<td class="pr" style="font-size:40px">{pr}<span style="color:var(--soft);font-size:22px">*</span></td></tr>'
                      for et, pr in rows)
        cards.append(f'<div class="cat"><div class="cat-h bc" style="font-size:33px">{name}</div>'
                     f'<table>{trs}</table></div>')
    return "".join(cards)


# ── Definición de piezas ─────────────────────────────────────────────────────
def slide_lanzamiento(w, h, story=False):
    s = 1.15 if story else 1.0
    pt = 190 if story else 70
    inner = f"""<div class="in" style="padding:{pt}px 80px {230 if story else 70}px">
      <div style="display:flex;flex-direction:column;align-items:center">{mast(1.25 if story else 1.0)}</div>
      <div style="margin-top:auto;display:flex;flex-direction:column;align-items:center;gap:{round(14*s)}px">
        <div class="kicker bc" style="font-size:{round(34*s)}px">¡Boletas a la venta!</div>
        <div class="when bc" style="font-size:{round(64*s)}px">Sábado 24 de octubre</div>
        <div class="place bc" style="font-size:{round(34*s)}px">Centro de Eventos CESAP · Bogotá</div>
        <div class="pill bc" style="padding:{round(18*s)}px {round(44*s)}px;margin-top:{round(10*s)}px"><span style="font-size:{round(30*s)}px">Boletas desde $54.900*</span></div>
        {tk_lockup(round(26*s))}
        <div class="handle bc" style="font-size:{round(20*s)}px;margin-top:{round(6*s)}px">@oktoberfestartesanalbog</div>
      </div></div>"""
    return stage(w, h, inner, objpos="72% center" if not story else "55% center",
                 photo_h=1400 if story else None, fade=story, nota=True)


def slide_boleteria(w, h, story=False):
    pt = 150 if story else 46
    head = '<div class="kicker bc" style="font-size:36px;color:var(--gold);letter-spacing:.26em">Boletas a la venta</div>'
    foot = (f"""<div style="margin-top:auto;display:flex;flex-direction:column;align-items:center;gap:16px;padding-bottom:20px">
        <div class="pill bc" style="padding:18px 50px"><span style="font-size:30px">Compra en tuboleta.com</span></div>
        {tk_lockup(26)}
        <div class="handle bc" style="font-size:20px">@oktoberfestartesanalbog</div>
      </div>""" if story else "")
    inner = f"""<div class="in" style="padding:{pt}px 66px {150 if story else 74}px;justify-content:flex-start">
      <img class="brand" src="{OKT}" style="width:{240 if not story else 300}px">
      <div style="margin-top:{8 if not story else 14}px">{head}</div>
      <div class="cats" style="margin-top:{16 if not story else 26}px">{entradas_html()}</div>
      {foot}
    </div>"""
    return stage(w, h, inner, objpos="center 50%", photo_h=1400 if story else None,
                 fade=False, dark=True, nota=True, photo=PH_STAGE)


def slide_features(w, h):
    rows = "".join(f'<div class="row"><div class="dot"></div><div class="txt bc" style="font-size:44px">{x}</div></div>'
                   for x in FEATS)
    inner = f"""<div class="in" style="padding:96px 90px 120px;justify-content:center;gap:40px">
      <img class="brand" src="{OKT}" style="width:420px">
      <div class="kicker bc" style="font-size:34px;letter-spacing:.28em">Vive el Oktoberfest</div>
      <div class="feats-list">{rows}</div>
    </div>"""
    return stage(w, h, inner, objpos="center 42%", fade=False, nota=False, photo=PH_BEER)


def slide_valor(w, h):
    """Historia propuesta de valor (1080×1920): todo lo que ofrece el festival, en grande."""
    rows = "".join(f'<div class="row"><div class="dot"></div><div class="txt bc" style="font-size:62px">{x}</div></div>'
                   for x in FEATS)
    extra = ".feats-list .row{padding:30px 6px}.feats-list .dot{width:20px;height:20px}"
    inner = f"""<div class="in" style="padding:180px 78px 240px;justify-content:flex-start">
      <img class="sello" src="{LATOMA}" style="height:58px">
      <img class="brand" src="{OKT}" style="width:500px;margin-top:14px">
      <div class="kicker bc" style="font-size:42px;letter-spacing:.24em;margin-top:26px">Todo esto te espera</div>
      <div class="feats-list" style="margin-top:36px">{rows}</div>
      <div style="margin-top:auto;display:flex;flex-direction:column;align-items:center;gap:8px">
        <div class="when bc" style="font-size:54px">Sábado 24 de octubre</div>
        <div class="place bc" style="font-size:32px">Centro de Eventos CESAP · Bogotá</div>
        <div class="handle bc" style="font-size:22px;margin-top:10px">@oktoberfestartesanalbog</div>
      </div>
    </div>"""
    return stage(w, h, inner, objpos="center 42%", photo_h=1400, fade=True, nota=False,
                 photo=PH_BEER, extra=extra)


def slide_cta(w, h):
    inner = f"""<div class="in" style="padding:110px 90px 130px;justify-content:center;gap:26px">
      {mast(1.0)}
      <div class="kicker bc" style="font-size:38px;margin-top:20px">Compra tu boleta</div>
      <div class="pill bc" style="padding:22px 60px"><span style="font-size:36px">Comprar en Tuboleta</span></div>
      {tk_lockup(30)}
      <div class="when bc" style="font-size:40px;margin-top:14px">Sábado 24 de octubre</div>
      <div class="place bc" style="font-size:30px">Centro de Eventos CESAP · Bogotá</div>
      <div class="handle bc" style="font-size:22px;margin-top:8px">@oktoberfestartesanalbog</div>
    </div>"""
    return stage(w, h, inner, objpos="center 55%", fade=False, nota=True, photo=PH_CROWD)


PIEZAS = [
    ("historia-lanzamiento", 1080, 1920, lambda: slide_lanzamiento(1080, 1920, story=True)),
    ("historia-boletas", 1080, 1920, lambda: slide_boleteria(1080, 1920, story=True)),
    ("historia-propuesta-valor", 1080, 1920, lambda: slide_valor(1080, 1920)),
    ("carrusel-1-lanzamiento", 1080, 1350, lambda: slide_lanzamiento(1080, 1350)),
    ("carrusel-2-boleteria", 1080, 1350, lambda: slide_boleteria(1080, 1350)),
    ("carrusel-3-experiencias", 1080, 1350, lambda: slide_features(1080, 1350)),
    ("carrusel-4-cta", 1080, 1350, lambda: slide_cta(1080, 1350)),
]


def main():
    for slug, w, h, fn in PIEZAS:
        src = BUILD / f"{slug}.html"; png = BUILD / f"{slug}.png"; jpg = OUT / f"{slug}.jpg"
        src.write_text(fn(), encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={w},{h}",
                        "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()],
                       check=True, capture_output=True)
        im = Image.open(png).convert("RGB")
        assert im.size == (w, h), f"{slug}: {im.size}"
        for q in range(95, 78, -3):
            im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
            if jpg.stat().st_size <= 500 * 1000:
                break
        print(f"{jpg.name}  {w}x{h}  {jpg.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
