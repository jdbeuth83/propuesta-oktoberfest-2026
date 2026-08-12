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

SRC = pathlib.Path("/Users/juandiegobeuthbernal/design-system/assets/events/oktoberfest-2026/logos/oktoberfest.png")
OUT = pathlib.Path(__file__).resolve().parent / "_assets"
OUT.mkdir(parents=True, exist_ok=True)

PAD = 60          # margen transparente para que el contorno no se recorte
GROW = 34         # grosor del contorno blanco (px sobre el original de 1871)


def outlined() -> pathlib.Path:
    logo = Image.open(SRC).convert("RGBA")
    logo = ImageOps.expand(logo, border=PAD, fill=(0, 0, 0, 0))
    alpha = logo.split()[3]

    # Dilatar el alfa para crear el halo: MaxFilter crece el borde por pasadas.
    grown = alpha
    steps = max(1, GROW // 4)
    for _ in range(steps):
        grown = grown.filter(ImageFilter.MaxFilter(9))
    grown = grown.filter(ImageFilter.GaussianBlur(1.2)).point(lambda p: 255 if p > 90 else 0)

    halo = Image.new("RGBA", logo.size, (255, 255, 255, 0))
    halo.putalpha(grown)
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


if __name__ == "__main__":
    outlined()
    byn()
