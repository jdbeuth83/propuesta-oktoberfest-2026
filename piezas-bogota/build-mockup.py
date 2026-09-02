#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mockup EDITABLE de la ficha completa del evento en Tuboleta con el look propuesto:
fondo full-bleed (foto atardecer, sin banderines) + arte hero + toda la
información estructurada como en la referencia BogotaEats:

  Datos → Entradas (Categoría / Etapa / Precio + Servicio / Aforo) →
  Información adicional (descripción + servicios) → Responsable.

Datos reales tomados de la ficha de Tuboleta del evento.
Renderiza la página completa a PNG y deja el HTML editable.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
REPO_AS = ROOT / "_assets"
WORK_AS = ROOT / "_assets"
OUT = ROOT / "renders" / "pagina"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1440, 4600
NIGHT = (20, 17, 11)


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


FONDO = du(OUT / "fondo-oktoberfest-bogota-2026.jpg", "image/jpeg")
OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")
LATOMA = du(WORK_AS / "latoma-blanco-hires.png", "image/png")
TUBO = du(WORK_AS / "tuboleta-blanco.png", "image/png")

# ── Entradas reales (Categoría, [(etapa, precio, servicio, aforo)]) ──
ENTRADAS = [
    ("Cervecero Pro", [
        ("Preventa", "$54.900", "$5.300", "200"), ("Etapa 1", "$59.900", "$5.300", "300"),
        ("Etapa 2", "$74.900", "$6.700", "300"), ("Etapa 3", "$86.900", "$8.200", "750"),
        ("Etapa 4", "$99.900", "$8.200", "750"), ("Etapa 5", "$112.900", "$9.600", "750"),
        ("Precio Full", "$124.900", "$9.600", "750")]),
    ("Cervecero Pro + Jarro", [
        ("Preventa", "$122.900", "$5.300", "200"), ("Precio Full", "$192.900", "$9.600", "400")]),
    ("De Parche", [
        ("Preventa", "$36.900", "$5.300", "100"), ("Etapa 1", "$46.900", "$6.700", "100"),
        ("Etapa 2", "$56.900", "$8.200", "100"), ("Precio Full", "$66.900", "$9.600", "300")]),
]

SERVICIOS = [
    "Cervecerías y diferentes estilos de cerveza artesanal.",
    "Música y entretenimiento en vivo.",
    "Una variada oferta gastronómica.",
    "Activaciones y experiencias de marca.",
    "Espacios diseñados para compartir y vivir toda la esencia del Oktoberfest.",
]


def find_chrome():
    p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(p).exists():
        return p
    raise SystemExit("No Chrome")


def entradas_html():
    cards = []
    for name, rows in ENTRADAS:
        trs = "".join(
            f'<tr><td class="et">{et}</td><td class="pr">{pr} <span>+ {sv} servicio</span></td>'
            f'<td class="af">{af}</td></tr>' for et, pr, sv, af in rows)
        cards.append(f'''<div class="cat">
          <div class="cat-h">{name}</div>
          <table><thead><tr><th>Etapa</th><th>Precio + servicio</th><th>Aforo</th></tr></thead>
          <tbody>{trs}</tbody></table></div>''')
    return "".join(cards)


HTML = f"""<!doctype html>
<meta charset="utf-8"><title>Oktoberfest Artesanal Bogotá 2026 · Tuboleta (propuesta)</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;600;700&display=swap');
:root{{--night:#14110B;--gold:#E9A72C;--ember:#E2611A;--cream:#EEE7D6;--soft:#B7AC93;--panel:rgba(18,15,10,.72)}}
*{{margin:0;box-sizing:border-box;font-family:'Barlow',system-ui,sans-serif}}
body{{width:{W}px;background:#14110B url('{FONDO}') no-repeat 50% 0/cover;color:var(--cream)}}
.bc{{font-family:'Barlow Condensed',sans-serif}}
.hdr{{background:#2f57b8;padding:22px 48px;display:flex;align-items:center;gap:30px}}
.hdr img{{height:30px}} .nav{{color:#fff;font-weight:600;font-size:15px;opacity:.95}}
.acc{{margin-left:auto;color:#fff;font-weight:600;font-size:14px;opacity:.9}}
.search{{background:#3f66c6;padding:0 48px 24px}}
.searchbar{{background:#fff;border-radius:10px;height:50px;display:flex;align-items:center;
  padding:0 20px;color:#8a8a8a;font-weight:600;max-width:1120px;margin:0 auto}}
.searchbar .go{{margin-left:auto;background:var(--gold);width:60px;height:50px;border-radius:0 10px 10px 0;margin-right:-20px}}
.wrap{{max-width:1180px;margin:0 auto;padding:44px 30px 70px;text-align:center}}
/* Hero */
.sello{{height:52px;filter:drop-shadow(0 6px 20px rgba(0,0,0,.6))}}
.brand{{width:640px;max-width:86%;margin:14px auto 0;display:block;filter:drop-shadow(0 14px 34px rgba(0,0,0,.5))}}
.city{{font-family:'Barlow Condensed';font-weight:700;font-size:116px;line-height:.9;letter-spacing:.06em;
  text-transform:uppercase;color:var(--gold);margin-top:12px;text-shadow:0 8px 40px rgba(0,0,0,.6)}}
.city b{{color:var(--cream)}}
.rule{{width:180px;height:4px;background:var(--gold);border-radius:2px;margin:24px auto 0}}
.when{{font-family:'Barlow Condensed';font-weight:700;font-size:62px;letter-spacing:.05em;text-transform:uppercase;
  color:var(--cream);margin-top:16px;text-shadow:0 5px 30px rgba(0,0,0,.85)}}
.place{{font-family:'Barlow Condensed';font-weight:600;font-size:36px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--gold);margin-top:6px}}
.feats{{font-family:'Barlow Condensed';font-weight:600;font-size:28px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--cream);margin-top:18px}}
.feats i{{color:var(--gold);font-style:normal;margin:0 10px;opacity:.85}}
/* Datos */
.info{{display:flex;justify-content:center;gap:40px;margin-top:48px;flex-wrap:wrap}}
.info .it{{display:flex;gap:12px;text-align:left;max-width:210px}}
.info .ic{{width:28px;height:28px;border:2px solid var(--gold);border-radius:7px;flex:0 0 auto;margin-top:2px}}
.info b{{display:block;font-weight:700;font-size:15px;color:var(--gold)}}
.info span{{font-size:14px;color:var(--cream);line-height:1.35}}
.buy{{margin:44px auto 0;display:inline-block;background:linear-gradient(180deg,#F0B93A,#E9A72C);color:#2A1B06;
  font-family:'Barlow Condensed';font-weight:700;font-size:32px;letter-spacing:.12em;text-transform:uppercase;
  padding:18px 60px;border-radius:999px;box-shadow:0 22px 54px -14px rgba(233,167,44,.85),inset 0 2px 0 rgba(255,255,255,.5)}}
/* Secciones */
.sec{{margin-top:60px;text-align:left}}
.sec-h{{font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:.05em;text-transform:uppercase;
  color:var(--gold);text-align:center;margin-bottom:8px;text-shadow:0 3px 20px rgba(0,0,0,.95),0 1px 4px rgba(0,0,0,.9)}}
.sec-s{{text-align:center;color:var(--cream);font-size:16px;margin-bottom:26px;text-shadow:0 2px 12px rgba(0,0,0,.95)}}
.info b,.info span{{text-shadow:0 2px 12px rgba(0,0,0,.95)}}
/* Entradas */
.cats{{display:flex;flex-direction:column;gap:18px}}
.cat{{background:var(--panel);border:1px solid rgba(233,167,44,.4);border-radius:16px;overflow:hidden;backdrop-filter:blur(3px)}}
.cat-h{{font-family:'Barlow Condensed';font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--cream);background:rgba(233,167,44,.14);padding:14px 24px;border-bottom:1px solid rgba(233,167,44,.35)}}
table{{width:100%;border-collapse:collapse}}
th{{font-family:'Barlow Condensed';font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--soft);text-align:left;padding:12px 24px}}
th:last-child,td.af{{text-align:center}} th:nth-child(2){{text-align:left}}
td{{padding:13px 24px;border-top:1px solid rgba(255,255,255,.07);font-size:17px;color:var(--cream)}}
td.et{{font-weight:600}} td.pr{{font-family:'Barlow Condensed';font-weight:700;font-size:22px;color:var(--gold)}}
td.pr span{{font-family:'Barlow';font-weight:600;font-size:13px;color:var(--soft)}}
td.af{{color:var(--soft);font-size:15px}}
/* Info adicional */
.panel{{background:var(--panel);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:32px 36px;backdrop-filter:blur(3px)}}
.panel p{{font-size:17px;line-height:1.6;color:var(--cream);margin-bottom:14px}}
.panel .lead{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;color:var(--gold)}}
.panel ul{{margin:6px 0 16px;padding-left:4px;list-style:none}}
.panel li{{position:relative;padding-left:28px;font-size:17px;line-height:1.6;color:var(--cream);margin-bottom:6px}}
.panel li:before{{content:'';position:absolute;left:4px;top:11px;width:9px;height:9px;background:var(--gold);
  transform:rotate(45deg);border-radius:2px}}
.data-line{{margin-top:6px;font-family:'Barlow Condensed';font-weight:600;font-size:18px;letter-spacing:.04em;color:var(--cream)}}
.data-line b{{color:var(--gold)}}
/* Responsable + ticketing */
.resp{{margin-top:40px;text-align:center;color:var(--soft);font-family:'Barlow Condensed';font-weight:600;
  font-size:18px;letter-spacing:.06em}}
.resp b{{color:var(--cream)}}
.tk{{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:22px}}
.tk .lbl{{font-family:'Barlow Condensed';font-weight:600;font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:var(--soft)}}
.tk img{{height:36px}} .tk .web{{font-family:'Barlow Condensed';font-weight:700;font-size:26px;color:var(--cream)}}
</style>

<div class="hdr"><img src="{TUBO}" alt="Tuboleta">
  <div class="nav bc">Conciertos · Teatro · Deportes · Ventas a empresas · Más</div>
  <div class="acc bc">Bono Regalo · Pásala · Contáctanos · Mi cuenta</div></div>
<div class="search"><div class="searchbar bc">Buscar por artista, evento…<div class="go"></div></div></div>

<div class="wrap">
  <img class="sello" src="{LATOMA}" alt="La Toma Cervecera">
  <img class="brand" src="{OKT}" alt="Oktoberfest Artesanal">
  <div class="city">Bogotá <b>2026</b></div>
  <div class="rule"></div>
  <div class="when">Sábado 24 de octubre</div>
  <div class="place">Centro de Eventos CESAP · Bogotá</div>
  <div class="feats">+40 Cervecerías<i>·</i>Bandas en vivo<i>·</i>Gastronomía<i>·</i>Talento local</div>

  <div class="info">
    <div class="it"><div class="ic"></div><div><b>LUGAR</b><span>Centro Social de Agentes y Patrulleros (CESAP) · Dg 44 #68B-30</span></div></div>
    <div class="it"><div class="ic"></div><div><b>FECHA</b><span>Sábado 24 de octubre de 2026</span></div></div>
    <div class="it"><div class="ic"></div><div><b>HORARIO</b><span>12:00 m. a 12:00 a. m. (12 horas)</span></div></div>
    <div class="it"><div class="ic"></div><div><b>APERTURA</b><span>12:00 p. m.</span></div></div>
    <div class="it"><div class="ic"></div><div><b>EDAD MÍNIMA</b><span>18 años</span></div></div>
  </div>
  <div class="buy bc">Comprar entradas</div>

  <div class="sec">
    <div class="sec-h">Entradas</div>
    <div class="sec-s">Admisión general · precios por etapa (incluye valor + servicio) y aforo por localidad</div>
    <div class="cats">{entradas_html()}</div>
  </div>

  <div class="sec">
    <div class="sec-h">Información adicional</div>
    <div class="panel">
      <p class="lead">¡Bogotá se prepara para vivir una de las celebraciones cerveceras más esperadas del año!</p>
      <p>Este 24 de octubre, el <b>CESAP – Centro Social de Agentes y Patrulleros</b> se transforma en el punto de encuentro para disfrutar Oktoberfest Artesanal 2026: una experiencia que reúne en un solo lugar cerveza artesanal, gastronomía, música en vivo, entretenimiento y grandes experiencias de marca.</p>
      <p>Durante <b>12 horas</b> podrás disfrutar de:</p>
      <ul>{''.join(f'<li>{s}</li>' for s in SERVICIOS)}</ul>
      <div class="data-line"><b>Fecha:</b> 24 de octubre de 2026 &nbsp;·&nbsp; <b>Lugar:</b> CESAP – Bogotá &nbsp;·&nbsp; <b>Horario:</b> 12:00 m. a 12:00 a. m.</div>
    </div>
  </div>

  <div class="resp">Responsable: <b>Black Elephant Group S.A.S</b> &nbsp;·&nbsp; NIT 901.538.172-7 &nbsp;·&nbsp; PULEP IZP513</div>
  <div class="tk"><span class="lbl">Boletas en</span><img src="{TUBO}" alt="Tuboleta"><span class="web">tuboleta.com</span></div>
</div>
"""


def main():
    html = OUT / "propuesta-pagina-oktoberfest-bogota.html"
    png = OUT / "propuesta-pagina-oktoberfest-bogota.png"
    html.write_text(HTML, encoding="utf-8")
    subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=8000",
                    f"--screenshot={png}", html.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    # recortar el sólido Noche Festival sobrante al pie
    px = im.load()
    end = im.height
    for y in range(im.height - 1, 0, -1):
        if any(abs(px[x, y][0] - NIGHT[0]) + abs(px[x, y][1] - NIGHT[1]) + abs(px[x, y][2] - NIGHT[2]) > 24
               for x in range(0, im.width, 60)):
            end = min(im.height, y + 60)
            break
    im = im.crop((0, 0, im.width, end))
    im.save(png)
    print(f"propuesta {im.size}  ->  {png}")


if __name__ == "__main__":
    main()
