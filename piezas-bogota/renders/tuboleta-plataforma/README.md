# Piezas para Tuboleta · Oktoberfest Artesanal Bogotá 2026

Recursos que exige el «Manual de piezas para publicar eventos en Tuboleta».
Son de la **ficha de venta**: **informativas, sin llamado a la acción**.
Comunican evento, ciudad, fecha, lugar y los pilares del festival, con el
código **PULEP** en todas las piezas.

Construidas sobre el Sistema de Diseño Bogotá (imagen madre a la hora dorada,
paleta del ocaso, Barlow Condensed) con el **logotipo Oktoberfest en alta
resolución** (contorno blanco para fondos oscuros, derivado del logo del design
system por `make-logos.py`).

Todas en **JPG <500 KB a 72 dpi** (galería <1 MB); el logo del ticket en **PNG**.

## Copy (fijo)
- **Evento:** Oktoberfest Artesanal · Bogotá 2026
- **Fecha:** Sábado 24 de octubre
- **Lugar:** Centro de Eventos CESAP
- **Pilares:** +40 Cervecerías · Bandas en vivo · Gastronomía · Talento local
- **Legal:** @oktoberfestartesanalbog · PULEP IZP513

## Piezas
| Pieza | Archivo | Medida |
|---|---|---|
| Banner desplegable · desktop | `banner-desplegable/desktop-1920x150.jpg` | 1920×150 |
| Banner desplegable · mobile | `banner-desplegable/mobile-1920x710.jpg` | 1920×710 |
| Imagen del evento | `imagen-evento/imagen-evento-900x800.jpg` | 900×800 |
| Boleta digital (arte del PDF) | `boleta-digital/boleta-digital-900x1050.jpg` | 900×1050 |
| Recurso banner | `recurso-banner/recurso-banner-1000x400.jpg` | 1000×400 |
| Recurso plano (datos del evento) | `recurso-plano/recurso-plano-1080x1080.jpg` | 1080×1080 |
| Redes · post | `redes/post-1080x1080.jpg` | 1080×1080 |
| Redes · story | `redes/story-1080x1920.jpg` | 1080×1920 |
| Galería (branded + 2 fotos) | `galeria/galeria-1..3-1000x1000.jpg` | 1000×1000 |
| Logo blanco y negro | `logo/logo-oktoberfest-artesanal-byn-500x250.png` | ≤500×250 |

## Pendiente
- **Recurso plano:** hoy es tarjeta de datos; se reemplaza por el plano oficial
  de localidades cuando el recinto lo defina.

## Cómo se regenera
```bash
python3 make-logos.py       # deriva el logo hi-res + B&N desde el design system
python3 build-tuboleta.py   # las 12 piezas de una
```
Para cambiar copy (fecha, lugar, pilares, PULEP) se editan las constantes al
inicio de `build-tuboleta.py` y se regenera. El script detecta `headless_shell`
(CI Linux) o Google Chrome (macOS).

## Regla de marcas
El manual solo prohíbe logos de **terceros**. Oktoberfest Artesanal y La Toma
Cervecera (su productora) son marcas propias del evento y sí van en las piezas.
