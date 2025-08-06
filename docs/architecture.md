# Arquitectura de Dars

Dars está diseñado con una arquitectura modular y extensible que facilita la creación de aplicaciones UI modernas en Python.

## Estructura del Proyecto

```
dars/
  core/           # Núcleo del framework (App, Component, etc.)
  components/     # Componentes básicos y avanzados
  exporters/      # Exportadores (web, base, etc.)
  scripts/        # Sistema de scripts JS
  cli/            # Herramientas de línea de comandos
  docs/           # Documentación
```

## Núcleo
- **App**: Punto de entrada y gestor de páginas/componentes.
- **Component**: Clase base para todos los componentes UI.

## Componentes
- **Básicos**: Text, Button, Input, Container, etc.
- **Avanzados**: Card, Modal, Navbar, Table, Tabs, Accordion, etc.
- **Layouts**: GridLayout, FlexLayout, AnchorPoint, LayoutBase.

## Exportadores
- **HTML/CSS/JS**: Exporta apps a web estático, multipágina, PWA.
- **Extensible**: Puedes crear nuevos exportadores personalizados.

## CLI
- Inicialización de proyectos (`dars init`)
- Exportación (`dars export`)
- Preview (`dars preview`)

## Barrel Import
Puedes importar todos los componentes principales con:
```python
from dars.all import *
```

## Ejemplo de flujo
1. Crea tu app con App y componentes.
2. Usa layouts y scripts según necesidad.
3. Exporta a HTML/CSS/JS con el CLI.
4. Despliega en cualquier hosting estático o como PWA.
