#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanzamiento · Oktoberfest Artesanal Bogotá 2026 — post (1080×1080) e historia
(1080×1920). Misma imagen madre del Save the Date, ahora con TODOS los datos y
el anuncio de boletas a la venta.

Contenido: marca + Bogotá 2026 · ¡Boletas a la venta! · Sábado 24 de octubre ·
Centro de Eventos CESAP · pilares (+40 cervecerías, bandas en vivo, gastronomía,
talento local) · Boletas desde $54.900 en tuboleta.com · @handle · PULEP.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "lanzamiento"
OUT.mkdir(parents=True, exist_ok=True)

PULEP = "IZP513"
KICKER = "¡Boletas a la venta!"
DATE = "Sábado 24 de octubre"
PLACE = "Centro de Eventos CESAP · Bogotá"
FEATS = ["+40 Cervecerías", "Bandas en vivo", "Gastronomía", "Talento local"]
PRICE = "Boletas desde $54.900"
WEB = "tuboleta.com"
MAX_KB = 500


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


HERO = du(REPO_AS / "hero-sunset.jpg", "image/jpeg")
OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
TUBO = du(WORK_AS / "tuboleta-blanco.png", "image/png")
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")


def find_chrome():
    p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(p).exists():
        return p
    raise SystemExit("No Chrome")


FORMATS = [
    dict(slug="post-1080x1080", w=1080, h=1080, pad=(58, 80, 58), objpos="72% center",
         fade=False, sello=46, brand=400, city=68, kicker=30, when=54, place=30, feats=25,
         tk=24, price=26, pillw=40, handle=17),
    dict(slug="historia-1080x1920", w=1080, h=1920, pad=(170, 80, 210), objpos="55% center",
         fade=True, photo_h=1400, sello=68, brand=580, city=100, kicker=42, when=82, place=42,
         feats=32, tk=32, price=38, pillw=54, handle=23),
]


def page(f):
    fade = f.get("fade", False)
    pt, px, pb = f["pad"]
    gap = round(min(f["w"], f["h"]) * 0.024)
    photo_h = f.get("photo_h", f["h"])
    fade_css = ("""
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);""" if fade else "")
    top_veil = ("rgba(20,17,11,.88) 0%,rgba(20,17,11,.5) 20%,rgba(20,17,11,.08) 36%,transparent 48%"
                if fade else
                "rgba(20,17,11,.86) 0%,rgba(20,17,11,.66) 24%,rgba(20,17,11,.36) 38%,"
                "rgba(20,17,11,.10) 50%,transparent 62%")
    veil = (f"linear-gradient(180deg,{top_veil}),"
            "linear-gradient(0deg,rgba(10,6,2,.94) 0%,rgba(10,6,2,.82) 20%,"
            "rgba(10,6,2,.46) 42%,transparent 60%)")
    corner_in = round(min(f["w"], f["h"]) * 0.035)
    corner_fs = max(12, round(min(f["w"], f["h"]) * 0.018))
    feats_html = "<i>·</i>".join(f"<span>{x}</span>" for x in FEATS)
    return f"""<!doctype html><meta charset="utf-8">
<title>Lanzamiento · Oktoberfest Bogotá 2026 · {f['slug']}</title>
<style>
{FONTS_CSS}
:root{{--night:#14110B;--cream:#EEE7D6;--soft:#B7AC93;--gold:#E9A72C;--ember:#E2611A}}
*{{box-sizing:border-box;margin:0}} html,body{{background:#000}}
body{{font-family:'Barlow',system-ui,sans-serif;-webkit-font-smoothing:antialiased}} img{{display:block}}
.stage{{position:relative;width:{f['w']}px;height:{f['h']}px;overflow:hidden;background:var(--night);color:var(--cream)}}
.photo{{position:absolute;inset:auto 0 0 0;height:{photo_h}px;{fade_css}}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{f['objpos']};
  filter:saturate(1.1) contrast(1.03) brightness(1.1)}}
.glow{{position:absolute;inset:0;background:radial-gradient(58% 26% at 42% 40%,rgba(244,196,90,.24),transparent 72%)}}
.veil{{position:absolute;inset:0;background:{veil}}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;
  text-align:center;padding:{pt}px {px}px {pb}px}}
.mast,.foot{{display:flex;flex-direction:column;align-items:center}} .foot{{margin-top:auto}}
.sello{{height:{f['sello']}px;filter:drop-shadow(0 6px 22px rgba(0,0,0,.6))}}
.brand{{width:{f['brand']}px;margin-top:{round(gap*1.0)}px;filter:drop-shadow(0 12px 30px rgba(0,0,0,.45))}}
.city{{margin-top:{round(gap*.5)}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:{f['city']}px;line-height:.9;letter-spacing:.085em;text-transform:uppercase;color:var(--gold);
  text-shadow:0 6px 34px rgba(0,0,0,.6)}}
.city span{{color:var(--cream)}}
.kicker{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;font-size:{f['kicker']}px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.85);
  margin-bottom:{round(gap*.5)}px}}
.when{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;font-size:{f['when']}px;line-height:1;
  letter-spacing:.05em;text-transform:uppercase;color:var(--cream);text-shadow:0 5px 30px rgba(0,0,0,.85)}}
.place{{margin-top:{round(gap*.3)}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;
  font-size:{f['place']}px;letter-spacing:.13em;text-transform:uppercase;color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.9)}}
.feats{{margin-top:{round(gap*.6)}px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;
  gap:{round(gap*.45)}px;max-width:{round(f['w']*.86)}px}}
.feats span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{f['feats']}px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--cream);text-shadow:0 3px 16px rgba(0,0,0,.85);white-space:nowrap}}
.feats i{{color:var(--gold);font-style:normal;font-size:{f['feats']}px;opacity:.85}}
.pill{{margin-top:{round(gap*.85)}px;display:inline-flex;align-items:center;background:var(--gold);color:#2A1B06;
  border-radius:999px;padding:{round(f['pillw']*.42)}px {f['pillw']}px;box-shadow:0 22px 54px -18px rgba(233,167,44,.95)}}
.pill span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:{f['price']}px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}}
.tk{{margin-top:{round(gap*.65)}px;display:flex;align-items:center;justify-content:center;gap:{round(gap*.4)}px}}
.tk .lbl{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{f['tk']}px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--cream)}}
.tk img{{height:{round(f['tk']*1.25)}px;filter:drop-shadow(0 3px 12px rgba(0,0,0,.7))}}
.tk .web{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;font-size:{f['tk']}px;color:var(--cream)}}
.handle{{margin-top:{round(gap*.7)}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;
  font-size:{f['handle']}px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft)}}
.pulep{{position:absolute;left:{corner_in}px;bottom:{corner_in}px;z-index:4;
  font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{corner_fs}px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--cream);text-shadow:0 2px 12px rgba(0,0,0,.9)}}
</style>
<div class="stage">
  <div class="photo"><img src="{HERO}" alt="Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div><div class="veil"></div>
  <div class="in">
    <div class="mast">
      <img class="sello" src="{LATOMA}" alt="La Toma Cervecera">
      <img class="brand" src="{OKT}" alt="Oktoberfest Artesanal">
      <div class="city">Bogotá <span>2026</span></div>
    </div>
    <div class="foot">
      <div class="kicker">{KICKER}</div>
      <div class="when">{DATE}</div>
      <div class="place">{PLACE}</div>
      <div class="feats">{feats_html}</div>
      <div class="pill"><span>{PRICE}</span></div>
      <div class="tk"><span class="lbl">en</span><img src="{TUBO}" alt="Tuboleta"><span class="web">{WEB}</span></div>
      <div class="handle">@oktoberfestartesanalbog</div>
    </div>
  </div>
  <div class="pulep">PULEP {PULEP}</div>
</div>
"""


def main():
    build = OUT / ".build"; build.mkdir(exist_ok=True)
    for f in FORMATS:
        src = build / f"{f['slug']}.html"; png = build / f"{f['slug']}.png"
        jpg = OUT / f"lanzamiento-{f['slug']}.jpg"
        src.write_text(page(f), encoding="utf-8")
        subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={f['w']},{f['h']}", "--virtual-time-budget=8000",
                        f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
        im = Image.open(png).convert("RGB")
        assert im.size == (f["w"], f["h"]), im.size
        for q in range(95, 78, -3):
            im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
            if jpg.stat().st_size <= MAX_KB * 1000:
                break
        print(f"{jpg.name}  {im.size[0]}x{im.size[1]}  {jpg.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
