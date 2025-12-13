#!/usr/bin/env python3
"""
Dars - Aplicación de Demostración Completa
Una aplicación que demuestra todas las características principales de Dars
"""

from dars.all import *

# Crear la aplicación con configuración avanzada
app = App(
    title="Dars - Demostración Completa",
    theme="light",
)

index = Page(
    Text(text="This template is deprecated. It needs to be updated. Please wait unitil its updated because its too old.")
)

app.add_page("index", index, index=True)
if __name__ == '__main__':
    app.rTimeCompile()
