#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flyer general Oktoberfest Artesanal — Medellín y Bogotá, en post (1080×1350) e
historia (1080×1920).

Medellín: line up + venta de boletas (La Tiquetera) + patrocinadores.
Bogotá:   propuesta de valor + venta de boletas (Tuboleta) + patrocinadores.
Todo sobre foto real del festival, paleta ocaso y el logo azul.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
FOTOS = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/fotos")
OUT = ROOT / "renders" / "flyer"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
SP = {n: du(WORK_AS / f"spon-{n}.png", "image/png") for n in ("3cordilleras", "comfenalco", "betplay")}

MED_FEATS = ["+70 Cervecerías", "+350 Cervezas por probar", "4 Escenarios",
             "Gastronomía", "Artistas en vivo", "Atracciones del parque"]
BOG_FEATS = ["+40 Cervecerías", "+200 Cervezas por probar", "Artistas en vivo",
             "Gastronomía", "Experiencias inmersivas"]
LINEUP = ["Kraken", "Tributo a Caifanes · The Mills · Bajo Tierra",
          "Tributo a Molotov · Nepentes · Manuel Urrego",
          "Terlete · DJ Tobby · + más por confirmar"]

CITIES = {
    "medellin": dict(city="Medellín", date="Sábado 26 de septiembre", place="Parque Norte · Medellín",
                     platform="latiquetera.com", foto="escenario/F1-231_Oktober-307.jpg", objpos="center 55%",
                     lineup=True, sponsors=["3cordilleras", "comfenalco", "betplay"], pulep=""),
    "bogota": dict(city="Bogotá", date="Sábado 24 de octubre", place="Centro de Eventos CESAP · Bogotá",
                   platform="tuboleta.com", foto=None, objpos="60% center",
                   lineup=False, sponsors=["3cordilleras", "betplay"], pulep="IZP513"),
}
FORMATS = [("post", 1080, 1350), ("historia", 1080, 1920)]


def page(cfg, fmt, w, h):
    story = fmt == "historia"
    s = 1.18 if story else 1.0
    pt = 150 if story else 66
    pb = 150 if story else 66
    gap = round(min(w, h) * 0.022)
    hero = du(FOTOS / cfg["foto"], "image/jpeg") if cfg["foto"] else du(REPO_AS / "hero-sunset.jpg", "image/jpeg")
    corner = round(min(w, h) * 0.033)

    if cfg["lineup"]:
        head = f'<div class="ln-h">{LINEUP[0]}</div>' + "".join(
            f'<div class="ln">{x}</div>' for x in LINEUP[1:])
        middle = f'<div class="lineup"><div class="kick">Line Up</div>{head}</div>'
    else:
        feats = "<i>·</i>".join(f"<span>{x}</span>" for x in BOG_FEATS)
        middle = f'<div class="feats">{feats}</div>'

    spons = "".join(f'<img class="sp" src="{SP[n]}">' for n in cfg["sponsors"])
    pulep = f'<div class="pulep">PULEP {cfg["pulep"]}</div>' if cfg["pulep"] else ""

    return f"""<!doctype html><meta charset="utf-8">
<title>Flyer {cfg['city']} · {fmt}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800&display=swap');
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#000}}
body{{font-family:'Barlow',sans-serif;-webkit-font-smoothing:antialiased}} img{{display:block}}
.stage{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:#14110B;color:#EEE7D6}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{cfg['objpos']};filter:saturate(1.08) contrast(1.03) brightness(1.06)}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,10,6,.86) 0%,rgba(14,10,6,.5) 26%,
  rgba(14,10,6,.42) 50%,rgba(10,6,2,.78) 76%,rgba(8,5,2,.95) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:{pt}px 70px {pb}px}}
.sello{{height:{round(48*s)}px;opacity:.95;filter:drop-shadow(0 5px 18px rgba(0,0,0,.6))}}
.brand{{width:{round(430*s)}px;max-width:88%;margin-top:{round(gap*.7)}px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.5))}}
.city{{margin-top:{round(gap*.5)}px;font-family:'Barlow Condensed';font-weight:700;font-size:{round(78*s)}px;line-height:.9;
  letter-spacing:.06em;text-transform:uppercase;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.city span{{color:#EEE7D6}}
.dp{{margin-top:{round(gap*.35)}px;font-family:'Barlow Condensed';font-weight:600;font-size:{round(30*s)}px;letter-spacing:.14em;
  text-transform:uppercase;color:#EEE7D6;text-shadow:0 3px 16px rgba(0,0,0,.9)}}
.kickv{{margin-top:{round(gap*.7)}px;font-family:'Barlow Condensed';font-weight:700;font-size:{round(34*s)}px;letter-spacing:.14em;
  text-transform:uppercase;color:#E9A72C;text-shadow:0 3px 18px rgba(0,0,0,.85)}}
.mid{{display:flex;flex-direction:column;align-items:center;margin:{round(gap*.9)}px 0}}
.lineup{{display:flex;flex-direction:column;align-items:center}}
.kick{{font-family:'Barlow Condensed';font-weight:600;font-size:{round(22*s)}px;letter-spacing:.3em;text-transform:uppercase;color:#E9A72C;margin-bottom:{round(gap*.4)}px}}
.ln-h{{font-family:'Playfair Display',serif;font-weight:800;font-size:{round(70*s)}px;line-height:.95;text-transform:uppercase;color:#EEE7D6;text-shadow:0 5px 24px rgba(0,0,0,.8)}}
.ln{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(30*s)}px;line-height:1.28;text-transform:uppercase;color:#EEE7D6;
  text-shadow:0 3px 14px rgba(0,0,0,.85);max-width:{round(w*.9)}px}}
.feats{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:{round(gap*.5)}px;max-width:{round(w*.86)}px}}
.feats span{{font-family:'Barlow Condensed';font-weight:600;font-size:{round(30*s)}px;letter-spacing:.08em;text-transform:uppercase;color:#EEE7D6;white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.85)}}
.feats i{{color:#E9A72C;font-style:normal;font-size:{round(30*s)}px;opacity:.85}}
.pill{{display:inline-flex;align-items:center;background:#E9A72C;color:#2A1B06;border-radius:999px;
  padding:{round(16*s)}px {round(40*s)}px;box-shadow:0 20px 50px -18px rgba(233,167,44,.95)}}
.pill span{{font-family:'Barlow Condensed';font-weight:700;font-size:{round(30*s)}px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}}
.foot{{margin-top:auto;display:flex;flex-direction:column;align-items:center;width:100%}}
.spon-h{{font-family:'Barlow Condensed';font-weight:600;font-size:{round(20*s)}px;letter-spacing:.24em;text-transform:uppercase;color:#B7AC93;margin-bottom:{round(gap*.55)}px}}
.spons{{display:flex;align-items:center;justify-content:center;gap:{round(46*s)}px;flex-wrap:wrap}}
.sp{{height:{round(40*s)}px;width:auto;opacity:.95}}
.handle{{margin-top:{round(gap*.8)}px;font-family:'Barlow Condensed';font-weight:600;font-size:{round(20*s)}px;letter-spacing:.14em;text-transform:uppercase;color:#B7AC93}}
.pulep{{position:absolute;left:{corner}px;bottom:{corner}px;z-index:4;font-family:'Barlow Condensed';font-weight:600;
  font-size:{max(12,round(min(w,h)*0.016))}px;letter-spacing:.16em;text-transform:uppercase;color:#EEE7D6;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
</style>
<div class="stage">
  <div class="photo"><img src="{hero}" alt=""></div>
  <div class="veil"></div>
  <div class="in">
    <img class="sello" src="{LATOMA}">
    <img class="brand" src="{OKT}">
    <div class="city">{cfg['city'].split()[0]} <span>2026</span></div>
    <div class="dp">{cfg['date']} · {cfg['place']}</div>
    <div class="kickv">¡Boletas a la venta!</div>
    <div class="mid">{middle}</div>
    <div class="pill"><span>Boletas en {cfg['platform']}</span></div>
    <div class="foot">
      <div class="spon-h">Con el apoyo de</div>
      <div class="spons">{spons}</div>
      <div class="handle">@oktoberfestartesanal{'bog' if cfg['city']=='Bogotá' else ''}</div>
    </div>
  </div>
  {pulep}
</div>"""


def main():
    build = OUT / ".build"; build.mkdir(exist_ok=True)
    for key, cfg in CITIES.items():
        for fmt, w, h in FORMATS:
            src = build / f"{key}-{fmt}.html"; png = build / f"{key}-{fmt}.png"
            jpg = OUT / f"flyer-{key}-{fmt}.jpg"
            src.write_text(page(cfg, fmt, w, h), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={w},{h}",
                            "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()],
                           check=True, capture_output=True)
            im = Image.open(png).convert("RGB")
            assert im.size == (w, h), f"{key}-{fmt}: {im.size}"
            for q in range(94, 60, -3):
                im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
                if jpg.stat().st_size <= 500 * 1000:
                    break
            print(f"flyer-{key}-{fmt}  {w}x{h}  {jpg.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
