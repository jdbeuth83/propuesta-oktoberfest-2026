#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flyer general Oktoberfest Artesanal — Medellín y Bogotá · post (1080×1350) e
historia (1080×1920). Rediseño profesional tras auditoría comercial/mercadeo:

  · Dato HERO de cervecerías (+70 Med / +40 Bog) como argumento de venta principal.
  · Medellín sobre imagen de ATARDECER (hora dorada), no nocturna.
  · Line up (Medellín) · CTA de boletas claro.
  · Footer de credibilidad: ORGANIZAN (Black Elephant · La Toma) + patrocinadores.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "flyer"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
BE = du(WORK_AS / "black-elephant-crema.png", "image/png")
SP = {n: du(WORK_AS / f"spon-{n}.png", "image/png") for n in ("3cordilleras", "comfenalco", "betplay")}
QR = {c: du(WORK_AS / f"qr-{c}.png", "image/png") for c in ("medellin", "bogota")}

LINEUP = ["Kraken", "Tributo a Caifanes · The Mills · Bajo Tierra",
          "Tributo a Molotov · Nepentes · Manuel Urrego",
          "Terlete · DJ Tobby · + más por confirmar"]

CITIES = {
    "medellin": dict(city="Medellín", date="Sábado 26 de septiembre", place="Parque Norte · Medellín",
                     platform="latiquetera.com", bg=WORK_AS / "medellin-atardecer.jpg", objpos="center 40%",
                     cerv="+70", sub="+350 cervezas por probar · 4 escenarios · artistas en vivo · gastronomía · atracciones del parque",
                     lineup=True, sponsors=["3cordilleras", "comfenalco", "betplay"], handle="@oktoberfestartesanal", pulep=""),
    "bogota": dict(city="Bogotá", date="Sábado 24 de octubre", place="Centro de Eventos CESAP · Bogotá",
                   platform="tuboleta.com", bg=REPO_AS / "hero-sunset.jpg", objpos="60% center",
                   cerv="+40", sub="+200 cervezas por probar · artistas en vivo · gastronomía · experiencias inmersivas",
                   lineup=False, sponsors=["3cordilleras", "betplay"], handle="@oktoberfestartesanalbog", pulep="IZP513"),
}
FORMATS = [("post", 1080, 1350), ("historia", 1080, 1920), ("postal", 1800, 1200)]  # postal = horizontal
ONLY = ["medellin"]  # por ahora trabajamos solo con Medellín


def page(key, cfg, fmt, w, h):
    story = fmt == "historia"
    postal = fmt == "postal"
    s = 1.05 if story else (1.16 if postal else 1.0)
    # Historia: márgenes grandes arriba/abajo por las zonas seguras de Instagram.
    pt = 250 if story else (96 if postal else 62)
    pb = 300 if story else (88 if postal else 60)
    g = round(min(w, h) * 0.02)
    hero = du(cfg["bg"], "image/jpeg")

    if cfg["lineup"]:
        ln = f'<div class="ln-h">{LINEUP[0]}</div>' + "".join(f'<div class="ln">{x}</div>' for x in LINEUP[1:])
        middle = f'<div class="lineup"><div class="kk">Line Up 2026</div>{ln}</div>'
    else:
        middle = ""

    spons = "".join(f'<img class="sp" src="{SP[n]}">' for n in cfg["sponsors"])
    pulep = f'<div class="pulep">PULEP {cfg["pulep"]}</div>' if cfg["pulep"] else ""

    if postal:
        cta_inner = (f'<div class="qrbox"><img class="qr" src="{QR[key]}">'
                     f'<div class="qrt">Escanea<br>y compra tus<br>boletas aquí</div></div>'
                     f'<div class="qrsub">{cfg["platform"]}</div>')
    else:
        cta_inner = f'<div class="pill"><span>Boletas en {cfg["platform"]}</span></div>'

    return f"""<!doctype html><meta charset="utf-8"><title>Flyer {cfg['city']} · {fmt}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800&display=swap');
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#000}}
body{{font-family:'Barlow',sans-serif;-webkit-font-smoothing:antialiased}} img{{display:block}}
.bc{{font-family:'Barlow Condensed',sans-serif}}
.stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:#14110B;color:#EEE7D6}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{cfg['objpos']};filter:saturate(1.1) contrast(1.03) brightness(1.05)}}
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(12,9,5,.72) 0%,rgba(12,9,5,.32) 20%,rgba(12,9,5,.28) 42%,rgba(10,6,2,.72) 70%,rgba(8,5,2,.96) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:{pt}px 66px {pb}px}}
.sello{{height:{round(46*s)}px;opacity:.95;filter:drop-shadow(0 5px 18px rgba(0,0,0,.6))}}
.brand{{width:{round(400*s)}px;max-width:86%;margin-top:{round(g*.7)}px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.5))}}
.city{{margin-top:{round(g*.5)}px;font-family:'Barlow Condensed';font-weight:700;font-size:{round(74*s)}px;line-height:.9;
  letter-spacing:.05em;text-transform:uppercase;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.city span{{color:#EEE7D6}}
.dp{{margin-top:{round(g*.35)}px;font-family:'Barlow Condensed';font-weight:600;font-size:{round(27*s)}px;letter-spacing:.14em;
  text-transform:uppercase;color:#EEE7D6;text-shadow:0 3px 16px rgba(0,0,0,.9)}}
.rule{{width:{round(200*s)}px;height:2px;background:linear-gradient(90deg,transparent,#E9A72C,transparent);margin:{round(g*.75)}px 0 {round(g*.5)}px}}
/* Dato HERO de cervecerías */
.stat{{display:flex;align-items:baseline;justify-content:center;gap:{round(14*s)}px}}
.stat b{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(96*s)}px;line-height:.85;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.stat u{{text-decoration:none;font-family:'Barlow Condensed';font-weight:700;font-size:{round(40*s)}px;letter-spacing:.06em;
  text-transform:uppercase;color:#EEE7D6}}
.sub{{margin-top:{round(g*.45)}px;font-family:'Barlow Condensed';font-weight:600;font-size:{round(24*s)}px;letter-spacing:.05em;
  text-transform:uppercase;color:#EEE7D6;max-width:{round(w*.82)}px;line-height:1.35;text-shadow:0 3px 14px rgba(0,0,0,.9)}}
/* Line up */
.lineup{{margin-top:{round(g*.9)}px;display:flex;flex-direction:column;align-items:center}}
.kk{{font-family:'Barlow Condensed';font-weight:600;font-size:{round(22*s)}px;letter-spacing:.3em;text-transform:uppercase;color:#E9A72C;margin-bottom:{round(g*.35)}px}}
.ln-h{{font-family:'Playfair Display',serif;font-weight:800;font-size:{round(58*s)}px;line-height:.95;text-transform:uppercase;color:#EEE7D6;text-shadow:0 5px 24px rgba(0,0,0,.85)}}
.ln{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(27*s)}px;line-height:1.26;text-transform:uppercase;color:#EEE7D6;text-shadow:0 3px 14px rgba(0,0,0,.9);max-width:{round(w*.9)}px}}
/* CTA */
.cta{{margin-top:{round(g*1.0)}px;display:flex;flex-direction:column;align-items:center;gap:{round(g*.5)}px}}
.cta .k{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(30*s)}px;letter-spacing:.14em;text-transform:uppercase;color:#E9A72C;text-shadow:0 3px 18px rgba(0,0,0,.85)}}
.pill{{display:inline-flex;align-items:center;background:#E9A72C;color:#2A1B06;border-radius:999px;padding:{round(16*s)}px {round(40*s)}px;
  box-shadow:0 20px 50px -18px rgba(233,167,44,.95)}}
.pill span{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(28*s)}px;letter-spacing:.07em;text-transform:uppercase;white-space:nowrap}}
.qrbox{{display:flex;align-items:center;gap:{round(20*s)}px;background:#EEE7D6;border-radius:{round(18*s)}px;padding:{round(16*s)}px {round(24*s)}px;box-shadow:0 18px 46px -18px rgba(0,0,0,.7)}}
.qr{{width:{round(148*s)}px;height:{round(148*s)}px;border-radius:8px;display:block}}
.qrt{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(27*s)}px;line-height:1.06;letter-spacing:.02em;text-transform:uppercase;color:#2A1B06;text-align:left}}
.qrsub{{margin-top:{round(g*.4)}px;font-family:'Barlow Condensed';font-weight:700;font-size:{round(23*s)}px;letter-spacing:.08em;text-transform:uppercase;color:#E9A72C}}
/* Footer credibilidad */
.foot{{margin-top:auto;display:flex;flex-direction:column;align-items:center;width:100%;padding-top:{round(g*.8)}px}}
.grp{{display:flex;flex-direction:column;align-items:center}}
.lbl{{font-family:'Barlow Condensed';font-weight:600;font-size:{round(18*s)}px;letter-spacing:.24em;text-transform:uppercase;color:#B7AC93;margin-bottom:{round(g*.4)}px}}
.logos{{display:flex;align-items:center;justify-content:center;gap:{round(40*s)}px;flex-wrap:wrap}}
.org{{height:{round(46*s)}px;width:auto;opacity:.95}} .lt{{height:{round(38*s)}px;width:auto;opacity:.95}}
.sp{{height:{round(36*s)}px;width:auto;opacity:.92}}
.sep{{width:70%;max-width:520px;height:1px;background:rgba(255,255,255,.12);margin:{round(g*.75)}px 0}}
.handle{{margin-top:{round(g*.7)}px;font-family:'Barlow Condensed';font-weight:600;font-size:{round(19*s)}px;letter-spacing:.14em;text-transform:uppercase;color:#B7AC93}}
.pulep{{position:absolute;left:{round(min(w,h)*0.033)}px;bottom:{round(min(w,h)*0.033)}px;z-index:4;font-family:'Barlow Condensed';
  font-weight:600;font-size:{max(12,round(min(w,h)*0.015))}px;letter-spacing:.16em;text-transform:uppercase;color:#EEE7D6;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
</style>
<div class="stage">
  <div class="photo"><img src="{hero}" alt=""></div><div class="veil"></div>
  <div class="in">
    <img class="sello" src="{LATOMA}">
    <img class="brand" src="{OKT}">
    <div class="city">{cfg['city'].split()[0]} <span>2026</span></div>
    <div class="dp">{cfg['date']} · {cfg['place']}</div>
    <div class="rule"></div>
    <div class="stat"><b>{cfg['cerv']}</b><u>Cervecerías<br>artesanales</u></div>
    <div class="sub">{cfg['sub']}</div>
    {middle}
    <div class="cta">
      <div class="k">¡Boletas a la venta!</div>
      {cta_inner}
    </div>
    <div class="foot">
      <div class="grp"><div class="lbl">Organizan</div>
        <div class="logos"><img class="org" src="{BE}"><img class="lt" src="{LATOMA}"></div></div>
      <div class="sep"></div>
      <div class="grp"><div class="lbl">Con el apoyo de</div>
        <div class="logos">{spons}</div></div>
      <div class="handle">{cfg['handle']}</div>
    </div>
  </div>
  {pulep}
</div>"""


def page_h(key, cfg, w, h):
    """Postal HORIZONTAL para imprimir (volante), con QR arriba a la derecha."""
    hero = du(cfg["bg"], "image/jpeg")
    ln = f'<div class="ln-h">{LINEUP[0]}</div>' + "".join(f'<div class="ln">{x}</div>' for x in LINEUP[1:]) if cfg["lineup"] else ""
    spons = "".join(f'<img class="sp" src="{SP[n]}">' for n in cfg["sponsors"])
    pulep = f'<div class="pulep">PULEP {cfg["pulep"]}</div>' if cfg["pulep"] else ""
    return f"""<!doctype html><meta charset="utf-8"><title>Postal horizontal {cfg['city']}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800&display=swap');
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#000}}
body{{font-family:'Barlow',sans-serif;-webkit-font-smoothing:antialiased}} img{{display:block}}
.stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:#14110B;color:#EEE7D6}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 42%;filter:saturate(1.1) contrast(1.03) brightness(1.05)}}
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(12,9,5,.6) 0%,rgba(12,9,5,.34) 30%,rgba(10,6,2,.5) 70%,rgba(8,5,2,.94) 100%),
  radial-gradient(120% 90% at 50% 42%,transparent 44%,rgba(8,5,2,.55) 100%)}}
.in{{position:absolute;left:0;right:0;top:0;bottom:170px;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:60px 90px 0}}
.sello{{height:44px;opacity:.95;filter:drop-shadow(0 5px 18px rgba(0,0,0,.6))}}
.brand{{width:360px;margin-top:12px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.5))}}
.city{{margin-top:10px;font-family:'Barlow Condensed';font-weight:700;font-size:84px;line-height:.9;letter-spacing:.05em;text-transform:uppercase;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.city span{{color:#EEE7D6}}
.dp{{margin-top:8px;font-family:'Barlow Condensed';font-weight:600;font-size:30px;letter-spacing:.14em;text-transform:uppercase;color:#EEE7D6;text-shadow:0 3px 16px rgba(0,0,0,.9)}}
.rule{{width:220px;height:2px;background:linear-gradient(90deg,transparent,#E9A72C,transparent);margin:18px 0 14px}}
.stat{{display:flex;align-items:baseline;justify-content:center;gap:16px}}
.stat b{{font-family:'Barlow Condensed';font-weight:700;font-size:100px;line-height:.85;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.stat u{{text-decoration:none;font-family:'Barlow Condensed';font-weight:700;font-size:44px;letter-spacing:.06em;text-transform:uppercase;color:#EEE7D6}}
.sub{{margin-top:10px;font-family:'Barlow Condensed';font-weight:600;font-size:26px;letter-spacing:.05em;text-transform:uppercase;color:#EEE7D6;max-width:900px;line-height:1.32;text-shadow:0 3px 14px rgba(0,0,0,.9)}}
.kk{{margin-top:22px;font-family:'Barlow Condensed';font-weight:600;font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#E9A72C}}
.ln-h{{font-family:'Playfair Display',serif;font-weight:800;font-size:60px;line-height:.95;text-transform:uppercase;color:#EEE7D6;text-shadow:0 5px 24px rgba(0,0,0,.85);margin-top:4px}}
.ln{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;line-height:1.25;text-transform:uppercase;color:#EEE7D6;text-shadow:0 3px 14px rgba(0,0,0,.9)}}
.venta{{margin-top:20px;font-family:'Barlow Condensed';font-weight:700;font-size:34px;letter-spacing:.14em;text-transform:uppercase;color:#E9A72C;text-shadow:0 3px 18px rgba(0,0,0,.85)}}
/* QR arriba a la derecha */
.qrc{{position:absolute;top:60px;right:60px;z-index:5;display:flex;align-items:center;gap:20px;background:#EEE7D6;border-radius:20px;padding:18px 24px;box-shadow:0 20px 50px -16px rgba(0,0,0,.75)}}
.qrc img{{width:180px;height:180px;border-radius:8px;display:block}}
.qrc .t{{font-family:'Barlow Condensed';font-weight:700;font-size:27px;line-height:1.06;text-transform:uppercase;color:#2A1B06;text-align:left}}
.qrc .t small{{display:block;font-size:19px;color:#7a6a48;letter-spacing:.04em;margin-top:6px}}
/* Footer barra inferior */
.foot{{position:absolute;left:0;right:0;bottom:44px;z-index:4;display:flex;align-items:center;justify-content:center;gap:60px;flex-wrap:wrap}}
.grp{{display:flex;flex-direction:column;align-items:center}}
.lbl{{font-family:'Barlow Condensed';font-weight:600;font-size:17px;letter-spacing:.24em;text-transform:uppercase;color:#B7AC93;margin-bottom:10px}}
.logos{{display:flex;align-items:center;gap:34px}}
.org{{height:46px;opacity:.95}} .lt{{height:38px;opacity:.95}} .sp{{height:34px;opacity:.92}}
.vsep{{width:1px;height:64px;background:rgba(255,255,255,.16)}}
.handle{{position:absolute;left:0;right:0;bottom:14px;z-index:4;text-align:center;font-family:'Barlow Condensed';font-weight:600;font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:#8a7f68}}
.pulep{{position:absolute;left:40px;bottom:14px;z-index:5;font-family:'Barlow Condensed';font-weight:600;font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:#EEE7D6;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
</style>
<div class="stage">
  <div class="photo"><img src="{hero}" alt=""></div><div class="veil"></div>
  <div class="qrc"><img src="{QR[key]}"><div class="t">Escanea<br>y compra tus<br>boletas aquí<small>{cfg['platform']}</small></div></div>
  <div class="in">
    <img class="sello" src="{LATOMA}">
    <img class="brand" src="{OKT}">
    <div class="city">{cfg['city'].split()[0]} <span>2026</span></div>
    <div class="dp">{cfg['date']} · {cfg['place']}</div>
    <div class="rule"></div>
    <div class="stat"><b>{cfg['cerv']}</b><u>Cervecerías artesanales</u></div>
    <div class="sub">{cfg['sub']}</div>
    <div class="kk">Line Up 2026</div>{ln}
    <div class="venta">¡Boletas a la venta!</div>
  </div>
  <div class="foot">
    <div class="grp"><div class="lbl">Organizan</div>
      <div class="logos"><img class="org" src="{BE}"><img class="lt" src="{LATOMA}"></div></div>
    <div class="vsep"></div>
    <div class="grp"><div class="lbl">Con el apoyo de</div>
      <div class="logos">{spons}</div></div>
  </div>
  <div class="handle">{cfg['handle']}</div>
  {pulep}
</div>"""


def main():
    build = OUT / ".build"; build.mkdir(exist_ok=True)
    for key, cfg in CITIES.items():
        if ONLY and key not in ONLY:
            continue
        for fmt, w, h in FORMATS:
            postal = fmt == "postal"
            scale = 2 if postal else 1            # postal: doble resolución para impresión
            dpi = 300 if postal else 72
            cap = 3000 if postal else 500         # KB
            src = build / f"{key}-{fmt}.html"; png = build / f"{key}-{fmt}.png"; jpg = OUT / f"flyer-{key}-{fmt}.jpg"
            html = page_h(key, cfg, w, h) if postal else page(key, cfg, fmt, w, h)
            src.write_text(html, encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
                            "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
            im = Image.open(png).convert("RGB")
            assert im.size == (w * scale, h * scale), f"{key}-{fmt}: {im.size}"
            for q in range(95, 60, -3):
                im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(dpi, dpi))
                if jpg.stat().st_size <= cap * 1000:
                    break
            print(f"flyer-{key}-{fmt}  {im.size[0]}x{im.size[1]}  {dpi}dpi  {jpg.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
