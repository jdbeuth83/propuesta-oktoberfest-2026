#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deriva la versión monocroma del logotipo para fondos oscuros.

El logo original (`_assets/okt-logo.png`, tomado del Sistema de Diseño Bogotá) es
azul + café con un contorno blanco tipo sticker: sobre la noche del festival el
café desaparece y el contorno obliga a una plancha. Aquí se retira el contorno y
se pinta la letra en Crema Espuma, sin redibujar el blackletter — la regla del
sistema es que el logotipo nunca se reescribe.
"""
import pathlib

from PIL import Image

AS = pathlib.Path(__file__).resolve().parent / "_assets"
CREAM = (238, 231, 214)  # Crema Espuma #EEE7D6


def knockout(src: pathlib.Path, dst: pathlib.Path) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    out = Image.new("RGBA", (w, h))
    sp, op = im.load(), out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if a == 0:
                continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            # contorno sticker: claro y neutro -> fuera
            if lum > 186 and max(r, g, b) - min(r, g, b) < 40:
                continue
            # el resto va a crema, atenuando el antialias contra el contorno
            alpha = min(255, int(a * (1 - max(0, lum - 120) / 150)))
            op[x, y] = CREAM + (alpha,)
    out.save(dst, optimize=True)
    print(f"{dst.name}  {dst.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    knockout(AS / "okt-logo.png", AS / "okt-logo-crema.png")
