# Historias · Oktoberfest Artesanal Bogotá 2026

Piezas verticales 9:16 (1080 × 1920) construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

## Piezas

| Archivo | Uso |
|---|---|
| `historia-boleteria-bogota-2026.png` | Historia de calentamiento previa al lanzamiento de boletería |

## Cómo se regenera

```bash
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
- **Logotipo** — blackletter sobre plancha crema, con aire alrededor y nunca sobre el cielo
  brillante sin capa de contraste. La Toma Cervecera aparece como sello productor.

## Zonas seguras de Instagram

Márgenes de 190 px arriba y 252 px abajo para que ni el header ni la barra de respuesta
tapen el sello productor, la fecha ni el handle.
