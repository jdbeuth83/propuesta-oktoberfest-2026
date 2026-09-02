#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Historia teaser (1080×1920) para publicar YA · Oktoberfest Artesanal Bogotá 2026.
Foto de ediciones pasadas (banco de imágenes: multitud + escenario nocturno) y
un único mensaje: PRÓXIMAMENTE NOTICIAS.
"""
import base64, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
WORK_AS = ROOT / "_assets"
FOTO = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/fotos-bogota/FOTOS LA TOMA-152.jpg")  # multitud Bogotá
OUT = ROOT / "renders" / "historia-teaser"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920


def du(p, m):
    return f"data:{m};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"


PHOTO = du(FOTO, "image/jpeg")
OKT = du(WORK_AS / "okt-logo-hires.png", "image/png")


def find_chrome():
    p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(p).exists():
        return p
    raise SystemExit("No Chrome")


HTML = f"""<!doctype html>
<meta charset="utf-8"><title>Historia teaser · Oktoberfest Bogotá 2026</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&display=swap');
:root{{--night:#14110B;--gold:#E9A72C;--cream:#EEE7D6;--soft:#B7AC93}}
*{{margin:0;box-sizing:border-box;font-family:'Barlow Condensed',system-ui,sans-serif}}
html,body{{background:#000}}
.stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--night)}}
.photo{{position:absolute;inset:0}}
.photo img{{width:100%;height:100%;object-fit:cover;object-position:center 50%;
  filter:saturate(1.08) contrast(1.04)}}
/* velo: oscurece arriba (para texto) y un pie suave; deja la escena viva al centro */
.veil{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(8,6,3,.86) 0%,rgba(8,6,3,.55) 22%,rgba(8,6,3,.10) 40%,
    rgba(8,6,3,0) 58%,rgba(8,6,3,.30) 82%,rgba(8,6,3,.70) 100%)}}
.in{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;
  text-align:center;padding:250px 90px 250px}}
.brand{{width:560px;filter:drop-shadow(0 14px 34px rgba(0,0,0,.6))}}
.kicker{{margin-top:64px;font-weight:600;font-size:40px;letter-spacing:.46em;text-transform:uppercase;
  color:var(--gold);text-shadow:0 4px 22px rgba(0,0,0,.9)}}
.big{{margin-top:6px;font-weight:700;font-size:150px;line-height:.92;letter-spacing:.02em;text-transform:uppercase;
  color:var(--cream);text-shadow:0 8px 40px rgba(0,0,0,.95)}}
.rule{{width:120px;height:4px;background:var(--gold);border-radius:2px;margin:40px auto 0;opacity:.9}}
.handle{{margin-top:auto;font-weight:600;font-size:30px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--cream);text-shadow:0 3px 16px rgba(0,0,0,.9)}}
</style>
<div class="stage">
  <div class="photo"><img src="{PHOTO}" alt="Oktoberfest Artesanal — ediciones pasadas"></div>
  <div class="veil"></div>
  <div class="in">
    <img class="brand" src="{OKT}" alt="Oktoberfest Artesanal">
    <div class="kicker">Próximamente</div>
    <div class="big">Noticias</div>
    <div class="rule"></div>
    <div class="handle">@oktoberfestartesanalbog</div>
  </div>
</div>
"""


def main():
    html = OUT / "historia-teaser-proximamente.html"
    png = OUT / "_teaser.png"
    jpg = OUT / "historia-teaser-proximamente-1080x1920.jpg"
    html.write_text(HTML, encoding="utf-8")
    subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=8000",
                    f"--screenshot={png}", html.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    assert im.size == (W, H), im.size
    for q in range(95, 78, -3):
        im.save(jpg, "JPEG", quality=q, optimize=True, progressive=True, dpi=(72, 72))
        if jpg.stat().st_size <= 500 * 1000:
            break
    print(f"{jpg.name}  {im.size[0]}x{im.size[1]}  {jpg.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
