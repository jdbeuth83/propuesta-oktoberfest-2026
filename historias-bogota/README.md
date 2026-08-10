# Historias · Oktoberfest Artesanal Bogotá 2026

Piezas verticales 9:16 (1080 × 1920) construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

## Piezas

| Archivo | Uso |
|---|---|
| `historia-savethedate-centrado.png` | Save the date · eje simétrico, lectura de afiche |
| `historia-savethedate-izquierda.png` | Save the date · eje editorial alineado al margen |

Dice cinco cosas: **Oktoberfest Artesanal**, **La Toma Cervecera**, **Bogotá 2026**,
**Save the date · 24 de octubre** y **Boletas próximamente**. Sin locación todavía, sin
titulares y sin cuerpo de texto — la imagen madre hace el resto.

La ciudad es obligatoria en toda pieza: el festival también corre en Medellín y «Bogotá 2026»
es lo que separa una edición de la otra de un vistazo.

## Cómo se regenera

```bash
python3 build-historia-savethedate.py   # genera los dos ejes
```

Cada eje escribe su HTML autocontenido (fuentes e imágenes en base64) y se renderiza a PNG
con el Chromium headless del entorno. Para editar el copy o el encuadre se
toca el script — no el PNG.

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
- **Sello productor** — La Toma Cervecera encabeza el masthead a 74 px de alto, al doble del
  tamaño con el que arrancó la pieza.

## Zonas seguras de Instagram

Márgenes de 186 px arriba y 250 px abajo para que ni el header ni la barra de respuesta
tapen el sello productor, la fecha ni el handle.
