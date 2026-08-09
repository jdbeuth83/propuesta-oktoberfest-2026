# Historias · Oktoberfest Artesanal Bogotá 2026

Piezas verticales 9:16 (1080 × 1920) construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

## Piezas

| Archivo | Uso |
|---|---|
| `historia-boleteria-bogota-2026.png` | Historia previa al lanzamiento de boletería |

La pieza dice cuatro cosas y nada más: **logotipo**, **Bogotá 2026**, **fecha y lugar**,
**boletas próximamente**. Sin titulares ni cuerpo de texto — la imagen madre hace el resto.

## Cómo se regenera

```bash
python3 prepare-assets.py            # solo si cambia el logotipo original
python3 build-historia-boleteria.py
```

Escribe `historia-boleteria.html` (autocontenido, fuentes e imágenes en base64) y lo
renderiza a PNG con el Chromium headless del entorno. Para editar el copy o el encuadre,
se toca el script — no el PNG.

## Fidelidad al sistema

- **Imagen madre** — la toma aérea del festival a la hora dorada (`_assets/hero-sunset.jpg`,
  derivada de `hero-okt-sunset-v1.png` del sistema).
- **Paleta del ocaso** — Ocaso Oro `#E9A72C` en titulares y CTA, Ocaso Fuego `#E2611A` en la
  fecha, Crema Espuma `#EEE7D6` en texto, Noche Festival `#14110B` de fondo.
- **Tipografía** — Playfair Display 900 (display, itálica de acento), Barlow (cuerpo),
  Barlow Condensed en mayúscula espaciada (etiquetas).
- **Iconografía** — lúpulo, cerveza, música y atardecer, trazo simple en oro.
- **Logotipo** — blackletter en el masthead, sin recuadro ni plancha: `prepare-assets.py`
  retira el contorno sticker del logo original y lo pinta en Crema Espuma, sin redibujar la
  letra. Va sobre la zona oscura de la imagen, nunca sobre el cielo brillante. La Toma
  Cervecera lo encabeza como sello productor.
- **Ciudad** — «Bogotá 2026» en Barlow Condensed 700 a 112 px como segundo nivel de lectura,
  justo debajo del logotipo.

## Zonas seguras de Instagram

Márgenes de 190 px arriba y 252 px abajo para que ni el header ni la barra de respuesta
tapen el sello productor, la fecha ni el handle.
