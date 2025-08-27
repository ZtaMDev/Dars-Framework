from dars.core.app import App
from dars.components.basic import Container, Text, Button
import os
from dars.all import *

# Usar los iconos generados por defecto del framework
ICON_192 = "icon-192x192.png"
ICON_512 = "icon-512x512.png"

app = App(
    title="Dars PWA Custom Icons Template",
    description="Template PWA Dars con iconos personalizados",
    pwa_enabled=True,
    pwa_name="Dars PWA Custom",
    pwa_short_name="DarsPWA",
    theme_color="#1976d2",
    background_color="#fafafa",
    pwa_display="standalone",
    pwa_orientation="portrait",
    service_worker_enabled=True,
    icons=[
        {"src": ICON_192, "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": ICON_512, "sizes": "512x512", "type": "image/png"}
    ]
)

app.root = Container(
    Text(text="¡Bienvenido a la PWA con iconos personalizados!"),
    Button(text="Haz clic aquí", on_click=dScript("alert('¡Botón de ejemplo!')")),
)

if __name__ == '__main__':
    app.rTimeCompile(add_file_types=".js")
