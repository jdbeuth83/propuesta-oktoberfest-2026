#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email marketing · Oktoberfest Artesanal X — MEDELLÍN 2026 (lanzamiento).

Medellín se vende con LA TIQUETERA (latiquetera.com) — Bogotá con Tuboleta.
SIN tabla de precios. Incluye Ladrillos por Pola y la Experiencia Rockstar (Full).

Genera: email-hero-medellin.jpg · email-oktoberfest-medellin.jpg · .html enviable.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "email"
OUT.mkdir(parents=True, exist_ok=True)
FOTO = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/fotos/escenario/F1-231_Oktober-307.jpg")

EVENTO_URL = "https://www.latiquetera.com"          # TODO: URL de la ficha del evento en La Tiquetera
ROCKSTAR_URL = EVENTO_URL                            # TODO: link específico de la Experiencia Rockstar
ROCKSTAR_PRICE = "$159.000"                          # Medellín: Full
RAW = ("https://raw.githubusercontent.com/jdbeuth83/propuesta-oktoberfest-2026/"
       "claude/tuboleta-piezas-bogota/piezas-bogota/renders/")
HERO_URL = RAW + "email/email-hero-medellin.jpg"
SELLO_URL = RAW + "email/ladrillos-por-pola-sello.png"
TIQ_URL = RAW + "email/latiquetera-crema.png"
FEATS = ["+40 Cervecerías", "+200 Cervezas por probar", "Artistas en vivo",
         "Gastronomía", "Experiencias inmersivas"]


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


PHOTO = du(FOTO, "image/jpeg")
OKTX = du(WORK_AS / "okt-logo-hires.png", "image/png")  # logo azul de Bogotá (por decisión del cliente, también en Medellín)
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
TIQ = du(WORK_AS / "latiquetera-crema.png", "image/png")
SELLO = du(WORK_AS / "ladrillos-sello.png", "image/png")
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


HERO_HTML = f"""<!doctype html><meta charset="utf-8"><style>
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#14110B}}
.stage{{position:relative;width:600px;height:640px;overflow:hidden;background:#14110B;color:#EEE7D6;font-family:'Barlow',sans-serif}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 46%;filter:saturate(1.08) contrast(1.05) brightness(1.12)}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,17,11,.80) 0%,rgba(20,17,11,.34) 26%,
  rgba(20,17,11,.14) 46%,rgba(10,6,2,.6) 78%,rgba(10,6,2,.93) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:34px 40px 40px}}
.sello{{height:34px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))}}
.brand{{width:390px;margin-top:14px;filter:drop-shadow(0 8px 22px rgba(0,0,0,.5))}}
.city{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:56px;line-height:.9;letter-spacing:.06em;
  text-transform:uppercase;color:#E9A72C;margin-top:12px;text-shadow:0 5px 24px rgba(0,0,0,.6)}}
.city span{{color:#EEE7D6}}
.kicker{{margin-top:auto;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:26px;letter-spacing:.16em;
  text-transform:uppercase;color:#E9A72C;text-shadow:0 3px 14px rgba(0,0,0,.85)}}
.when{{margin-top:6px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:44px;letter-spacing:.04em;
  text-transform:uppercase;color:#EEE7D6;text-shadow:0 4px 22px rgba(0,0,0,.85)}}
.place{{margin-top:4px;font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:22px;letter-spacing:.12em;
  text-transform:uppercase;color:#E9A72C}}
</style>
<div class="stage">
  <div class="photo"><img src="{PHOTO}"></div><div class="veil"></div>
  <div class="in">
    <img class="sello" src="{LATOMA}">
    <img class="brand" src="{OKTX}">
    <div class="city">Medellín <span>2026</span></div>
    <div class="kicker">¡Boletas a la venta!</div>
    <div class="when">Sábado 26 de septiembre</div>
    <div class="place">Parque Norte · Medellín</div>
  </div>
</div>"""


def feats_rows():
    return "".join(f"""<tr><td style="padding:8px 0;font-family:'Barlow Condensed',Arial,sans-serif;font-size:24px;
      font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:#EEE7D6">
      <span style="color:#E9A72C">&#9670;</span>&nbsp;&nbsp;{x}</td></tr>""" for x in FEATS)


def franja_ladrillos(sello_src):
    return f"""<tr><td style="padding:0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#EAE1CB" style="background:#EAE1CB;">
        <tr><td style="padding:28px 46px;text-align:center;">
          <img src="{sello_src}" width="240" alt="Ladrillos por Pola"
            style="display:block;margin:0 auto 14px;width:240px;max-width:70%;height:auto;border:0;">
          <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:24px;font-weight:700;
            color:#14110B;letter-spacing:.02em;text-transform:uppercase;">Por cada boleta, un ladrillo</div>
          <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#4a3f2a;max-width:460px;margin:10px auto 0;">
            Tu entrada aporta a la <b>reconstrucción de los hogares</b> de las familias afectadas por el
            terremoto en Chocó, Valle del Cauca y el Eje Cafetero. Junto a Bajocuerda y 3 Cordilleras
            construimos una meta de <b>22.000 ladrillos</b>. Comprar tu boleta también reconstruye.
          </div>
        </td></tr>
      </table>
    </td></tr>"""


def btn(label):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" align="center"><tr>
      <td align="center" bgcolor="#E9A72C" style="border-radius:999px;">
        <a href="{EVENTO_URL}" target="_blank" style="display:inline-block;padding:17px 46px;
          font-family:'Barlow Condensed',Arial,sans-serif;font-size:23px;font-weight:700;letter-spacing:.09em;
          text-transform:uppercase;color:#2A1B06;text-decoration:none;">{label}</a></td></tr></table>"""


def email_html(hero_src, sello_src, tiq_src):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>Oktoberfest Artesanal X · Medellín 2026 · ¡Boletas a la venta!</title></head>
<body style="margin:0;padding:0;background:#0c0a06;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">¡Boletas a la venta! Oktoberfest Artesanal Medellín 2026 · Sábado 26 de septiembre · Parque Norte · +40 cervecerías, +200 cervezas y más.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0c0a06;">
<tr><td align="center" style="padding:24px 12px;">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0"
    style="width:600px;max-width:600px;background:#14110B;border-radius:16px;overflow:hidden;
    font-family:'Barlow Condensed',Arial,Helvetica,sans-serif;color:#EEE7D6;">

    <tr><td style="padding:0;"><a href="{EVENTO_URL}" target="_blank"><img src="{hero_src}" width="600"
      alt="Oktoberfest Artesanal X Medellín 2026 · ¡Boletas a la venta! · Sábado 26 de septiembre · Parque Norte"
      style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>

    <tr><td style="padding:28px 44px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:26px;font-weight:700;color:#EEE7D6;line-height:1.2;">
        La décima edición del festival cervecero<br>vuelve a <span style="color:#E9A72C;">Medellín</span></div>
      <div style="font-family:Arial,sans-serif;font-size:14px;color:#B7AC93;margin-top:10px;line-height:1.5;">
        Un día para vivir la esencia del Oktoberfest: cerveza artesanal, música en vivo, gastronomía y experiencias inmersivas.</div>
    </td></tr>

    <tr><td style="padding:14px 66px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:16px;font-weight:600;letter-spacing:.24em;
        text-transform:uppercase;color:#E9A72C;margin-bottom:6px;">Todo esto te espera</div>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{feats_rows()}</table>
    </td></tr>

    {franja_ladrillos(sello_src)}

    <tr><td style="padding:26px 44px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:18px;font-weight:600;color:#EEE7D6;
        letter-spacing:.06em;text-transform:uppercase;">Sábado 26 de septiembre · Parque Norte · Medellín</div>
    </td></tr>

    <tr><td style="padding:8px 44px 6px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
        style="border:1px solid rgba(233,167,44,.55);border-radius:14px;background:rgba(233,167,44,.08);">
        <tr><td style="padding:18px 24px;text-align:center;">
          <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:23px;font-weight:700;
            letter-spacing:.08em;text-transform:uppercase;color:#E9A72C;">Experiencia Rockstar</div>
          <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:17px;color:#EEE7D6;margin-top:2px;">
            <b style="color:#E9A72C;">{ROCKSTAR_PRICE}*</b> &nbsp;·&nbsp; suma <b>10 ladrillos</b> por experiencia</div>
          <a href="{ROCKSTAR_URL}" target="_blank" style="display:inline-block;margin-top:10px;
            font-family:'Barlow Condensed',Arial,sans-serif;font-size:15px;font-weight:700;letter-spacing:.08em;
            text-transform:uppercase;color:#E9A72C;text-decoration:underline;">Reservar la experiencia &#8594;</a>
        </td></tr>
      </table>
    </td></tr>

    <tr><td align="center" style="padding:20px 44px 6px;">{btn("Comprar en La Tiquetera")}</td></tr>
    <tr><td align="center" style="padding:8px 44px 6px;">
      <table role="presentation" cellpadding="0" cellspacing="0"><tr>
        <td style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:15px;font-weight:600;letter-spacing:.08em;
          text-transform:uppercase;color:#B7AC93;padding-right:10px;">en</td>
        <td><img src="{tiq_src}" height="22" alt="La Tiquetera" style="display:block;height:22px;border:0;"></td>
        <td style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:15px;font-weight:700;color:#EEE7D6;padding-left:10px;">latiquetera.com</td>
      </tr></table>
    </td></tr>

    <tr><td style="padding:22px 44px 30px;border-top:1px solid rgba(255,255,255,.08);text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:14px;letter-spacing:.1em;
        text-transform:uppercase;color:#B7AC93;">@oktoberfestartesanal</div>
      <div style="font-family:Arial,sans-serif;font-size:12px;color:#8a7f68;margin-top:8px;">
        *Los valores no incluyen el servicio de La Tiquetera.</div>
    </td></tr>
  </table>
  <div style="font-family:Arial,sans-serif;font-size:11px;color:#5c5442;padding:16px 20px 0;max-width:600px;">
    Recibiste este correo porque eres parte de la comunidad de La Toma Cervecera.
  </div>
</td></tr></table></body></html>"""


def main():
    src = OUT / ".build.html"; png = OUT / ".build.png"
    # 1) hero
    hero_jpg = OUT / "email-hero-medellin.jpg"
    src.write_text(HERO_HTML, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=600,640",
                    "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    for q in range(90, 55, -4):
        im.save(hero_jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if hero_jpg.stat().st_size <= 300 * 1024:
            break
    print("hero", im.size)
    # 2) correo completo como imagen (embebido)
    full_img = OUT / "email-oktoberfest-medellin.jpg"
    src.write_text(email_html(du(hero_jpg, "image/jpeg"), SELLO, TIQ), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=624,3400",
                    "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB"); px = im.load(); bg = (12, 10, 6); end = im.height
    for y in range(im.height - 1, 0, -1):
        if any(abs(px[x, y][0]-bg[0])+abs(px[x, y][1]-bg[1])+abs(px[x, y][2]-bg[2]) > 20 for x in range(0, im.width, 40)):
            end = min(im.height, y + 40); break
    im = im.crop((0, 0, im.width, end))
    for q in range(90, 55, -4):
        im.save(full_img, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if full_img.stat().st_size <= 850 * 1024:
            break
    print("correo (imagen)", im.size, f"{full_img.stat().st_size/1024:.0f} KB")
    # 3) HTML enviable (imágenes por URL raw)
    (OUT / "email-oktoberfest-medellin.html").write_text(email_html(HERO_URL, SELLO_URL, TIQ_URL), encoding="utf-8")
    print("HTML enviable escrito")


if __name__ == "__main__":
    main()
