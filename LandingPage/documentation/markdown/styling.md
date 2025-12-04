# Styling System in Dars

Dars Framework introduces a powerful, Python-native utility class system inspired by Tailwind CSS. This system allows you to style your components using concise string utilities directly in your Python code, without needing Node.js, PostCSS, or any external build tools.

## Overview

Instead of writing raw CSS dictionaries or separate CSS files, you can now use the `style`, `hover_style`, and `active_style` arguments with utility strings. These strings are parsed at runtime (and export time) into standard CSS dictionaries.

### Example

```python
from dars.all import *

def MyComponent():
    return Container(
        Text("Hello, Dars!"),
        style="bg-blue-500 p-4 rounded-lg shadow-md hover:bg-blue-600 transition-all",
        hover_style="scale-105",
        active_style="scale-95"
    )
```

## Supported Utilities

The system supports a wide range of utilities covering layout, spacing, typography, colors, borders, and effects.

### Layout & Flexbox
- **Display**: `flex`, `grid`, `block`, `inline-block`, `hidden`
- **Flex Direction**: `flex-row`, `flex-col`, `flex-row-reverse`, `flex-col-reverse`
- **Justify Content**: `justify-start`, `justify-center`, `justify-end`, `justify-between`, `justify-around`
- **Align Items**: `items-start`, `items-center`, `items-end`, `items-stretch`
- **Gap**: `gap-4`, `gap-x-2`, `gap-y-4`

### Spacing (Padding & Margin)
- **Padding**: `p-4` (all sides), `px-4` (horizontal), `py-4` (vertical), `pt-4` (top), `pr-4` (right), `pb-4` (bottom), `pl-4` (left)
- **Margin**: `m-4`, `mx-4`, `my-4`, `mt-4`, `mr-4`, `mb-4`, `ml-4`
- **Values**: 
  - Numbers correspond to `0.25rem` units (e.g., `4` = `1rem`, `8` = `2rem`).
  - Arbitrary values: `p-[20px]`, `m-[5%]`.

### Sizing
- **Width**: `w-full`, `w-screen`, `w-1/2`, `w-10`, `w-[300px]`
- **Height**: `h-full`, `h-screen`, `h-10`, `h-[50vh]`
- **Max/Min**: `max-w-md`, `min-h-screen`

### Typography
- **Font Size**: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-[14px]`
- **Font Weight**: `font-thin`, `font-normal`, `font-bold`, `font-black`
- **Text Align**: `text-left`, `text-center`, `text-right`, `text-justify`
- **Text Color**: `text-blue-500`, `text-white`, `text-[#123456]`

### Backgrounds
- **Color**: `bg-red-500`, `bg-gray-100`, `bg-[#f0f0f0]`
- **Opacity**: `bg-opacity-50` (requires separate utility or arbitrary value)

### Borders & Radius
- **Border Width**: `border`, `border-2`, `border-4`
- **Border Color**: `border-gray-300`, `border-red-500`
- **Border Radius**: `rounded`, `rounded-md`, `rounded-lg`, `rounded-full`, `rounded-[10px]`

### Effects
- **Shadow**: `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-none`
- **Opacity**: `opacity-0`, `opacity-50`, `opacity-100`
- **Cursor**: `cursor-pointer`, `cursor-not-allowed`

## Arbitrary Values

For values not covered by the standard scale, use square brackets `[]`:

```python

Container(
    style="w-[350px] bg-[#1a2b3c] z-[100] top-[50px]"
)

```

## State Variants

You can define styles for specific states using `hover_style` and `active_style` arguments.

```python

Button(
    "Click Me",
    style="bg-blue-500 text-white px-4 py-2 rounded",
    hover_style="bg-blue-600 shadow-lg",
    active_style="bg-blue-700 transform scale-95"
)

```

## Performance

The parsing happens in Python before the HTML/CSS is generated. This means
1.  **Zero Runtime Overhead**: The browser receives standard CSS.
2.  **No JavaScript Dependency**: No need to load a large utility CSS library or run JS parsers in the browser.
3.  **Optimized Output**: Only the styles you use are generated (as inline styles or extracted CSS).
