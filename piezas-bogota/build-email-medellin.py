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
FEATS = ["+70 Cervecerías", "+350 Cervezas por probar", "4 Escenarios en simultáneo",
         "Artistas en vivo", "Gastronomía urbana", "Atracciones del parque"]


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


PHOTO = du(FOTO, "image/jpeg")
OKTX = du(WORK_AS / "okt-logo-hires.png", "image/png")  # logo azul de Bogotá (por decisión del cliente, también en Medellín)
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
TIQ = du(WORK_AS / "latiquetera-crema.png", "image/png")
SELLO = du(WORK_AS / "ladrillos-sello.png", "image/png")
LINEUP = du(WORK_AS / "lineup-medellin.jpg", "image/jpeg")
JARRO = du(WORK_AS / "jarro-email.jpg", "image/jpeg")
FONTS_CSS = (REPO_AS / "fonts.css").read_text(encoding="utf-8")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Fotos de referencia del banco Medellín para galería y bloque Rockstar
FOTOS = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/fotos")
GAL_SRC = ["copa-vaso/F1-002_Oktober-10.jpg", "escenario/F1-009_Oktober-106.jpg",
           "gente/F1-004_Oktober-101.jpg", "cervecerias/F1-019_Oktober-115.jpg"]
ROCK_SRC = "copa-vaso/F1-057_Oktober-15.jpg"  # cerveza oscura servida en copa estrella (fuerte, clara)
GAL_URL = [RAW + f"email/med-gal-{i+1}.jpg" for i in range(4)]
ROCK_URL = RAW + "email/med-rockstar.jpg"
LINEUP_URL = RAW + "email/lineup-medellin.jpg"
JARRO_URL = RAW + "email/jarro-email.jpg"


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


ROCKSTAR_HTML = f"""<!doctype html><meta charset="utf-8"><style>
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#14110B}}
.stage{{position:relative;width:600px;height:430px;overflow:hidden;background:#14110B;color:#EEE7D6;font-family:'Barlow',sans-serif}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 45%;filter:saturate(1.1) contrast(1.05) brightness(1.05)}}
.veil{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,7,3,.92) 0%,rgba(10,7,3,.74) 44%,rgba(10,7,3,.5) 100%),
  linear-gradient(180deg,rgba(20,17,11,.5),rgba(10,6,2,.55))}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;justify-content:center;padding:40px 46px}}
.k{{font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:24px;letter-spacing:.28em;text-transform:uppercase;color:#EEE7D6}}
.big{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:74px;line-height:.92;letter-spacing:.02em;
  text-transform:uppercase;color:#E9A72C;text-shadow:0 6px 30px rgba(0,0,0,.7)}}
.price{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:46px;color:#EEE7D6;margin-top:8px}}
.price small{{font-size:20px;color:#B7AC93}}
.desc{{font-family:'Barlow',sans-serif;font-size:17px;color:#EEE7D6;margin-top:12px;max-width:420px;line-height:1.45}}
.tag{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:18px;letter-spacing:.08em;text-transform:uppercase;
  color:#E9A72C;margin-top:14px}}
</style>
<div class="stage">
  <div class="photo"><img src="{du(FOTOS / ROCK_SRC, 'image/jpeg')}"></div><div class="veil"></div>
  <div class="in">
    <div class="k">Experiencia</div>
    <div class="big">Rockstar</div>
    <div class="price">$159.000<small> *</small></div>
    <div class="desc">Acceso a la <b>Zona Rockstar</b>, manero exclusivo y lo mejor del festival — la forma premium de vivir el Oktoberfest.</div>
    <div class="tag">+ Suma 10 ladrillos por experiencia</div>
  </div>
</div>"""


ARTISTS = [["Tributo a Caifanes", "The Mills"], ["Bajo Tierra", "Tributo a Molotov"],
           ["Nepentes", "Manuel Urrego"], ["Terlete", "DJ Tobby"]]
_art_lines = "".join(
    '<div class="al">' + '<i>·</i>'.join(f'<span>{a}</span>' for a in row) + '</div>' for row in ARTISTS)

LINEUP_HTML = f"""<!doctype html><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap');
{FONTS_CSS}
*{{margin:0;box-sizing:border-box}} html,body{{background:#14110B}}
.stage{{position:relative;width:600px;height:750px;overflow:hidden;background:#14110B;color:#EEE7D6;font-family:'Barlow',sans-serif}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 60%;filter:saturate(1.06) contrast(1.04) brightness(1.02)}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,9,5,.82) 0%,rgba(12,9,5,.5) 34%,rgba(12,9,5,.55) 62%,rgba(10,6,2,.9) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:30px 34px 26px}}
.brand{{width:220px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.55))}}
.meta{{margin-top:12px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:17px;letter-spacing:.12em;
  text-transform:uppercase;color:#EEE7D6}}
.meta b{{color:#E9A72C}}
.head{{margin-top:16px;font-family:'Playfair Display',serif;font-weight:800;font-size:66px;line-height:.95;
  text-transform:uppercase;color:#EEE7D6;text-shadow:0 6px 26px rgba(0,0,0,.7)}}
.al{{font-family:'Playfair Display',serif;font-weight:700;font-size:28px;line-height:1.32;text-transform:uppercase;color:#EEE7D6;
  text-shadow:0 3px 14px rgba(0,0,0,.85)}}
.al i{{color:#E9A72C;font-style:normal;margin:0 8px}}
.more{{margin-top:8px;font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:19px;letter-spacing:.14em;
  text-transform:uppercase;color:#E9A72C}}
.foot{{margin-top:auto;display:flex;flex-direction:column;align-items:center}}
.lt{{width:150px;opacity:.95}} .tk{{margin-top:8px;font-family:'Barlow Condensed',sans-serif;font-weight:700;
  font-size:16px;letter-spacing:.1em;text-transform:uppercase;color:#EEE7D6}}
</style>
<div class="stage">
  <div class="photo"><img src="{du(FOTO,'image/jpeg')}"></div><div class="veil"></div>
  <div class="in">
    <img class="brand" src="{du(WORK_AS/'okt-logo-hires.png','image/png')}">
    <div class="meta">26 Sep 2026 <b>·</b> Parque Norte <b>·</b> Medellín</div>
    <div class="head">Kraken</div>
    <div style="margin-top:12px">{_art_lines}</div>
    <div class="more">+ Más artistas por confirmar</div>
    <div class="foot">
      <img class="lt" src="{du(WORK_AS/'latoma-blanco-hires.png','image/png')}">
      <div class="tk">Boletería en latiquetera.com</div>
    </div>
  </div>
</div>"""


def feats_rows():
    return "".join(f"""<tr><td style="padding:8px 0;font-family:'Barlow Condensed',Arial,sans-serif;font-size:24px;
      font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:#EEE7D6">
      <span style="color:#E9A72C">&#9670;</span>&nbsp;&nbsp;{x}</td></tr>""" for x in FEATS)


def gallery_block(urls):
    def cell(u, alt):
        return (f'<td width="50%" style="padding:4px;"><img src="{u}" width="292" alt="{alt}" '
                f'style="display:block;width:100%;height:auto;border-radius:10px;border:0;"></td>')
    return f"""<tr><td style="padding:10px 40px 6px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr>{cell(urls[0],"Cerveza artesanal")}{cell(urls[1],"Escenarios en vivo")}</tr>
        <tr>{cell(urls[2],"Miles de asistentes")}{cell(urls[3],"Cervecerías")}</tr>
      </table></td></tr>"""


def lineup_block(url):
    return f"""<tr><td style="padding:22px 40px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:16px;font-weight:600;letter-spacing:.24em;
        text-transform:uppercase;color:#E9A72C;margin-bottom:10px;">Line Up · Artistas confirmados</div>
      <a href="{EVENTO_URL}" target="_blank"><img src="{url}" width="600" alt="Line Up Oktoberfest Artesanal Medellín 2026: Kraken, Tributo a Caifanes, The Mills, Bajo Tierra, Tributo a Molotov, Nepentes, Lianna, Manuel Urrego, Terlete, DJ Tobby"
        style="display:block;width:100%;max-width:600px;height:auto;border-radius:12px;border:0;"></a>
    </td></tr>"""


def jarro_block(url):
    return f"""<tr><td style="padding:22px 40px 8px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
        style="background:rgba(233,167,44,.06);border:1px solid rgba(233,167,44,.35);border-radius:14px;">
        <tr>
          <td width="44%" style="padding:14px 8px 14px 16px;"><img src="{url}" width="100%" alt="Jarro X Aniversario La Toma Cervecera"
            style="display:block;width:100%;height:auto;border-radius:10px;border:0;"></td>
          <td width="56%" style="padding:14px 20px 14px 10px;">
            <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:24px;font-weight:700;letter-spacing:.04em;
              text-transform:uppercase;color:#E9A72C;line-height:1.05;">El jarro<br>X Aniversario</div>
            <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:16px;font-weight:600;color:#B7AC93;
              letter-spacing:.1em;margin-top:4px;">2016 — 2026</div>
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.55;color:#EEE7D6;margin-top:10px;">
              10 años celebrando la cultura cervecera. Llévate el <b>jarro conmemorativo</b> de la edición X — disponible con tu localidad Cervecero Pro + Jarro.</div>
          </td>
        </tr>
      </table>
    </td></tr>"""


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


def email_html(hero_src, sello_src, tiq_src, gal_urls, rock_src, lineup_src, jarro_src):
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
        El festival de cerveza artesanal<br>más grande de <span style="color:#E9A72C;">Colombia</span></div>
      <div style="font-family:Arial,sans-serif;font-size:14px;color:#B7AC93;margin-top:10px;line-height:1.55;">
        13.000 personas, <b>4 escenarios en simultáneo</b>, cerveza artesanal, música en vivo, gastronomía urbana,
        experiencias y las atracciones del Parque Norte. 12 horas de festival: 12:00 m. a 12:00 a. m.</div>
    </td></tr>

    <tr><td style="padding:14px 66px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:16px;font-weight:600;letter-spacing:.24em;
        text-transform:uppercase;color:#E9A72C;margin-bottom:6px;">Todo esto te espera</div>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{feats_rows()}</table>
    </td></tr>

    {lineup_block(lineup_src)}

    {gallery_block(gal_urls)}

    {jarro_block(jarro_src)}

    {franja_ladrillos(sello_src)}

    <tr><td style="padding:26px 44px 6px;text-align:center;">
      <div style="font-family:'Barlow Condensed',Arial,sans-serif;font-size:18px;font-weight:600;color:#EEE7D6;
        letter-spacing:.06em;text-transform:uppercase;">Sábado 26 de septiembre · Parque Norte · Medellín</div>
    </td></tr>

    <tr><td style="padding:16px 40px 6px;"><a href="{ROCKSTAR_URL}" target="_blank">
      <img src="{rock_src}" width="600" alt="Experiencia Rockstar · $159.000 · Zona Rockstar · suma 10 ladrillos"
        style="display:block;width:100%;max-width:600px;height:auto;border-radius:14px;border:0;"></a></td></tr>
    <tr><td align="center" style="padding:8px 44px 4px;">
      <table role="presentation" cellpadding="0" cellspacing="0" align="center"><tr>
        <td align="center" bgcolor="#E9A72C" style="border-radius:999px;">
          <a href="{ROCKSTAR_URL}" target="_blank" style="display:inline-block;padding:15px 40px;
            font-family:'Barlow Condensed',Arial,sans-serif;font-size:20px;font-weight:700;letter-spacing:.08em;
            text-transform:uppercase;color:#2A1B06;text-decoration:none;">Reservar la Experiencia Rockstar</a>
        </td></tr></table>
    </td></tr>

    <tr><td align="center" style="padding:18px 44px 6px;border-top:1px solid rgba(255,255,255,.06);">{btn("Comprar boleta general")}</td></tr>
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


def render_html(html, w, h, out, cap_kb):
    src = OUT / ".build.html"; png = OUT / ".build.png"; src.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={w},{h}",
                    "--virtual-time-budget=8000", f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
    return Image.open(png).convert("RGB")


def crop_square(rel, side=600):
    im = Image.open(FOTOS / rel).convert("RGB")
    s = min(im.size); im = im.crop(((im.width-s)//2, (im.height-s)//2, (im.width+s)//2, (im.height+s)//2))
    return im.resize((side, side), Image.LANCZOS)


def main():
    # 1) galería (4 fotos cuadradas)
    gal_jpg = []
    for i, rel in enumerate(GAL_SRC):
        p = OUT / f"med-gal-{i+1}.jpg"
        im = crop_square(rel, 600)
        for q in range(88, 55, -4):
            im.save(p, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
            if p.stat().st_size <= 180 * 1024:
                break
        gal_jpg.append(p)
    # 2) hero
    hero_jpg = OUT / "email-hero-medellin.jpg"
    im = render_html(HERO_HTML, 600, 640, hero_jpg, 300)
    for q in range(90, 55, -4):
        im.save(hero_jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if hero_jpg.stat().st_size <= 300 * 1024:
            break
    print("hero", im.size)
    # 3) banner Rockstar
    rock_jpg = OUT / "med-rockstar.jpg"
    im = render_html(ROCKSTAR_HTML, 600, 430, rock_jpg, 260)
    for q in range(90, 55, -4):
        im.save(rock_jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if rock_jpg.stat().st_size <= 260 * 1024:
            break
    print("rockstar", im.size)
    # 3b) Line Up (pieza propia, editable) + jarro para hospedar
    import shutil
    lineup_jpg = OUT / "lineup-medellin.jpg"
    im = render_html(LINEUP_HTML, 600, 750, lineup_jpg, 260)
    for q in range(90, 55, -4):
        im.save(lineup_jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if lineup_jpg.stat().st_size <= 260 * 1024:
            break
    print("lineup", im.size)
    shutil.copy(WORK_AS / "jarro-email.jpg", OUT / "jarro-email.jpg")
    # 4) correo completo como imagen (todo embebido)
    full_img = OUT / "email-oktoberfest-medellin.jpg"
    gal_du = [du(p, "image/jpeg") for p in gal_jpg]
    im = render_html(email_html(du(hero_jpg, "image/jpeg"), SELLO, TIQ, gal_du, du(rock_jpg, "image/jpeg"),
                                du(lineup_jpg, "image/jpeg"), JARRO),
                     624, 5400, full_img, 980)
    px = im.load(); bg = (12, 10, 6); end = im.height
    for y in range(im.height - 1, 0, -1):
        if any(abs(px[x, y][0]-bg[0])+abs(px[x, y][1]-bg[1])+abs(px[x, y][2]-bg[2]) > 20 for x in range(0, im.width, 40)):
            end = min(im.height, y + 40); break
    im = im.crop((0, 0, im.width, end))
    for q in range(90, 50, -4):
        im.save(full_img, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if full_img.stat().st_size <= 950 * 1024:
            break
    print("correo (imagen)", im.size, f"{full_img.stat().st_size/1024:.0f} KB")
    # 5) HTML enviable (imágenes por URL raw de GitHub)
    (OUT / "email-oktoberfest-medellin.html").write_text(
        email_html(HERO_URL, SELLO_URL, TIQ_URL, GAL_URL, ROCK_URL, LINEUP_URL, JARRO_URL), encoding="utf-8")
    print("HTML enviable escrito")


if __name__ == "__main__":
    main()
