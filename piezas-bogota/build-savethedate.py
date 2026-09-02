#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Save the date · Oktoberfest Artesanal Bogotá 2026

Genera la misma pieza en todos los formatos que pide el lanzamiento: redes,
página de la tiquetera y sitio web.

Contenido: dos marcas (Oktoberfest Artesanal y La Toma Cervecera), la ciudad
—que separa esta edición de la de Medellín— y tres datos: save the date,
24 de octubre y boletas próximamente. Sin locación todavía.

Dos ejes de composición según la forma del lienzo:
  · stack  — vertical y cuadrado: marca arriba, datos abajo, todo centrado.
  · banner — apaisado: marca a la izquierda, datos a la derecha, la foto
             respira en el centro.

Construida sobre el Sistema de Diseño Bogotá: imagen madre a la hora dorada,
paleta del ocaso, Barlow Condensed y el logotipo blackletter original.
"""
import base64
import pathlib
import subprocess

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
AS = ROOT / "_assets"
BUILD = ROOT / ".build"
RENDERS = ROOT / "renders"
# El Chromium completo en modo headless deja un viewport ~87 px más bajo que la
# ventana pedida y recorta el borde inferior del lienzo. El headless_shell
# respeta --window-size al pixel, así que el render sale exacto.
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# Escala tipográfica y encuadre por formato. La foto es apaisada: en lienzos
# verticales el recorte se corre a la derecha lo necesario para no cortar el
# inflable de cerveza por la mitad, y en los anchos se ajusta el eje vertical
# para conservar el sol y la carpa de lúpulo.
#
# `fade` funde el borde superior de la foto contra la noche: solo cabe donde
# sobra alto (9:16). En el resto la foto va a sangre completa —si no, el
# atardecer se pierde justo en la zona que se desvanece— y el contraste lo pone
# el velo, la capa que el sistema exige antes de poner tipografía sobre cielo.
FORMATS = [
    # ── Redes ────────────────────────────────────────────────────────────────
    dict(group="social", slug="post-4x5", w=1080, h=1350, mode="stack",
         pad=(92, 86, 92), objpos="58% center", fade=False,
         sello=58, brand=480, city=88, kicker=25, when=76, pill=28,
         pill_pad="20px 34px", handle=21),
    dict(group="social", slug="post-1x1", w=1080, h=1080, mode="stack",
         pad=(76, 86, 76), objpos="72% center", fade=False,
         sello=50, brand=420, city=76, kicker=22, when=64, pill=25,
         pill_pad="18px 30px", handle=19),
    dict(group="social", slug="historia-9x16", w=1080, h=1920, mode="stack",
         pad=(186, 78, 250), objpos="55% center", fade=True, photo_h=1400,
         sello=74, brand=600, city=112, kicker=30, when=96, pill=34,
         pill_pad="24px 40px", handle=24),

    # ── Tiquetera ────────────────────────────────────────────────────────────
    dict(group="tiquetera", slug="banner-1920x600", w=1920, h=600, mode="banner",
         pad=(70, 96, 70), objpos="center 30%", fade=False,
         sello=44, brand=430, city=78, kicker=21, when=70, pill=26,
         pill_pad="18px 30px", handle=18),
    dict(group="tiquetera", slug="cuadrado-1200x1200", w=1200, h=1200, mode="stack",
         pad=(84, 96, 84), objpos="72% center", fade=False,
         sello=56, brand=470, city=84, kicker=24, when=72, pill=28,
         pill_pad="19px 32px", handle=21),
    dict(group="tiquetera", slug="card-800x600", w=800, h=600, mode="stack",
         pad=(44, 52, 44), objpos="38% center", fade=False,
         sello=32, brand=290, city=52, kicker=15, when=46, pill=18,
         pill_pad="12px 20px", handle=None),

    # ── Web ──────────────────────────────────────────────────────────────────
    dict(group="web", slug="hero-2560x1080", w=2560, h=1080, mode="banner",
         pad=(120, 150, 120), objpos="center 25%", fade=False,
         sello=64, brand=660, city=120, kicker=32, when=112, pill=38,
         pill_pad="26px 44px", handle=26),
    dict(group="web", slug="hero-mobile-1080x1440", w=1080, h=1440, mode="stack",
         pad=(96, 86, 96), objpos="56% center", fade=False,
         sello=58, brand=500, city=92, kicker=26, when=80, pill=29,
         pill_pad="21px 35px", handle=21),
    dict(group="web", slug="og-1200x630", w=1200, h=630, mode="banner",
         pad=(56, 72, 56), objpos="center 40%", fade=False,
         sello=36, brand=340, city=62, kicker=17, when=56, pill=21,
         pill_pad="14px 24px", handle=None),
]


def data_uri(name, mime):
    return f"data:{mime};base64,{base64.b64encode((AS / name).read_bytes()).decode()}"


hero = data_uri("hero-sunset.jpg", "image/jpeg")
okt = data_uri("okt-logo.png", "image/png")
latoma = data_uri("latoma-blanco.png", "image/png")
fonts_css = (AS / "fonts.css").read_text(encoding="utf-8")


def page(f) -> str:
    banner = f["mode"] == "banner"
    pt, px, pb = f["pad"]
    # El respiro se mide contra el lado corto para que no se dispare en los
    # lienzos muy apaisados.
    gap = round(min(f["w"], f["h"]) * 0.028)

    fade = ("""
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);"""
            if f["fade"] else "")

    if banner:
        # La tipografía se ancla en los bordes: el velo oscurece izquierda y
        # derecha y deja el centro de la foto a plena luz.
        veil = """
  linear-gradient(90deg,rgba(10,6,2,.88) 0%,rgba(10,6,2,.52) 30%,rgba(10,6,2,.44) 58%,rgba(10,6,2,.86) 100%),
  linear-gradient(180deg,rgba(20,17,11,.55) 0%,transparent 38%,rgba(10,6,2,.62) 100%)"""
        layout = f"""
.in{{flex-direction:row;align-items:center;justify-content:space-between;gap:{gap * 2}px;}}
.mast{{align-items:flex-start;text-align:left;}}
.foot{{align-items:flex-end;text-align:right;}}"""
    else:
        top_veil = ("rgba(20,17,11,.94) 0%,rgba(20,17,11,.60) 20%,rgba(20,17,11,.10) 36%,transparent 46%"
                    if f["fade"] else
                    "rgba(20,17,11,.92) 0%,rgba(20,17,11,.80) 26%,rgba(20,17,11,.52) 40%,"
                    "rgba(20,17,11,.18) 52%,transparent 64%")
        veil = f"""
  linear-gradient(180deg,{top_veil}),
  linear-gradient(0deg,rgba(10,6,2,.96) 0%,rgba(10,6,2,.86) 16%,rgba(10,6,2,.48) 34%,transparent 48%)"""
        layout = """
.in{flex-direction:column;align-items:center;text-align:center;}
.mast,.foot{align-items:center;}
.foot{margin-top:auto;}"""

    handle = (f'<div class="handle">@oktoberfestartesanalbog</div>'
              if f["handle"] else "")
    handle_css = (f""".handle{{margin-top:{gap}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{f['handle']}px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--cream-soft);}}""" if f["handle"] else "")

    return f"""<!doctype html>
<meta charset="utf-8">
<title>Save the date · Oktoberfest Artesanal Bogotá 2026 · {f['slug']}</title>
<style>
{fonts_css}
:root{{
  --night:#14110B;
  --cream:#EEE7D6; --cream-soft:#B7AC93;
  --gold:#E9A72C; --ember:#E2611A;
}}
*{{box-sizing:border-box;margin:0;}}
html,body{{background:#000;}}
body{{font-family:'Barlow',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}}
img{{display:block;}}

.stage{{position:relative;width:{f['w']}px;height:{f['h']}px;overflow:hidden;
  background:var(--night);color:var(--cream);}}

/* ── Imagen madre: hora dorada ── */
.photo{{position:absolute;inset:auto 0 0 0;height:{f.get('photo_h', f['h'])}px;{fade}}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{f['objpos']};
  filter:saturate(1.08) contrast(1.04);}}
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 26% at 42% 40%,rgba(244,196,90,.24),transparent 72%);}}
.veil{{position:absolute;inset:0;background:{veil};}}

.in{{position:absolute;inset:0;z-index:3;display:flex;padding:{pt}px {px}px {pb}px;}}
.mast,.foot{{display:flex;flex-direction:column;}}
{layout}

/* ── Marcas ── */
.sello{{height:{f['sello']}px;width:auto;opacity:.95;
  filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));}}
/* Logotipo original: azul + café con su contorno blanco. La sombra solo lo
   despega de la foto, no reemplaza al contorno. */
.brand{{width:{f['brand']}px;height:auto;margin-top:{round(gap * 1.2)}px;
  filter:drop-shadow(0 10px 30px rgba(0,0,0,.55));}}
.city{{margin-top:{round(gap * .6)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:700;font-size:{f['city']}px;line-height:.9;letter-spacing:.085em;
  text-transform:uppercase;color:var(--gold);text-shadow:0 6px 34px rgba(0,0,0,.6);}}
.city span{{color:var(--cream);}}

/* ── Cierre: save the date y boletas ── */
.rule{{width:{round(min(f['w'], f['h']) * 0.13)}px;height:3px;background:var(--gold);border-radius:2px;}}
.kicker{{margin-top:{round(gap * .8)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:600;font-size:{f['kicker']}px;letter-spacing:.34em;text-transform:uppercase;
  color:var(--gold);text-shadow:0 3px 18px rgba(0,0,0,.8);}}
.when{{margin-top:{round(gap * .35)}px;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-weight:700;font-size:{f['when']}px;line-height:1;letter-spacing:.05em;
  text-transform:uppercase;color:var(--cream);text-shadow:0 5px 30px rgba(0,0,0,.85);}}
.tickets{{margin-top:{round(gap * .9)}px;display:inline-flex;align-items:center;
  background:var(--gold);color:#2A1B06;border-radius:999px;padding:{f['pill_pad']};
  box-shadow:0 22px 54px -18px rgba(233,167,44,.95);}}
.tickets span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:{f['pill']}px;
  font-weight:700;letter-spacing:.13em;text-transform:uppercase;white-space:nowrap;}}
{handle_css}
</style>

<div class="stage">
  <div class="photo"><img src="{hero}" alt="Festival Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div>
  <div class="veil"></div>

  <div class="in">
    <div class="mast">
      <img class="sello" src="{latoma}" alt="La Toma Cervecera">
      <img class="brand" src="{okt}" alt="Oktoberfest Artesanal">
      <div class="city">Bogotá <span>2026</span></div>
    </div>
    <div class="foot">
      <div class="rule"></div>
      <div class="kicker">Save the date</div>
      <div class="when">24 de octubre</div>
      <div class="tickets"><span>Boletas próximamente</span></div>
      {handle}
    </div>
  </div>
</div>
"""


BUILD.mkdir(exist_ok=True)
for f in FORMATS:
    out_dir = RENDERS / f["group"]
    out_dir.mkdir(parents=True, exist_ok=True)
    src = BUILD / f"savethedate-{f['group']}-{f['slug']}.html"
    out_png = out_dir / f"savethedate-{f['slug']}.png"
    src.write_text(page(f), encoding="utf-8")

    subprocess.run([
        CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={f['w']},{f['h']}",
        "--virtual-time-budget=6000", f"--screenshot={out_png}", src.as_uri(),
    ], check=True, capture_output=True)

    with Image.open(out_png) as im:
        assert im.size == (f["w"], f["h"]), f"{out_png.name}: salió {im.size}"
        # Una franja negra al pie delataría un viewport más corto que la ventana
        # y un recorte silencioso del diseño.
        px_ = im.convert("RGB").load()
        band = next((f["h"] - 1 - y for y in range(f["h"] - 1, -1, -1)
                     if any(sum(px_[x, y]) > 12 for x in range(0, f["w"], 40))), f["h"])
        assert band < 8, f"{out_png.name}: {band} px negros al pie, el lienzo quedó recortado"

    print(f"{f['group']}/{out_png.name}  {f['w']}x{f['h']}  {out_png.stat().st_size/1024:.0f} KB")
