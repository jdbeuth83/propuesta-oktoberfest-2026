# Historias · Oktoberfest Artesanal Bogotá 2026

Piezas verticales 9:16 (1080 × 1920) construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

## Piezas

| Archivo | Uso |
|---|---|
| `historia-savethedate-con-ciudad.png` | Save the date · mantiene «Bogotá 2026» bajo el logotipo |
| `historia-savethedate-sin-ciudad.png` | Save the date · solo las dos marcas y los tres datos |

Ambas dicen lo mismo: **Oktoberfest Artesanal**, **La Toma Cervecera**, **Save the date ·
24 de octubre** y **Boletas próximamente**. Sin locación todavía, sin titulares y sin cuerpo
de texto — la imagen madre hace el resto.

## Cómo se regenera

```bash
python3 prepare-assets.py               # solo si cambia el logotipo original
python3 build-historia-savethedate.py   # genera las dos variantes
```

Cada variante escribe su HTML autocontenido (fuentes e imágenes en base64) y se renderiza a
PNG con el Chromium headless del entorno. Para editar el copy o el encuadre se toca el
script — no el PNG.

## Fidelidad al sistema

- **Imagen madre** — la toma aérea del festival a la hora dorada (`_assets/hero-sunset.jpg`,
  derivada de `hero-okt-sunset-v1.png` del sistema).
- **Paleta del ocaso** — Ocaso Oro `#E9A72C` en la etiqueta y la píldora, Crema Espuma
  `#EEE7D6` en la fecha, Noche Festival `#14110B` de fondo.
- **Tipografía** — Barlow Condensed 700 en mayúscula espaciada para fecha y etiquetas; el
  logotipo blackletter es la firma de marca y nunca se reescribe.
- **Logotipo** — sin recuadro ni plancha: `prepare-assets.py` retira el contorno sticker del
  logo original y lo pinta en Crema Espuma, sin redibujar la letra. Va sobre la zona oscura
  de la imagen, nunca sobre el cielo brillante. La Toma Cervecera lo encabeza como sello
  productor.

## Zonas seguras de Instagram

Márgenes de 186 px arriba y 250 px abajo para que ni el header ni la barra de respuesta
tapen el sello productor, la fecha ni el handle.
