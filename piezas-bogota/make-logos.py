#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deriva del logo Oktoberfest Artesanal en alta resolución (1871×756, del design
system) dos versiones nítidas para las piezas de Tuboleta:

  · okt-logo-hires.png  — con contorno blanco para fondos oscuros (foto).
  · logo-oktoberfest-artesanal-byn-500x250.png — blanco y negro para el ticket.
"""
import pathlib
from PIL import Image, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/logos/oktoberfest.png")
# La Toma en máxima calidad: la maestra del design system (misma de Claude Design).
LATOMA_SRC = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/brand/logos/la-toma-horizontal-blanco.png")
OUT = ROOT / "_assets"
OUT.mkdir(parents=True, exist_ok=True)

PAD = 60          # margen transparente para que el contorno no se recorte
GROW = 34         # grosor del contorno blanco (px sobre el original de 1871)


def outlined() -> pathlib.Path:
    """Contorno blanco liso y de ancho uniforme (estilo sticker oficial).

    Método difuminar→umbralizar en 3× para un halo redondeado y parejo, sin los
    abultamientos que deja el MaxFilter. El ancho lo fija GROW (px sobre 1871).
    """
    SC = 3
    logo = Image.open(SRC).convert("RGBA")
    logo = ImageOps.expand(logo, border=PAD, fill=(0, 0, 0, 0))
    alpha = logo.split()[3]

    big = alpha.resize((alpha.width * SC, alpha.height * SC), Image.LANCZOS)
    # Difuminar y umbralizar bajo expande la silueta de forma uniforme; el radio
    # controla cuánto crece y el blur final suaviza el borde (antialias).
    grown = big.filter(ImageFilter.GaussianBlur(GROW * SC * 0.62))
    grown = grown.point(lambda p: 255 if p >= 46 else 0)
    grown = grown.filter(ImageFilter.GaussianBlur(SC * 1.1))
    grown = grown.resize(alpha.size, Image.LANCZOS)

    white = Image.new("RGBA", logo.size, (255, 255, 255, 255))
    halo = Image.composite(white, Image.new("RGBA", logo.size, (255, 255, 255, 0)), grown)

    out_img = Image.alpha_composite(halo, logo)
    out_img = out_img.crop(out_img.getbbox())
    p = OUT / "okt-logo-hires.png"
    out_img.save(p, "PNG", optimize=True)
    print(f"contorneado {out_img.size}  {p.stat().st_size/1024:.0f} KB")
    return p


def byn() -> pathlib.Path:
    logo = Image.open(SRC).convert("RGBA")
    _, _, _, a = logo.split()
    gray = ImageOps.grayscale(logo.convert("RGB"))
    bw = Image.merge("RGBA", (gray, gray, gray, a))
    bw = bw.crop(bw.getbbox())
    bw.thumbnail((500, 250), Image.LANCZOS)
    p = OUT / "logo-oktoberfest-artesanal-byn-500x250.png"
    bw.save(p, "PNG", optimize=True)
    print(f"byn {bw.size}  {p.stat().st_size/1024:.0f} KB")
    return p


def latoma_hires() -> pathlib.Path:
    """La Toma Cervecera en alta resolución, recortada ajustada, sobre transparente."""
    with Image.open(LATOMA_SRC).convert("RGBA") as lg:
        lg = lg.crop(lg.getbbox())
        p = OUT / "latoma-blanco-hires.png"
        lg.save(p, "PNG", optimize=True)
    print(f"latoma hi-res {lg.size}  {p.stat().st_size/1024:.0f} KB")
    return p


if __name__ == "__main__":
    outlined()
    byn()
    latoma_hires()
