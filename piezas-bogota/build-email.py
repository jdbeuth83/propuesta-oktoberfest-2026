#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email marketing · Oktoberfest Artesanal Bogotá 2026 (lanzamiento de boletería).

Genera:
  · email-hero.jpg                     — cabecera (imagen madre + marca + datos)
  · email-oktoberfest-bogota.jpg       — el correo COMPLETO como imagen (preview/adjunto)
  · email-oktoberfest-bogota.html      — HTML table-based, listo para enviar (envío masivo)

El HTML es a prueba de clientes de correo (tablas + estilos inline, botón
«bulletproof»); si las imágenes se bloquean, el texto y el botón siguen legibles.
El hero se carga desde GitHub raw (repo público).
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "email"
OUT.mkdir(parents=True, exist_ok=True)

EVENTO_URL = "https://www.tuboleta.com/es/eventos/oktoberfest-artesanal-bogota-2026"
RAW = ("https://raw.githubusercontent.com/jdbeuth83/propuesta-oktoberfest-2026/"
       "claude/tuboleta-piezas-bogota/piezas-bogota/renders/")
HERO_URL = RAW + "email/email-hero.jpg"
CAMP = ROOT / "renders" / "campana-lanzamiento"
IMG_EXP_URL = RAW + "campana-lanzamiento/carrusel-3-experiencias.jpg"
IMG_BOL_URL = RAW + "campana-lanzamiento/carrusel-2-boleteria.jpg"
FEATS = ["+40 Cervecerías", "+200 Cervezas por probar", "Artistas en vivo",
         "Gastronomía", "Experiencias inmersivas"]


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


CHROME = find_chrome()


def render(html, w, h, out, scale=2, jpg_q=90, cap_kb=700):
    src = OUT / ".build.html"; png = OUT / ".build.png"
    src.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
                    "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()],
                   check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    for q in range(jpg_q, 55, -4):
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if out.stat().st_size <= cap_kb * 1024:
            break
    return im.size


# ── Hero (cabecera del correo) ───────────────────────────────────────────────
HERO_HTML = f"""<!doctype html><meta charset="utf-8"><style>
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#14110B}}
.stage{{position:relative;width:600px;height:640px;overflow:hidden;background:#14110B;color:#EEE7D6;
  font-family:'Barlow',sans-serif}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:72% center;filter:saturate(1.1) contrast(1.03) brightness(1.1)}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,17,11,.82) 0%,rgba(20,17,11,.35) 26%,
  rgba(20,17,11,.10) 44%,rgba(10,6,2,.55) 78%,rgba(10,6,2,.92) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:34px 40px 40px}}
.sello{{height:34px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))}}
.brand{{width:340px;margin-top:12px;filter:drop-shadow(0 8px 22px rgba(0,0,0,.5))}}
.city{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:58px;line-height:.9;letter-spacing:.06em;
  text-transform:uppercase;color:#E9A72C;margin-top:8px;text-shadow:0 5px 24px rgba(0,0,0,.6)}}
.city span{{color:#EEE7D6}}
.kicker{{margin-top:auto;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:26px;letter-spacing:.16em;
  text-transform:uppercase;color:#E9A72C;text-shadow:0 3px 14px rgba(0,0,0,.85)}}
.when{{margin-top:6px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:44px;letter-spacing:.04em;
  text-transform:uppercase;color:#EEE7D6;text-shadow:0 4px 22px rgba(0,0,0,.85)}}
.place{{margin-top:4px;font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:22px;letter-spacing:.12em;
  text-transform:uppercase;color:#E9A72C}}
</style>
<div class="stage">
  <div class="photo"><img src="{HERO}"></div><div class="veil"></div>
  <div class="in">
    <img class="sello" src="{LATOMA}">
    <img class="brand" src="{OKT}">
    <div class="city">Bogotá <span>2026</span></div>
    <div class="kicker">¡Boletas a la venta!</div>
    <div class="when">Sábado 24 de octubre</div>
    <div class="place">Centro de Eventos CESAP · Bogotá</div>
  </div>
</div>"""


def feats_rows():
    out = []
    for x in FEATS:
        out.append(f"""<tr><td style="padding:7px 0;font-family:'Barlow Condensed',Arial,sans-serif;font-size:22px;
          font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:#EEE7D6">
          <span style="color:#E9A72C">&#9670;</span>&nbsp;&nbsp;{x}</td></tr>""")
    return "".join(out)


def btn(label):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" align="center"><tr>
      <td align="center" bgcolor="#E9A72C" style="border-radius:999px;">
        <a href="{EVENTO_URL}" target="_blank" style="display:inline-block;padding:17px 50px;
          font-family:'Barlow Condensed',Arial,sans-serif;font-size:23px;font-weight:700;letter-spacing:.1em;
          text-transform:uppercase;color:#2A1B06;text-decoration:none;">{label}</a></td></tr></table>"""


def img_block(src, alt):
    return f"""<tr><td style="padding:0;"><a href="{EVENTO_URL}" target="_blank">
      <img src="{src}" width="600" alt="{alt}" style="display:block;width:100%;max-width:600px;height:auto;border:0;">
    </a></td></tr>"""


def email_html(hero_src, exp_src, bol_src):
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>Oktoberfest Artesanal Bogotá 2026 · ¡Boletas a la venta!</title></head>
<body style="margin:0;padding:0;background:#0c0a06;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">¡Boletas a la venta! Oktoberfest Artesanal Bogotá 2026 · Sábado 24 de octubre · +40 cervecerías, +200 cervezas por probar, artistas en vivo y más.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0c0a06;">
<tr><td align="center" style="padding:24px 12px;">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0"
    style="width:600px;max-width:600px;background:#14110B;border-radius:16px;overflow:hidden;
    font-family:'Barlow Condensed',Arial,Helvetica,sans-serif;color:#EEE7D6;">

    {img_block(hero_src, "Oktoberfest Artesanal Bogotá 2026 · ¡Boletas a la venta! · Sábado 24 de octubre · Centro de Eventos CESAP")}

    <tr><td style="padding:28px 44px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:26px;font-weight:700;color:#EEE7D6;
        letter-spacing:.02em;line-height:1.2;">El festival cervecero más esperado<br>llega a <span style="color:#E9A72C;">Bogotá</span></div>
      <div style="font-family:Arial,sans-serif;font-size:14px;color:#B7AC93;margin-top:10px;line-height:1.5;">
        Un solo día para vivir la esencia del Oktoberfest: cerveza artesanal, música en vivo,
        gastronomía y experiencias inmersivas.</div>
    </td></tr>

    {img_block(exp_src, "Todo esto te espera: +40 cervecerías, +200 cervezas por probar, artistas en vivo, gastronomía y experiencias inmersivas")}
    {img_block(bol_src, "Boletas a la venta: Cervecero Pro, Cervecero Pro + Jarro y De Parche")}

    <tr><td style="padding:26px 44px 4px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:36px;font-weight:700;color:#E9A72C;
        letter-spacing:.02em;">Boletas desde $54.900<span style="font-size:17px;color:#B7AC93;">*</span></div>
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:18px;font-weight:600;color:#EEE7D6;
        letter-spacing:.06em;text-transform:uppercase;margin-top:2px;">Sábado 24 de octubre · Centro de Eventos CESAP · Bogotá</div>
    </td></tr>

    <tr><td align="center" style="padding:22px 44px 6px;">{btn("Comprar en Tuboleta")}</td></tr>
    <tr><td align="center" style="padding:6px 44px 4px;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:15px;font-weight:600;letter-spacing:.1em;
        text-transform:uppercase;color:#B7AC93;">en tuboleta.com</div></td></tr>

    <tr><td style="padding:22px 44px 30px;border-top:1px solid rgba(255,255,255,.08);text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:14px;letter-spacing:.1em;
        text-transform:uppercase;color:#B7AC93;">@oktoberfestartesanalbog &nbsp;·&nbsp; PULEP IZP513</div>
      <div style="font-family:Arial,sans-serif;font-size:12px;color:#8a7f68;margin-top:8px;">
        *Los valores no incluyen el servicio de Tuboleta.</div>
    </td></tr>
  </table>
  <div style="font-family:Arial,sans-serif;font-size:11px;color:#5c5442;padding:16px 20px 0;max-width:600px;">
    Recibiste este correo porque eres parte de la comunidad de La Toma Cervecera.
  </div>
</td></tr></table>
</body></html>"""


def main():
    # 1) hero
    hero_jpg = OUT / "email-hero.jpg"
    print("hero", render(HERO_HTML, 600, 640, hero_jpg, scale=2, cap_kb=300))
    # 2) correo completo como imagen (imágenes embebidas)
    full_img = OUT / "email-oktoberfest-bogota.jpg"
    html_img = email_html(du(hero_jpg, "image/jpeg"),
                          du(CAMP / "carrusel-3-experiencias.jpg", "image/jpeg"),
                          du(CAMP / "carrusel-2-boleteria.jpg", "image/jpeg"))
    # medir alto: render a ventana alta y recortar sólido inferior
    src = OUT / ".build.html"; png = OUT / ".build.png"; src.write_text(html_img, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=624,3800",
                    "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()],
                   check=True, capture_output=True)
    im = Image.open(png).convert("RGB"); px = im.load()
    bg = (12, 10, 6); end = im.height
    for y in range(im.height - 1, 0, -1):
        if any(abs(px[x, y][0]-bg[0])+abs(px[x, y][1]-bg[1])+abs(px[x, y][2]-bg[2]) > 20 for x in range(0, im.width, 40)):
            end = min(im.height, y + 40); break
    im = im.crop((0, 0, im.width, end))
    for q in range(90, 55, -4):
        im.save(full_img, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if full_img.stat().st_size <= 800 * 1024:
            break
    print("correo (imagen)", im.size, f"{full_img.stat().st_size/1024:.0f} KB")
    # 3) HTML enviable (imágenes por URL pública de GitHub raw)
    (OUT / "email-oktoberfest-bogota.html").write_text(
        email_html(HERO_URL, IMG_EXP_URL, IMG_BOL_URL), encoding="utf-8")
    print("HTML enviable escrito")


if __name__ == "__main__":
    main()
