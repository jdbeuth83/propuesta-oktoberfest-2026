#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Historia 9:16 (1080x1920) — Oktoberfest Artesanal Bogotá 2026
Teaser de calentamiento para el lanzamiento de boletería.

Construida sobre el Sistema de Diseño Bogotá:
imagen madre a la hora dorada, paleta del ocaso, Playfair/Barlow,
iconografía de línea y logotipo blackletter sobre plancha crema.
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
okt = data_uri("okt-logo.png", "image/png")
latoma = data_uri("latoma-blanco.png", "image/png")
fonts_css = (AS / "fonts.css").read_text(encoding="utf-8")

# Iconografía del sistema: línea simple, un solo trazo, currentColor.
STROKE = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
HOP = f'<svg viewBox="0 0 48 48" {STROKE}><path d="M24 6c6 3 9 8 9 15 0 9-6 17-9 21-3-4-9-12-9-21 0-7 3-12 9-15z"/><path d="M24 12v30M16 20l8 5 8-5M15 28l9 5 9-5M16 36l8 4 8-4"/></svg>'
BEER = f'<svg viewBox="0 0 48 48" {STROKE}><path d="M15 16h16v22a4 4 0 0 1-4 4H19a4 4 0 0 1-4-4z"/><path d="M31 20h4a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4h-4"/><path d="M15 16a5 5 0 0 1 1-8 5 5 0 0 1 8-1 5 5 0 0 1 7 2 4 4 0 0 1 0 7"/></svg>'
SUN = f'<svg viewBox="0 0 48 48" {STROKE}><circle cx="24" cy="24" r="8"/><path d="M24 4v5M24 39v5M4 24h5M39 24h5M10 10l3.5 3.5M34.5 34.5 38 38M38 10l-3.5 3.5M13.5 34.5 10 38"/></svg>'
MUSIC = f'<svg viewBox="0 0 48 48" {STROKE}><path d="M18 34V12l20-4v22"/><circle cx="14" cy="34" r="4"/><circle cx="34" cy="30" r="4"/></svg>'
BELL = f'<svg viewBox="0 0 48 48" {STROKE.replace("2", "2.6", 1)}><path d="M24 7a11 11 0 0 1 11 11v9l4 7H9l4-7v-9A11 11 0 0 1 24 7z"/><path d="M20 37a4 4 0 0 0 8 0"/></svg>'

HTML = f"""<!doctype html>
<meta charset="utf-8">
<title>Historia · Boletería Oktoberfest Artesanal Bogotá 2026</title>
<style>
{fonts_css}
:root{{
  --night:#14110B; --line:#3A3020;
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

/* Calor del ocaso + velos de contraste (regla: nunca tipografía sobre cielo limpio) */
.glow{{position:absolute;inset:0;
  background:radial-gradient(58% 24% at 40% 41%,rgba(244,196,90,.26),transparent 72%);}}
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(20,17,11,.92) 0%,rgba(20,17,11,.52) 17%,rgba(20,17,11,.08) 32%,transparent 42%),
  linear-gradient(96deg,rgba(12,8,3,.72) 0%,rgba(12,8,3,.38) 34%,rgba(12,8,3,.06) 62%,transparent 80%),
  linear-gradient(0deg,rgba(10,6,2,.96) 0%,rgba(10,6,2,.84) 13%,rgba(10,6,2,.34) 30%,transparent 46%);}}

.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;
  padding:190px 78px 252px;}}

/* ── Sello productor ── */
.top{{display:flex;align-items:center;gap:20px;}}
.top img{{height:42px;opacity:.95;}}
.top .badge{{margin-left:auto;font-family:'Barlow Condensed',Barlow,sans-serif;
  font-size:21px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#fff;
  border:1.5px solid rgba(255,255,255,.4);border-radius:999px;padding:11px 22px;background:rgba(0,0,0,.3);}}

/* ── Mensaje ── */
.msg{{margin-top:84px;}}
.picto{{display:flex;gap:26px;color:#F4D9A8;}}
.picto svg{{width:48px;height:48px;}}
.eyebrow{{margin-top:36px;font-family:'Barlow Condensed',Barlow,sans-serif;font-size:26px;font-weight:600;
  letter-spacing:.3em;text-transform:uppercase;color:var(--gold);}}
h1{{margin-top:20px;font-family:'Playfair Display',Georgia,serif;font-weight:900;
  font-size:112px;line-height:.94;letter-spacing:-.025em;
  text-shadow:0 6px 38px rgba(0,0,0,.6);}}
h1 em{{font-style:italic;color:var(--gold);}}
.lede{{margin-top:32px;max-width:660px;font-size:32px;line-height:1.46;color:#E8E1CE;
  text-shadow:0 3px 20px rgba(0,0,0,.72);}}
.lede b{{color:var(--gold);font-weight:700;}}

.cta{{margin-top:46px;display:inline-flex;align-self:flex-start;align-items:center;gap:16px;
  background:var(--gold);color:#2A1B06;border-radius:999px;padding:24px 38px;
  box-shadow:0 22px 54px -18px rgba(233,167,44,.95);}}
.cta svg{{width:36px;height:36px;}}
.cta span{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:29px;font-weight:700;
  letter-spacing:.13em;text-transform:uppercase;}}

/* ── Firma de marca ── */
.foot{{margin-top:auto;}}
.plate{{display:inline-flex;background:var(--cream);border-radius:22px;padding:26px 38px;
  box-shadow:0 26px 64px -26px rgba(0,0,0,.95);}}
.plate img{{width:452px;}}
.line{{margin-top:26px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;}}
.dt{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:25px;font-weight:700;
  letter-spacing:.13em;text-transform:uppercase;color:#fff;background:var(--ember);
  border-radius:999px;padding:13px 24px;}}
.handle{{font-family:'Barlow Condensed',Barlow,sans-serif;font-size:24px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--cream-soft);}}
</style>

<div class="stage">
  <div class="photo"><img src="{hero}" alt="Festival Oktoberfest Artesanal Bogotá a la hora dorada"></div>
  <div class="glow"></div>
  <div class="veil"></div>

  <div class="in">
    <div class="top">
      <img src="{latoma}" alt="La Toma Cervecera">
      <span class="badge">Bogotá · 2026</span>
    </div>

    <div class="msg">
      <div class="picto">{HOP}{BEER}{MUSIC}{SUN}</div>
      <div class="eyebrow">Calentando motores</div>
      <h1>La boletería<br>está <em>a punto</em><br>de abrir</h1>
      <p class="lede">5.000 personas, 45 cervecerías y música en vivo a la hora dorada.
        <b>Prepara la alarma</b> — las primeras boletas vuelan.</p>
      <div class="cta">{BELL}<span>Activa las notificaciones</span></div>
    </div>

    <div class="foot">
      <div class="plate"><img src="{okt}" alt="Oktoberfest Artesanal"></div>
      <div class="line">
        <span class="dt">24 Oct 2026 · C. E. CESAP</span>
        <span class="handle">@oktoberfestartesanalbog</span>
      </div>
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
