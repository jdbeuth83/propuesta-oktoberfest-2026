# Save the date · Oktoberfest Artesanal Bogotá 2026

Piezas para redes construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

## Piezas

| Archivo | Formato | Uso |
|---|---|---|
| `savethedate-post-4x5.png` | 1080 × 1350 | Post de feed — formato principal |
| `savethedate-post-1x1.png` | 1080 × 1080 | Post de feed cuadrado |
| `savethedate-historia-9x16.png` | 1080 × 1920 | Historia |

Las tres dicen lo mismo: **Oktoberfest Artesanal**, **La Toma Cervecera**, **Bogotá 2026**,
**Save the date · 24 de octubre** y **Boletas próximamente**. Sin locación todavía, sin
titulares y sin cuerpo de texto — la imagen madre hace el resto.

La ciudad es obligatoria en toda pieza: el festival también corre en Medellín y «Bogotá 2026»
es lo que separa una edición de la otra de un vistazo.

## Cómo se regenera

```bash
python3 build-savethedate.py   # los tres formatos de una
```

Cada formato escribe su HTML autocontenido (fuentes e imágenes en base64) y se renderiza a
PNG. Para editar el copy, la escala o el encuadre se toca el script — no el PNG.

Dos detalles del render que conviene no perder:

- Se usa `headless_shell`, no el Chromium completo. En modo headless el Chromium deja un
  viewport ~87 px más bajo que la ventana pedida y recorta el borde inferior del lienzo sin
  avisar. El build verifica el tamaño exacto y falla si aparece franja negra al pie.
- El eje de composición está en `CENTERED`. En `True` queda centrado (lectura de afiche); en
  `False` se alinea al margen izquierdo.

## Fidelidad al sistema

- **Imagen madre** — la toma aérea del festival a la hora dorada (`_assets/hero-sunset.jpg`,
  derivada de `hero-okt-sunset-v1.png` del sistema).
- **Paleta del ocaso** — Ocaso Oro `#E9A72C` en la ciudad, la etiqueta y la píldora; Crema
  Espuma `#EEE7D6` en la fecha; Noche Festival `#14110B` de fondo.
- **Tipografía** — Barlow Condensed 700 en mayúscula espaciada para ciudad, fecha y
  etiquetas. El logotipo blackletter es la firma de marca y nunca se reescribe.
- **Logotipo** — el original tal cual: blackletter azul + café con su contorno blanco, sin
  recuadro ni plancha. El contorno le da todo el contraste que necesita sobre la noche del
  festival; la sombra suave solo lo despega de la foto.
- **Sello productor** — La Toma Cervecera encabeza el masthead, escalado por formato.
- **Encuadre** — la foto es apaisada, así que cada formato corre el recorte a la derecha lo
  suficiente para no cortar el inflable de cerveza por la mitad. En 9:16 el borde superior de
  la foto se funde contra la noche; en feed va a sangre completa —si se fundiera, el atardecer
  se perdería justo en esa zona— y el contraste lo pone el velo, la capa que el sistema exige
  antes de poner tipografía sobre el cielo.

## Zonas seguras de Instagram

La historia lleva márgenes de 186 px arriba y 250 px abajo para que ni el header ni la barra
de respuesta tapen el sello productor, la fecha ni el handle. Los posts de feed no llevan
interfaz encima, así que usan márgenes parejos.
