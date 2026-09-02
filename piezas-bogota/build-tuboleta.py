#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piezas para la ficha de venta del Oktoberfest Artesanal Bogotá 2026 en Tuboleta.

Genera los formatos que exige el «Manual de piezas para publicar eventos en
Tuboleta». A diferencia del save the date, estas piezas son de la PLATAFORMA DE
VENTA: informativas, sin llamado a la acción. Comunican evento, ciudad, fecha,
lugar y los pilares del festival (+40 cervecerías, bandas en vivo, gastronomía y
talento local), más el código PULEP en todas las piezas.

Mismo Sistema de Diseño Bogotá: imagen madre a la hora dorada, paleta del ocaso,
Barlow Condensed y el logotipo blackletter en alta resolución (con contorno
blanco para fondos oscuros). Tres ejes de composición: stack, banner y strip.

Todas en JPG <500 KB a 72 dpi (galería <1 MB); el logo del ticket en PNG.
"""
import base64
import pathlib
import subprocess

from PIL import Image, ImageOps

# Assets: imagen madre y La Toma del repo; logo Oktoberfest hi-res derivado del
# design system (assets/okt-logo-hires.png, generado por make-logos.py).
ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "tuboleta-plataforma"
BUILD = OUT / ".build"

PULEP = "IZP513"
DATE = "Sábado 24 de octubre"
PLACE = "Centro de Eventos CESAP"
FEATS = ["+40 Cervecerías", "Bandas en vivo", "Gastronomía", "Talento local"]
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


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


HERO = data_uri(REPO_AS / "hero-sunset.jpg", "image/jpeg")
OKT = data_uri(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = data_uri(WORK_AS / "latoma-blanco-hires.png", "image/png")
# Logo del proveedor de boletería (solo permitido en piezas de redes sociales).
TUBOLETA = data_uri(WORK_AS / "tuboleta-blanco.png", "image/png")
TUBOLETA_WEB = "tuboleta.com"
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")


FORMATS = [
    dict(group="banner-desplegable", slug="desktop-1920x150", w=1920, h=150,
         mode="strip", pad=(20, 66, 20), objpos="center 32%",
         brand=118, city=40, when=34, handle=15),
    dict(group="banner-desplegable", slug="mobile-1920x710", w=1920, h=710,
         mode="banner", pad=(74, 120, 74), objpos="center 30%",
         sello=46, brand=480, city=84, when=70, handle=20),
    dict(group="imagen-evento", slug="imagen-evento-900x800", w=900, h=800,
         mode="stack", pad=(38, 92, 38), objpos="60% center",
         sello=44, brand=400, city=66, when=54, handle=17),
    dict(group="boleta-digital", slug="boleta-digital-900x1050", w=900, h=1050,
         mode="stack", pad=(74, 88, 74), objpos="58% center",
         sello=50, brand=440, city=74, when=60, handle=19),
    dict(group="recurso-banner", slug="recurso-banner-1000x400", w=1000, h=400,
         mode="banner", pad=(42, 60, 42), objpos="center 34%",
         sello=32, brand=320, city=52, when=46, handle=15),
    dict(group="recurso-plano", slug="recurso-plano-1080x1080", w=1080, h=1080,
         mode="stack", pad=(80, 92, 80), objpos="72% center",
         sello=54, brand=480, city=80, when=66, handle=21),
    dict(group="redes", slug="post-1080x1080", w=1080, h=1080, mode="stack",
         pad=(64, 84, 64), objpos="72% center", ticketing=True,
         sello=48, brand=430, city=72, when=58, handle=19),
    dict(group="redes", slug="story-1080x1920", w=1080, h=1920, mode="stack",
         pad=(180, 80, 230), objpos="55% center", photo_h=1400, fade=True, ticketing=True,
         sello=70, brand=600, city=100, when=84, handle=24),
    dict(group="galeria", slug="galeria-1-1000x1000", w=1000, h=1000, mode="stack",
         pad=(70, 80, 70), objpos="55% center", max_kb=MAX_KB_GALLERY,
         sello=48, brand=420, city=70, when=56, handle=18),
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

    when = f.get("when", 40)
    place_fs = round(when * 0.62)
    feats_fs = round(when * 0.46)
    meta_fs = f.get("handle") or round(when * 0.34)

    fade_css = ("""
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);"""
                if fade else "")

    if mode in ("banner", "strip"):
        veil = ("linear-gradient(90deg,rgba(10,6,2,.78) 0%,rgba(10,6,2,.38) 30%,"
                "rgba(10,6,2,.30) 58%,rgba(10,6,2,.76) 100%),"
                "linear-gradient(180deg,rgba(20,17,11,.40) 0%,transparent 40%,rgba(10,6,2,.50) 100%)")
    else:
        top_veil = ("rgba(20,17,11,.86) 0%,rgba(20,17,11,.46) 20%,rgba(20,17,11,.06) 36%,transparent 48%"
                    if fade else
                    "rgba(20,17,11,.82) 0%,rgba(20,17,11,.62) 26%,rgba(20,17,11,.34) 40%,"
                    "rgba(20,17,11,.10) 52%,transparent 66%")
        veil = (f"linear-gradient(180deg,{top_veil}),"
                "linear-gradient(0deg,rgba(10,6,2,.88) 0%,rgba(10,6,2,.70) 18%,"
                "rgba(10,6,2,.36) 40%,transparent 58%)")

    if mode == "strip":
        layout = ".in{flex-direction:row;align-items:center;justify-content:space-between;gap:%dpx;}" % (gap * 2)
    elif mode == "banner":
        layout = (".in{flex-direction:row;align-items:center;justify-content:space-between;gap:%dpx;}"
                  ".mast{align-items:flex-start;text-align:left;}"
                  ".foot{align-items:flex-end;text-align:right;}" % (gap * 2))
    else:
        layout = (".in{flex-direction:column;align-items:center;text-align:center;}"
                  ".mast,.foot{align-items:center;}.foot{margin-top:auto;}")

    feats_html = "<i>·</i>".join(f"<span>{x}</span>" for x in FEATS)

    # Ticketing: el logo del proveedor + su web, permitido solo en redes.
    ticketing = ""
    if f.get("ticketing"):
        ticketing = (f'<div class="ticketing"><span class="tk-label">Boletas en</span>'
                     f'<img class="tk-logo" src="{TUBOLETA}" alt="Tuboleta">'
                     f'<span class="tk-web">{TUBOLETA_WEB}</span></div>')

    # PULEP en la esquina inferior izquierda, al borde (excepto strip, que lo
    # lleva en su barra de datos por falta de alto).
    corner_in = round(min(f["w"], f["h"]) * 0.035)
    corner_fs = max(12, round(min(f["w"], f["h"]) * 0.019))
    pulep_corner = ("" if mode == "strip"
                    else f'<div class="pulep-corner">PULEP {PULEP}</div>')
    pulep_corner_css = (
        f".pulep-corner{{position:absolute;left:{corner_in}px;bottom:{corner_in}px;z-index:4;"
        f"font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{corner_fs}px;"
        f"letter-spacing:.16em;text-transform:uppercase;color:var(--cream);"
        f"text-shadow:0 2px 12px rgba(0,0,0,.9);}}" if mode != "strip" else "")

    if clean:
        inner = ""
        watermark = (f'<img class="wm" src="{OKT}" alt="Oktoberfest Artesanal">'
                     f'<div class="wm-meta">@oktoberfestartesanalbog</div>')
        wm_bottom = round(f["h"] * .09)
        wm_width = round(f["w"] * .44)
        wm_css = (f".wm{{position:absolute;left:50%;bottom:{wm_bottom}px;transform:translateX(-50%);"
                  f"width:{wm_width}px;height:auto;z-index:3;opacity:.97;"
                  f"filter:drop-shadow(0 10px 30px rgba(0,0,0,.55));}}"
                  f".wm-meta{{position:absolute;left:0;right:0;bottom:{round(f['h']*.045)}px;z-index:3;"
                  f"text-align:center;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;"
                  f"font-size:{round(f['w']*.022)}px;letter-spacing:.14em;text-transform:uppercase;"
                  f"color:var(--cream-soft);}}")
    else:
        watermark = ""
        wm_css = ""
        sello = (f'<img class="sello" src="{LATOMA}" alt="La Toma Cervecera">' if f.get("sello") else "")
        if mode == "strip":
            inner = f"""
    <div class="mast"><img class="brand" src="{OKT}" alt="Oktoberfest Artesanal"></div>
    <div class="strip-data">
      <div class="line1">
        <span class="city">Bogotá <b>2026</b></span><i>·</i>
        <span class="when">{DATE}</span><i>·</i>
        <span class="place">{PLACE}</span>
      </div>
      <div class="feats">{feats_html}</div>
      <div class="meta">PULEP {PULEP}</div>
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
      <div class="when">{DATE}</div>
      <div class="place">{PLACE}</div>
      <div class="feats">{feats_html}</div>
      {ticketing}
      <div class="meta">@oktoberfestartesanalbog</div>
    </div>"""

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
  filter:saturate(1.1) contrast(1.03) brightness(1.1);}}
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 26% at 42% 40%,rgba(244,196,90,.24),transparent 72%);}}
.veil{{position:absolute;inset:0;background:{veil};}}
.in{{position:absolute;inset:0;z-index:3;display:flex;padding:{pt}px {px}px {pb}px;}}
.mast,.foot{{display:flex;flex-direction:column;}}
{layout}
.sello{{height:{f.get('sello',0)}px;width:auto;opacity:.95;filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));}}
.brand{{width:{f.get('brand',400)}px;height:auto;margin-top:{round(gap*1.1)}px;
  filter:drop-shadow(0 12px 30px rgba(0,0,0,.45));}}
.city{{margin-top:{round(gap*.6)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:700;font-size:{f.get('city',60)}px;line-height:.9;letter-spacing:.085em;
  text-transform:uppercase;color:var(--gold);text-shadow:0 6px 34px rgba(0,0,0,.6);}}
.city span,.city b{{color:var(--cream);font-weight:700;}}
.rule{{width:{round(min(f['w'],f['h'])*0.12)}px;height:3px;background:var(--gold);border-radius:2px;
  margin-bottom:{round(gap*.55)}px;}}
.when{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;font-size:{when}px;
  line-height:1;letter-spacing:.05em;text-transform:uppercase;color:var(--cream);
  text-shadow:0 5px 30px rgba(0,0,0,.85);}}
.place{{margin-top:{round(gap*.32)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{place_fs}px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.85);}}
.feats{{margin-top:{round(gap*.75)}px;display:flex;flex-wrap:wrap;align-items:center;
  justify-content:center;gap:{round(gap*.5)}px;max-width:{round(f['w']*.86)}px;}}
.feats span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{feats_fs}px;
  letter-spacing:.11em;text-transform:uppercase;color:var(--cream);
  text-shadow:0 3px 16px rgba(0,0,0,.85);white-space:nowrap;}}
.feats i{{color:var(--gold);font-style:normal;font-size:{feats_fs}px;opacity:.85;}}
.meta{{margin-top:{round(gap*.6)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{meta_fs}px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--cream-soft);}}
.ticketing{{margin-top:{round(gap*.95)}px;display:flex;align-items:center;justify-content:center;
  gap:{round(gap*.5)}px;flex-wrap:wrap;}}
.tk-label{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;font-size:{round(when*.48)}px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--cream-soft);}}
.tk-logo{{height:{round(when*.72)}px;width:auto;filter:drop-shadow(0 4px 16px rgba(0,0,0,.7));}}
.tk-web{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;font-size:{round(when*.56)}px;
  letter-spacing:.05em;color:var(--cream);text-shadow:0 3px 16px rgba(0,0,0,.85);}}
/* strip */
.strip-data{{display:flex;flex-direction:column;align-items:flex-end;text-align:right;gap:{round(gap*.35)}px;}}
.strip-data .line1{{display:flex;align-items:baseline;gap:{round(gap*.55)}px;}}
.strip-data .city{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:{f.get('city',40)}px;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);}}
.strip-data .city b{{color:var(--cream);}}
.strip-data .when{{font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:{when}px;letter-spacing:.05em;text-transform:uppercase;color:var(--cream);}}
.strip-data .place{{margin:0;font-size:{round(when*.82)}px;}}
.strip-data .line1 i{{color:var(--gold);font-style:normal;opacity:.7;font-size:{round(when*.8)}px;}}
.strip-data .feats{{margin:0;justify-content:flex-end;max-width:none;}}
.strip-data .meta{{margin:0;font-size:{round((f.get('handle') or 14)*.9)}px;}}
{pulep_corner_css}
{wm_css}
</style>
<div class="stage">
  <div class="photo"><img src="{HERO}" alt="Festival Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div>
  <div class="veil"></div>
  {watermark}
  <div class="in">{inner}
  </div>
  {pulep_corner}
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
        # Calidad alta para bordes de logo limpios; baja solo lo justo si excede.
        for q in range(95, 78, -3):
            rgb.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
            if jpg.stat().st_size <= cap * 1024:
                break
    return jpg


def build_logo() -> pathlib.Path:
    """Copia el logo B&N ya derivado (make-logos.py) a la carpeta de entrega."""
    out_dir = OUT / "logo"
    out_dir.mkdir(parents=True, exist_ok=True)
    src = WORK_AS / "logo-oktoberfest-artesanal-byn-500x250.png"
    out = out_dir / "logo-oktoberfest-artesanal-byn-500x250.png"
    out.write_bytes(src.read_bytes())
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
