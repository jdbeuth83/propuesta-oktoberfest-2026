# Piezas para Tuboleta · Oktoberfest Artesanal Bogotá 2026

Formatos que exige el «Manual de piezas para publicar eventos en Tuboleta»,
construidos sobre el mismo Sistema de Diseño Bogotá que el save the date
(imagen madre a la hora dorada, paleta del ocaso, Barlow Condensed y el
logotipo blackletter original).

Todas en **JPG <500 KB a 72 dpi** (galería <1 MB), salvo el logo en **PNG**.

| Pieza | Archivo | Medida |
|---|---|---|
| Banner desplegable · desktop | `banner-desplegable/desktop-1920x150.jpg` | 1920×150 |
| Banner desplegable · mobile | `banner-desplegable/mobile-1920x710.jpg` | 1920×710 |
| Imagen del evento (caja segura 700×720) | `imagen-evento/imagen-evento-900x800.jpg` | 900×800 |
| Boleta digital (arte del PDF) | `boleta-digital/boleta-digital-900x1050.jpg` | 900×1050 |
| Recurso banner | `recurso-banner/recurso-banner-1000x400.jpg` | 1000×400 |
| Recurso plano (datos del evento) | `recurso-plano/recurso-plano-1080x1080.jpg` | 1080×1080 |
| Redes · post | `redes/post-1080x1080.jpg` | 1080×1080 |
| Redes · story | `redes/story-1080x1920.jpg` | 1080×1920 |
| Galería (branded + 2 fotos) | `galeria/galeria-1..3-1000x1000.jpg` | 1000×1000 |
| Logo blanco y negro | `logo/logo-oktoberfest-artesanal-byn-500x250.png` | ≤500×250 |

## Pendientes del manual

- **Código PULEP.** Va en todas las piezas de promoción cuando el evento se
  registre. Aún no hay registro (las boletas no salen a la venta), así que no
  aparece. En cuanto exista, poner el código en `PULEP` de `build-tuboleta.py`
  y regenerar: reaparece en cada pieza automáticamente.
- **Recurso plano.** Hoy es una tarjeta de datos del evento; cuando haya recinto
  y mapa de localidades definidos, se reemplaza por el plano oficial.

## Cómo se regenera

```bash
python3 build-tuboleta.py   # las 12 piezas de una
```

Cada formato escribe su HTML autocontenido en `.build/` (fuentes e imágenes en
base64) y se renderiza a PNG con Chrome headless, luego se exporta a JPG bajo el
tope de peso. Para editar copy, escala o encuadre se toca el script, no el JPG.
El script detecta `headless_shell` (CI Linux) o Google Chrome (macOS).

## Regla de marcas

El manual solo prohíbe logos de **terceros**. Oktoberfest Artesanal y La Toma
Cervecera (su productora) son marcas propias del evento y sí van en las piezas.
