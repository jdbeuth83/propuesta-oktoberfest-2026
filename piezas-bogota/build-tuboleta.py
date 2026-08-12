#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piezas para publicar el Oktoberfest Artesanal Bogotá 2026 en Tuboleta.

Genera exactamente los formatos que exige el «Manual de piezas para publicar
eventos en Tuboleta»: banner desplegable, imagen del evento, boleta digital,
recurso banner, recurso plano, galería, redes (post/story) y el logo en blanco
y negro. Todas en JPG <500 KB a 72 dpi (galería <1 MB), salvo el logo (PNG).

Mismo Sistema de Diseño Bogotá que el save the date: imagen madre a la hora
dorada, paleta del ocaso, Barlow Condensed y el logotipo blackletter original.
Tres ejes de composición: stack (vertical/cuadrado), banner (apaisado) y strip
(franja 1920×150). La imagen del evento mantiene el diseño dentro de la caja
segura de 700×720 usando padding (100 lateral, 40 arriba/abajo sobre 900×800).
"""
import base64
import pathlib
import subprocess

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent
AS = ROOT / "_assets"
OUT = ROOT / "renders" / "tuboleta-plataforma"
BUILD = OUT / ".build"

PULEP = ""  # las boletas aún no salen a la venta: sin registro asignado todavía
MAX_KB = 500
MAX_KB_GALLERY = 1024


def find_chrome() -> str:
    for c in [
        "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]:
        if pathlib.Path(c).exists():
            return c
    raise SystemExit("No encontré headless_shell ni Google Chrome para renderizar.")


CHROME = find_chrome()
NEW_HEADLESS = "headless_shell" not in CHROME


def data_uri(name: str, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode((AS / name).read_bytes()).decode()}"


HERO = data_uri("hero-sunset.jpg", "image/jpeg")
OKT = data_uri("okt-logo.png", "image/png")
LATOMA = data_uri("latoma-blanco.png", "image/png")
FONTS_CSS = (AS / "fonts.css").read_text(encoding="utf-8")


FORMATS = [
    dict(group="banner-desplegable", slug="desktop-1920x150", w=1920, h=150,
         mode="strip", objpos="center 32%",
         sello=0, brand=104, city=42, kicker=0, when=40, pill=22,
         pill_pad="12px 26px", handle=0),
    dict(group="banner-desplegable", slug="mobile-1920x710", w=1920, h=710,
         mode="banner", pad=(84, 120, 84), objpos="center 30%",
         sello=48, brand=470, city=86, kicker=23, when=78, pill=29,
         pill_pad="19px 34px", handle=20),
    # Imagen del evento: lienzo 900×800, caja segura 700×720 vía padding.
    dict(group="imagen-evento", slug="imagen-evento-900x800", w=900, h=800,
         mode="stack", pad=(40, 100, 40), objpos="60% center",
         sello=46, brand=380, city=70, kicker=20, when=60, pill=24,
         pill_pad="15px 26px", handle=17),
    dict(group="boleta-digital", slug="boleta-digital-900x1050", w=900, h=1050,
         mode="stack", pad=(80, 92, 80), objpos="58% center",
         sello=50, brand=430, city=78, kicker=23, when=66, pill=26,
         pill_pad="17px 30px", handle=19),
    dict(group="recurso-banner", slug="recurso-banner-1000x400", w=1000, h=400,
         mode="banner", pad=(46, 64, 46), objpos="center 34%",
         sello=32, brand=300, city=54, kicker=16, when=50, pill=19,
         pill_pad="12px 22px", handle=None),
    dict(group="recurso-plano", slug="recurso-plano-1080x1080", w=1080, h=1080,
         mode="stack", pad=(84, 96, 84), objpos="72% center",
         sello=56, brand=470, city=84, kicker=24, when=72, pill=28,
         pill_pad="19px 32px", handle=21),
    dict(group="redes", slug="post-1080x1080", w=1080, h=1080, mode="stack",
         pad=(76, 86, 76), objpos="72% center",
         sello=50, brand=420, city=76, kicker=22, when=64, pill=25,
         pill_pad="18px 30px", handle=19),
    dict(group="redes", slug="story-1080x1920", w=1080, h=1920, mode="stack",
         pad=(200, 78, 250), objpos="55% center", photo_h=1400, fade=True,
         sello=74, brand=600, city=112, kicker=30, when=96, pill=34,
         pill_pad="24px 40px", handle=24),
    dict(group="galeria", slug="galeria-1-1000x1000", w=1000, h=1000, mode="stack",
         pad=(72, 82, 72), objpos="55% center", max_kb=MAX_KB_GALLERY,
         sello=48, brand=400, city=72, kicker=21, when=60, pill=24,
         pill_pad="16px 28px", handle=18),
    dict(group="galeria", slug="galeria-2-1000x1000", w=1000, h=1000, mode="stack",
         objpos="30% center", clean=True, max_kb=MAX_KB_GALLERY),
    dict(group="galeria", slug="galeria-3-1000x1000", w=1000, h=1000, mode="stack",
         objpos="80% center", clean=True, max_kb=MAX_KB_GALLERY),
]


def page(f: dict) -> str:
    mode = f["mode"]
    clean = f.get("clean", False)
    fade = f.get("fade", False)
    pt, px, pb = f.get("pad", (0, 0, 0))
    gap = round(min(f["w"], f["h"]) * 0.028)
    photo_h = f.get("photo_h", f["h"])

    fade_css = ("""
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);"""
                if fade else "")

    if mode in ("banner", "strip"):
        veil = ("linear-gradient(90deg,rgba(10,6,2,.88) 0%,rgba(10,6,2,.52) 30%,"
                "rgba(10,6,2,.44) 58%,rgba(10,6,2,.86) 100%),"
                "linear-gradient(180deg,rgba(20,17,11,.55) 0%,transparent 38%,rgba(10,6,2,.62) 100%)")
    else:
        top_veil = ("rgba(20,17,11,.94) 0%,rgba(20,17,11,.60) 20%,rgba(20,17,11,.10) 36%,transparent 46%"
                    if fade else
                    "rgba(20,17,11,.92) 0%,rgba(20,17,11,.80) 26%,rgba(20,17,11,.52) 40%,"
                    "rgba(20,17,11,.18) 52%,transparent 64%")
        veil = (f"linear-gradient(180deg,{top_veil}),"
                "linear-gradient(0deg,rgba(10,6,2,.96) 0%,rgba(10,6,2,.86) 16%,"
                "rgba(10,6,2,.48) 34%,transparent 48%)")

    if mode == "strip":
        layout = ".in{flex-direction:row;align-items:center;justify-content:space-between;gap:%dpx;}" % (gap * 2)
    elif mode == "banner":
        layout = (".in{flex-direction:row;align-items:center;justify-content:space-between;gap:%dpx;}"
                  ".mast{align-items:flex-start;text-align:left;}"
                  ".foot{align-items:flex-end;text-align:right;}" % (gap * 2))
    else:
        layout = (".in{flex-direction:column;align-items:center;text-align:center;}"
                  ".mast,.foot{align-items:center;}.foot{margin-top:auto;}")

    if clean:
        inner = ""
        watermark = f'<img class="wm" src="{OKT}" alt="Oktoberfest Artesanal">'
        wm_bottom = round(f["h"] * .06)
        wm_width = round(f["w"] * .42)
        wm_css = (f".wm{{position:absolute;left:50%;bottom:{wm_bottom}px;"
                  f"transform:translateX(-50%);width:{wm_width}px;height:auto;z-index:3;"
                  f"opacity:.96;filter:drop-shadow(0 10px 30px rgba(0,0,0,.6));}}")
    else:
        watermark = ""
        wm_css = ""
        sello = (f'<img class="sello" src="{LATOMA}" alt="La Toma Cervecera">' if f.get("sello") else "")
        handle = (f'<div class="handle">@oktoberfestartesanalbog</div>' if f.get("handle") else "")
        pulep = (f'<div class="pulep">PULEP {PULEP}</div>' if PULEP else "")
        if mode == "strip":
            inner = f"""
    <div class="mast"><img class="brand" src="{OKT}" alt="Oktoberfest Artesanal"></div>
    <div class="strip-data">
      <div class="city">Bogotá <span>2026</span></div>
      <div class="dot">·</div>
      <div class="when">24 de octubre</div>
      <div class="tickets"><span>Boletas próximamente</span></div>
    </div>"""
        else:
            inner = f"""
    <div class="mast">
      {sello}
      <img class="brand" src="{OKT}" alt="Oktoberfest Artesanal">
      <div class="city">Bogotá <span>2026</span></div>
    </div>
    <div class="foot">
      <div class="rule"></div>
      <div class="kicker">Save the date</div>
      <div class="when">24 de octubre</div>
      <div class="tickets"><span>Boletas próximamente</span></div>
      {handle}{pulep}
    </div>"""

    def fs(key, default=0):
        return f.get(key) or default

    return f"""<!doctype html>
<meta charset="utf-8">
<title>Oktoberfest Artesanal Bogotá 2026 · Tuboleta · {f['slug']}</title>
<style>
{FONTS_CSS}
:root{{--night:#14110B;--cream:#EEE7D6;--cream-soft:#B7AC93;--gold:#E9A72C;--ember:#E2611A;}}
*{{box-sizing:border-box;margin:0;}}
html,body{{background:#000;}}
body{{font-family:'Barlow',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}}
img{{display:block;}}
.stage{{position:relative;width:{f['w']}px;height:{f['h']}px;overflow:hidden;
  background:var(--night);color:var(--cream);}}
.photo{{position:absolute;inset:auto 0 0 0;height:{photo_h}px;{fade_css}}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{f['objpos']};
  filter:saturate(1.08) contrast(1.04);}}
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 26% at 42% 40%,rgba(244,196,90,.24),transparent 72%);}}
.veil{{position:absolute;inset:0;background:{veil};}}
.in{{position:absolute;inset:0;z-index:3;display:flex;padding:{pt}px {px}px {pb}px;}}
.mast,.foot{{display:flex;flex-direction:column;}}
{layout}
.sello{{height:{fs('sello')}px;width:auto;opacity:.95;filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));}}
.brand{{width:{fs('brand')}px;height:auto;margin-top:{round(gap*1.2)}px;
  filter:drop-shadow(0 10px 30px rgba(0,0,0,.55));}}
.city{{margin-top:{round(gap*.6)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:700;font-size:{fs('city')}px;line-height:.9;letter-spacing:.085em;
  text-transform:uppercase;color:var(--gold);text-shadow:0 6px 34px rgba(0,0,0,.6);}}
.city span{{color:var(--cream);}}
.rule{{width:{round(min(f['w'],f['h'])*0.13)}px;height:3px;background:var(--gold);border-radius:2px;}}
.kicker{{margin-top:{round(gap*.8)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{fs('kicker')}px;letter-spacing:.34em;text-transform:uppercase;
  color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.8);}}
.when{{margin-top:{round(gap*.35)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:700;font-size:{fs('when')}px;line-height:1;letter-spacing:.05em;
  text-transform:uppercase;color:var(--cream);text-shadow:0 5px 30px rgba(0,0,0,.85);}}
.tickets{{margin-top:{round(gap*.9)}px;display:inline-flex;align-items:center;
  background:var(--gold);color:#2A1B06;border-radius:999px;padding:{f.get('pill_pad','16px 28px')};
  box-shadow:0 22px 54px -18px rgba(233,167,44,.95);}}
.tickets span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:{fs('pill')}px;
  font-weight:700;letter-spacing:.13em;text-transform:uppercase;white-space:nowrap;}}
.handle{{margin-top:{gap}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;
  font-size:{fs('handle')}px;letter-spacing:.14em;text-transform:uppercase;color:var(--cream-soft);}}
.pulep{{margin-top:{round(gap*.5)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{max(12,round(fs('handle',16)*.8))}px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--cream-soft);}}
.strip-data{{display:flex;align-items:center;gap:{round(gap*.8)}px;}}
.strip-data .city,.strip-data .when{{margin:0;}}
.strip-data .tickets{{margin:0 0 0 {round(gap*.4)}px;}}
.dot{{font-size:{fs('when')}px;color:var(--gold);line-height:1;opacity:.7;}}
{wm_css}
</style>
<div class="stage">
  <div class="photo"><img src="{HERO}" alt="Festival Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div>
  <div class="veil"></div>
  {watermark}
  <div class="in">{inner}
  </div>
</div>
"""


def render(f: dict) -> pathlib.Path:
    out_dir = OUT / f["group"]
    out_dir.mkdir(parents=True, exist_ok=True)
    src = BUILD / f"tuboleta-{f['group']}-{f['slug']}.html"
    png = BUILD / f"tuboleta-{f['slug']}.png"
    src.write_text(page(f), encoding="utf-8")

    cmd = [CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1", f"--window-size={f['w']},{f['h']}",
           "--virtual-time-budget=6000", f"--screenshot={png}", src.as_uri()]
    if NEW_HEADLESS:
        cmd.insert(1, "--headless=new")
    subprocess.run(cmd, check=True, capture_output=True)

    with Image.open(png) as im:
        assert im.size == (f["w"], f["h"]), f"{f['slug']}: salió {im.size}"
        rgb = im.convert("RGB")
        px = rgb.load()
        band = next((f["h"] - 1 - y for y in range(f["h"] - 1, -1, -1)
                     if any(sum(px[x, y]) > 12 for x in range(0, f["w"], 40))), f["h"])
        assert band < 8, f"{f['slug']}: {band}px negros al pie"

        jpg = out_dir / f"{f['slug']}.jpg"
        cap = f.get("max_kb", MAX_KB)
        for q in range(92, 40, -4):
            rgb.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
            if jpg.stat().st_size <= cap * 1024:
                break
    return jpg


def build_logo() -> pathlib.Path:
    out_dir = OUT / "logo"
    out_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(AS / "okt-logo.png").convert("RGBA") as logo:
        _, _, _, a = logo.split()
        gray = ImageOps.grayscale(logo.convert("RGB"))
        bw = Image.merge("RGBA", (gray, gray, gray, a))
        bw = bw.crop(bw.getbbox())
        bw.thumbnail((500, 250), Image.LANCZOS)
    out = out_dir / "logo-oktoberfest-artesanal-byn-500x250.png"
    bw.save(out, "PNG", optimize=True)
    return out


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    print(f"Render con: {CHROME.split('/')[-1]}\n")
    for f in FORMATS:
        jpg = render(f)
        with Image.open(jpg) as im:
            size = im.size
        print(f"{f['group']:20} {jpg.name:34} {size[0]}x{size[1]}  {jpg.stat().st_size/1024:.0f} KB")
    logo = build_logo()
    with Image.open(logo) as im:
        size = im.size
    print(f"{'logo':20} {logo.name:34} {size[0]}x{size[1]}  {logo.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
