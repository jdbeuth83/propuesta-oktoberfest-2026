#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Save the date · Oktoberfest Artesanal Bogotá 2026

Genera la misma pieza en los tres formatos que usa la cuenta:
  · historia 9:16  (1080 x 1920)
  · post 4:5       (1080 x 1350) — formato principal de feed
  · post 1:1       (1080 x 1080)

Contenido: dos marcas (Oktoberfest Artesanal y La Toma Cervecera), la ciudad
—que separa esta edición de la de Medellín— y tres datos: save the date,
24 de octubre y boletas próximamente. Sin locación todavía.

Construida sobre el Sistema de Diseño Bogotá: imagen madre a la hora dorada,
paleta del ocaso, Barlow Condensed y el logotipo blackletter original.
"""
import base64
import pathlib
import subprocess

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
AS = ROOT / "_assets"
# El Chromium completo en modo headless deja un viewport ~87 px más bajo que la
# ventana pedida y recorta el borde inferior del lienzo. El headless_shell
# respeta --window-size al pixel, así que el render sale exacto.
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

CENTERED = True  # eje de composición; False lo alinea al margen izquierdo

# Cada formato lleva su propia escala tipográfica y su propio encuadre: la foto
# es apaisada, así que a menor altura de lienzo el recorte se corre a la derecha
# para no cortar el inflable de cerveza por la mitad.
#
# `fade` funde el borde superior de la foto contra la noche: solo cabe en 9:16,
# donde sobra alto. En feed la foto va a sangre completa —si no, el atardecer se
# pierde justo en la zona que se desvanece— y el contraste lo pone el velo.
FORMATS = [
    dict(slug="historia-9x16", w=1080, h=1920, pad=(186, 78, 250),
         photo_h=1400, obj="55%", fade=True, sello=74, brand=600, city=112,
         kicker=30, when=96, pill=34, pill_pad="24px 40px", handle=24),
    dict(slug="post-4x5", w=1080, h=1350, pad=(92, 86, 92),
         photo_h=1350, obj="58%", fade=False, sello=58, brand=480, city=88,
         kicker=25, when=76, pill=28, pill_pad="20px 34px", handle=21),
    dict(slug="post-1x1", w=1080, h=1080, pad=(76, 86, 76),
         photo_h=1080, obj="72%", fade=False, sello=50, brand=420, city=76,
         kicker=22, when=64, pill=25, pill_pad="18px 30px", handle=19),
]


def data_uri(name, mime):
    return f"data:{mime};base64,{base64.b64encode((AS / name).read_bytes()).decode()}"


hero = data_uri("hero-sunset.jpg", "image/jpeg")
okt = data_uri("okt-logo.png", "image/png")
latoma = data_uri("latoma-blanco.png", "image/png")
fonts_css = (AS / "fonts.css").read_text(encoding="utf-8")


def page(f) -> str:
    axis = "center" if CENTERED else "flex-start"
    align = "center" if CENTERED else "left"
    pt, px, pb = f["pad"]
    # El eje centrado deja la fecha sobre la carpa: pide un poco más de velo abajo.
    bottom_veil = "rgba(10,6,2,.48) 34%" if CENTERED else "rgba(10,6,2,.40) 33%"
    gap = round(f["h"] * 0.017)  # respiro proporcional entre bloques

    fade = ("""
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);"""
            if f["fade"] else "")
    # Sin fundido, el masthead cae sobre el cielo del atardecer: el velo superior
    # es entonces la capa de contraste que exige el sistema.
    top_veil = ("rgba(20,17,11,.94) 0%,rgba(20,17,11,.60) 20%,rgba(20,17,11,.10) 36%,transparent 46%"
                if f["fade"] else
                "rgba(20,17,11,.92) 0%,rgba(20,17,11,.80) 26%,rgba(20,17,11,.52) 40%,"
                "rgba(20,17,11,.18) 52%,transparent 64%")

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

/* ── Imagen madre: hora dorada, se funde con la noche del festival ── */
.photo{{position:absolute;inset:auto 0 0 0;height:{f['photo_h']}px;{fade}}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:{f['obj']} center;
  filter:saturate(1.08) contrast(1.04);}}

/* Calor del ocaso + velos de contraste, mínimos: hay muy poca tipografía */
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 24% at 40% 41%,rgba(244,196,90,.24),transparent 72%);}}
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,{top_veil}),
  linear-gradient(0deg,rgba(10,6,2,.96) 0%,rgba(10,6,2,.86) 16%,{bottom_veil},transparent 48%);}}

.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;
  align-items:{axis};text-align:{align};padding:{pt}px {px}px {pb}px;}}

/* ── Marcas ── */
.sello{{height:{f['sello']}px;width:auto;opacity:.95;
  filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));}}
/* Logotipo original: azul + café con su contorno blanco. La sombra solo lo
   despega de la foto, no reemplaza al contorno. */
.brand{{width:{f['brand']}px;height:auto;margin-top:{gap * 2}px;
  filter:drop-shadow(0 10px 30px rgba(0,0,0,.55));}}
.city{{margin-top:{gap}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:{f['city']}px;line-height:.9;letter-spacing:.085em;text-transform:uppercase;
  color:var(--gold);text-shadow:0 6px 34px rgba(0,0,0,.6);}}
.city span{{color:var(--cream);}}

/* ── Cierre: save the date y boletas ── */
.foot{{margin-top:auto;display:flex;flex-direction:column;align-items:{axis};}}
.rule{{width:{round(f['w'] * 0.122)}px;height:3px;background:var(--gold);border-radius:2px;}}
.kicker{{margin-top:{gap + 4}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;
  font-size:{f['kicker']}px;letter-spacing:.34em;text-transform:uppercase;color:var(--gold);
  text-shadow:0 3px 18px rgba(0,0,0,.8);}}
.when{{margin-top:{round(gap * .5)}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:{f['when']}px;line-height:1;letter-spacing:.05em;text-transform:uppercase;
  color:var(--cream);text-shadow:0 5px 30px rgba(0,0,0,.85);}}
.tickets{{margin-top:{round(gap * 1.4)}px;display:inline-flex;align-items:center;
  background:var(--gold);color:#2A1B06;border-radius:999px;padding:{f['pill_pad']};
  box-shadow:0 22px 54px -18px rgba(233,167,44,.95);}}
.tickets span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:{f['pill']}px;font-weight:700;
  letter-spacing:.13em;text-transform:uppercase;white-space:nowrap;}}
.handle{{margin-top:{gap}px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:600;
  font-size:{f['handle']}px;letter-spacing:.14em;text-transform:uppercase;color:var(--cream-soft);}}
</style>

<div class="stage">
  <div class="photo"><img src="{hero}" alt="Festival Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div>
  <div class="veil"></div>

  <div class="in">
    <img class="sello" src="{latoma}" alt="La Toma Cervecera">
    <img class="brand" src="{okt}" alt="Oktoberfest Artesanal">
    <div class="city">Bogotá <span>2026</span></div>

    <div class="foot">
      <div class="rule"></div>
      <div class="kicker">Save the date</div>
      <div class="when">24 de octubre</div>
      <div class="tickets"><span>Boletas próximamente</span></div>
      <div class="handle">@oktoberfestartesanalbog</div>
    </div>
  </div>
</div>
"""


for f in FORMATS:
    out_html = ROOT / f"savethedate-{f['slug']}.html"
    out_png = ROOT / f"savethedate-{f['slug']}.png"
    out_html.write_text(page(f), encoding="utf-8")
    subprocess.run([
        CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={f['w']},{f['h']}",
        "--virtual-time-budget=6000", f"--screenshot={out_png}", out_html.as_uri(),
    ], check=True, capture_output=True)

    with Image.open(out_png) as im:
        assert im.size == (f["w"], f["h"]), f"{out_png.name}: salió {im.size}"
        # El lienzo debe llegar hasta abajo: una franja negra al pie delataría un
        # viewport más corto que la ventana y un recorte silencioso del diseño.
        px = im.convert("RGB").load()
        band = next((f["h"] - 1 - y for y in range(f["h"] - 1, -1, -1)
                     if any(sum(px[x, y]) > 12 for x in range(0, f["w"], 40))), f["h"])
        assert band < 8, f"{out_png.name}: {band} px negros al pie, el lienzo quedó recortado"

    print(f"{out_png.name}  {f['w']}x{f['h']}  {out_png.stat().st_size/1024:.0f} KB")
