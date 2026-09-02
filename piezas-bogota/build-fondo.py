#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fondo de página (full-bleed) para la ficha del Oktoberfest Artesanal Bogotá 2026
en Tuboleta — versión FOTO limpia (la imagen inicial, sin banderines).

Imagen madre a la hora dorada, rayos dorados suaves desde el sol y cierre en
Noche Festival sólido (para que el repeat vertical no tenga costura). Sin texto:
el texto vive en el arte flotante y en la fila de datos de Tuboleta (en blanco).

Tuboleta lo aplica como `background-image` del <body> (`cover`, `50% 0%`).
Editable: colores/proporciones en variables CSS.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "pagina"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1600, 2800


def find_chrome():
    p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(p).exists():
        return p
    raise SystemExit("No Chrome")


HERO = f"data:image/jpeg;base64,{base64.b64encode((REPO_AS/'hero-sunset.jpg').read_bytes()).decode()}"

HTML = f"""<!doctype html>
<meta charset="utf-8"><title>Fondo · Oktoberfest Artesanal Bogotá 2026</title>
<style>
:root{{--night:#14110B;--gold:#E9A72C;--ember:#E2611A;--ray:rgba(244,196,90,.13)}}
*{{margin:0;box-sizing:border-box}} html,body{{background:var(--night)}}
.stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--night)}}
.photo{{position:absolute;left:0;right:0;top:30%;height:54%;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 66%,transparent 100%);
  mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 66%,transparent 100%)}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 42%;
  filter:saturate(1.12) contrast(1.02) brightness(1.06)}}
.rays{{position:absolute;left:50%;top:30%;width:2600px;height:2600px;transform:translate(-50%,-50%);
  background:repeating-conic-gradient(from 0deg at 50% 50%,var(--ray) 0deg 1.5deg,transparent 1.5deg 9deg);
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 4%,rgba(0,0,0,.5) 24%,transparent 58%);
  mask-image:radial-gradient(circle at 50% 50%,#000 4%,rgba(0,0,0,.5) 24%,transparent 58%);
  mix-blend-mode:screen;opacity:.85}}
.glow{{position:absolute;left:50%;top:30%;width:1400px;height:820px;transform:translate(-50%,-50%);
  background:radial-gradient(closest-side,rgba(244,196,90,.32),rgba(226,97,26,.10),transparent 72%)}}
.ocaso{{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(20,17,11,.62) 0%,rgba(20,17,11,.18) 12%,rgba(20,17,11,.04) 28%,
  rgba(20,17,11,.30) 50%,rgba(20,17,11,.80) 70%,var(--night) 84%,var(--night) 100%)}}
.vig{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 34%,transparent 52%,rgba(10,6,2,.5) 100%)}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")}}
</style>
<div class="stage">
  <div class="photo"><img src="{HERO}" alt=""></div>
  <div class="glow"></div>
  <div class="rays"></div>
  <div class="ocaso"></div>
  <div class="vig"></div>
  <div class="grain"></div>
</div>
"""


def main():
    html = OUT / "fondo-oktoberfest-bogota-2026.html"
    png = OUT / "_fondo.png"
    jpg = OUT / "fondo-oktoberfest-bogota-2026.jpg"
    html.write_text(HTML, encoding="utf-8")
    subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=6000",
                    f"--screenshot={png}", html.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    assert im.size == (W, H), im.size
    for q in range(90, 55, -3):
        im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if jpg.stat().st_size <= 700 * 1024:
            break
    print(f"fondo {im.size}  {jpg.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
