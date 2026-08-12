# Save the date · Oktoberfest Artesanal Bogotá 2026

Piezas gráficas construidas sobre el **Sistema de Diseño Bogotá**
(`jdbeuth83/oktoberfest-bogota` → `design-system-bogota.html`).

Todas dicen lo mismo: **Oktoberfest Artesanal**, **La Toma Cervecera**, **Bogotá 2026**,
**Save the date · 24 de octubre** y **Boletas próximamente**. Sin locación todavía, sin
titulares y sin cuerpo de texto — la imagen madre hace el resto.

La ciudad es obligatoria en toda pieza: el festival también corre en Medellín y «Bogotá 2026»
es lo que separa una edición de la otra de un vistazo.

## Piezas

### `renders/social/`

| Archivo | Formato | Uso |
|---|---|---|
| `savethedate-post-4x5.png` | 1080 × 1350 | Post de feed — formato principal |
| `savethedate-post-1x1.png` | 1080 × 1080 | Post de feed cuadrado |
| `savethedate-historia-9x16.png` | 1080 × 1920 | Historia |

### `renders/tiquetera/`

| Archivo | Formato | Uso |
|---|---|---|
| `savethedate-banner-1920x600.png` | 1920 × 600 | Banner de la ficha del evento |
| `savethedate-cuadrado-1200x1200.png` | 1200 × 1200 | Imagen principal / miniatura grande |
| `savethedate-card-800x600.png` | 800 × 600 | Tarjeta de listado (4:3) |

### `renders/web/`

| Archivo | Formato | Uso |
|---|---|---|
| `savethedate-hero-2560x1080.png` | 2560 × 1080 | Hero de escritorio |
| `savethedate-hero-mobile-1080x1440.png` | 1080 × 1440 | Hero de móvil (3:4) |
| `savethedate-og-1200x630.png` | 1200 × 630 | Open Graph — WhatsApp, Facebook, X |

Las medidas de tiquetera son las estándar del sector. Si la plataforma pide otras (Passline,
TuBoleta, Eventbrite y compañía difieren entre sí), se agregan al listado `FORMATS` del script
y salen en el mismo build.

## Cómo se regenera

```bash
python3 build-savethedate.py   # los nueve formatos de una
```

Cada formato escribe su HTML autocontenido en `.build/` (fuentes e imágenes en base64) y se
renderiza a PNG en `renders/`. Para editar el copy, la escala o el encuadre se toca el
script — no el PNG. El HTML es artefacto de build y no se versiona.

Dos detalles del render que conviene no perder:

- Se usa `headless_shell`, no el Chromium completo. En modo headless el Chromium deja un
  viewport ~87 px más bajo que la ventana pedida y recorta el borde inferior del lienzo sin
  avisar. El build verifica el tamaño exacto y falla si aparece franja negra al pie.
- Cada formato declara su propio encuadre (`objpos`) y su propia escala tipográfica. La foto
  es apaisada, así que en lienzos verticales el recorte se corre a la derecha lo necesario
  para no cortar el inflable de cerveza por la mitad, y en los anchos se ajusta el eje
  vertical para conservar el sol y la carpa de lúpulo.

## Ejes de composición

- **`stack`** — vertical y cuadrado. Marca arriba, datos abajo, todo centrado sobre el eje.
- **`banner`** — apaisado. Marca a la izquierda, datos a la derecha y la foto respirando en
  el centro; el velo oscurece los dos bordes y deja el centro a plena luz.

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
- **Velo** — es la capa de contraste que el sistema exige antes de poner tipografía sobre el
  cielo del atardecer. Solo la historia 9:16 funde además el borde superior de la foto contra
  la noche: donde no sobra alto, ese fundido se comería el atardecer.

## Zonas seguras de Instagram

La historia lleva márgenes de 186 px arriba y 250 px abajo para que ni el header ni la barra
de respuesta tapen el sello productor, la fecha ni el handle. El resto de formatos no lleva
interfaz encima y usa márgenes parejos.
