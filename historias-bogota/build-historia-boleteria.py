#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Historia 9:16 (1080x1920) — Oktoberfest Artesanal Bogotá 2026
Anuncio de boletería próximamente.

Cuatro datos y nada más: logotipo, ciudad, fecha y lugar, boletas próximamente.
Construida sobre el Sistema de Diseño Bogotá: imagen madre a la hora dorada,
paleta del ocaso, Playfair/Barlow y logotipo blackletter en monocromo crema.
"""
import base64
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
AS = ROOT / "_assets"
OUT_HTML = ROOT / "historia-boleteria.html"
OUT_PNG = ROOT / "historia-boleteria-bogota-2026.png"
CHROME = "/opt/pw-browsers/chromium"


def data_uri(name, mime):
    return f"data:{mime};base64,{base64.b64encode((AS / name).read_bytes()).decode()}"


hero = data_uri("hero-sunset.jpg", "image/jpeg")
okt = data_uri("okt-logo-crema.png", "image/png")
latoma = data_uri("latoma-blanco.png", "image/png")
fonts_css = (AS / "fonts.css").read_text(encoding="utf-8")

HTML = f"""<!doctype html>
<meta charset="utf-8">
<title>Historia · Boletería Oktoberfest Artesanal Bogotá 2026</title>
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

.stage{{position:relative;width:1080px;height:1920px;overflow:hidden;
  background:var(--night);color:var(--cream);}}

/* ── Imagen madre: hora dorada, se funde con la noche del festival ── */
.photo{{position:absolute;inset:auto 0 0 0;height:1400px;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);
  mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.45) 9%,#000 24%);}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:55% center;
  filter:saturate(1.08) contrast(1.04);}}

/* Calor del ocaso + velos de contraste, ahora mínimos: hay poca tipografía */
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 24% at 40% 41%,rgba(244,196,90,.24),transparent 72%);}}
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(20,17,11,.94) 0%,rgba(20,17,11,.60) 20%,rgba(20,17,11,.10) 36%,transparent 46%),
  linear-gradient(0deg,rgba(10,6,2,.96) 0%,rgba(10,6,2,.86) 16%,rgba(10,6,2,.40) 33%,transparent 48%);}}

.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;
  padding:186px 78px 250px;}}

/* ── Masthead: sello productor · logotipo · ciudad ── */
.sello{{align-self:flex-start;height:40px;width:auto;opacity:.92;}}
.brand{{align-self:flex-start;width:560px;height:auto;margin-top:36px;
  filter:drop-shadow(0 8px 30px rgba(0,0,0,.75));}}
.city{{margin-top:26px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:112px;line-height:.9;letter-spacing:.085em;text-transform:uppercase;color:var(--gold);
  text-shadow:0 6px 34px rgba(0,0,0,.6);}}
.city span{{color:var(--cream);}}

/* ── Cierre: cuándo, dónde y boletas ── */
.foot{{margin-top:auto;}}
.rule{{width:132px;height:3px;background:var(--gold);border-radius:2px;}}
.when{{margin-top:30px;font-family:'Barlow Condensed',Barlow,sans-serif;font-weight:700;
  font-size:84px;line-height:1;letter-spacing:.055em;text-transform:uppercase;color:var(--cream);
  text-shadow:0 5px 30px rgba(0,0,0,.8);}}
.where{{margin-top:14px;font-size:35px;line-height:1.25;color:#E4DCC8;
  text-shadow:0 3px 20px rgba(0,0,0,.8);}}
.tickets{{margin-top:40px;display:inline-flex;align-items:center;
  background:var(--gold);color:#2A1B06;border-radius:999px;padding:24px 40px;
  box-shadow:0 22px 54px -18px rgba(233,167,44,.95);}}
.tickets span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:34px;font-weight:700;
  letter-spacing:.13em;text-transform:uppercase;white-space:nowrap;}}
.handle{{margin-top:30px;font-family:'Barlow Condensed',Barlow,sans-serif;font-size:24px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--cream-soft);}}
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
      <div class="when">24 de octubre</div>
      <p class="where">Centro de Eventos CESAP</p>
      <div class="tickets"><span>Boletas próximamente</span></div>
      <div class="handle">@oktoberfestartesanalbog</div>
    </div>
  </div>
</div>
"""

OUT_HTML.write_text(HTML, encoding="utf-8")
print(f"HTML  {OUT_HTML.name}  {OUT_HTML.stat().st_size/1024:.0f} KB")

subprocess.run([
    CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--window-size=1080,1920",
    "--virtual-time-budget=6000", f"--screenshot={OUT_PNG}", OUT_HTML.as_uri(),
], check=True, capture_output=True)
print(f"PNG   {OUT_PNG.name}  {OUT_PNG.stat().st_size/1024:.0f} KB")
