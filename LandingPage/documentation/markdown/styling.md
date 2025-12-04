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
        style="bg-blue-500 p-4 rounded-lg shadow-md",
        hover_style="bg-blue-600 scale-105",
        active_style="scale-95"
    )
```

## Supported Utilities

The system supports a comprehensive range of utilities covering layout, spacing, typography, colors, borders, effects, transforms, and more.

### Layout & Display

- **Display**: `flex`, `inline-flex`, `grid`, `inline-grid`, `block`, `inline-block`, `inline`, `table`, `table-row`, `table-cell`, `hidden`, `contents`, `flow-root`
- **Flex Direction**: `flex-row`, `flex-row-reverse`, `flex-col`, `flex-col-reverse`
- **Flex Wrap**: `flex-wrap`, `flex-wrap-reverse`, `flex-nowrap`
- **Justify Content**: `justify-start`, `justify-end`, `justify-center`, `justify-between`, `justify-around`, `justify-evenly`
- **Justify Items**: `justify-items-start`, `justify-items-end`, `justify-items-center`, `justify-items-stretch`
- **Align Items**: `items-start`, `items-end`, `items-center`, `items-baseline`, `items-stretch`
- **Align Content**: `content-start`, `content-end`, `content-center`, `content-between`, `content-around`, `content-evenly`
- **Align Self**: `self-auto`, `self-start`, `self-end`, `self-center`, `self-stretch`, `self-baseline`
- **Flex Grow/Shrink**: `grow`, `grow-0`, `shrink`, `shrink-0`
- **Flex**: `flex-1`, `flex-auto`, `flex-initial`, `flex-none`
- **Order**: `order-{n}`
- **Basis**: `basis-{value}`

### Grid

- **Grid Template Columns**: `grid-cols-{n}` (e.g., `grid-cols-3`, `grid-cols-12`)
- **Grid Template Rows**: `grid-rows-{n}`
- **Grid Column Span**: `col-span-{n}`, `col-start-{n}`, `col-end-{n}`
- **Grid Row Span**: `row-span-{n}`, `row-start-{n}`, `row-end-{n}`
- **Grid Auto Flow**: `grid-flow-row`, `grid-flow-col`, `grid-flow-dense`, `grid-flow-row-dense`, `grid-flow-col-dense`
- **Grid Auto Columns**: `auto-cols-auto`, `auto-cols-min`, `auto-cols-max`, `auto-cols-fr`
- **Grid Auto Rows**: `auto-rows-auto`, `auto-rows-min`, `auto-rows-max`, `auto-rows-fr`
- **Gap**: `gap-{n}`, `gap-x-{n}`, `gap-y-{n}`

### Spacing (Padding & Margin)

- **Padding**: `p-{n}` (all sides), `px-{n}` (horizontal), `py-{n}` (vertical), `pt-{n}` (top), `pr-{n}` (right), `pb-{n}` (bottom), `pl-{n}` (left), `ps-{n}` (inline-start), `pe-{n}` (inline-end)
- **Margin**: `m-{n}`, `mx-{n}`, `my-{n}`, `mt-{n}`, `mr-{n}`, `mb-{n}`, `ml-{n}`, `ms-{n}`, `me-{n}`
- **Margin Auto**: `mx-auto`, `my-auto`
- **Values**: 
  - Numbers correspond to `0.25rem` units (e.g., `4` = `1rem`, `8` = `2rem`)
  - Arbitrary values: `p-[20px]`, `m-[5%]`

### Sizing

- **Width**: `w-{n}`, `w-full`, `w-screen`, `w-auto`, `w-min`, `w-max`, `w-fit`, `w-1/2`, `w-1/3`, `w-[300px]`
- **Height**: `h-{n}`, `h-full`, `h-screen`, `h-auto`, `h-min`, `h-max`, `h-fit`, `h-[50vh]`
- **Min Width**: `min-w-{n}`, `min-w-full`, `min-w-min`, `min-w-max`, `min-w-fit`
- **Min Height**: `min-h-{n}`, `min-h-full`, `min-h-screen`, `min-h-min`, `min-h-max`, `min-h-fit`
- **Max Width**: `max-w-{size}` (xs, sm, md, lg, xl, 2xl-7xl, full, min, max, fit, prose, screen-{size})
- **Max Height**: `max-h-{n}`, `max-h-full`, `max-h-screen`, `max-h-min`, `max-h-max`, `max-h-fit`, `max-h-none`
- **Size**: `size-{n}` (sets both width and height)

### Typography

- **Font Size**: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`, `text-5xl`, `text-6xl`, `text-7xl`, `text-8xl`, `text-9xl`
- **Font Size (Direct)**: `fs-[32px]`, `fs-[2rem]` Direct font-size specification
- **Font Weight**: `font-thin`, `font-extralight`, `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`, `font-extrabold`, `font-black`
- **Font Style**: `italic`, `not-italic`
- **Text Align**: `text-left`, `text-center`, `text-right`, `text-justify`, `text-start`, `text-end`
- **Text Color**: `text-{color}-{shade}`, `text-[#123456]`
- **Text Decoration**: `underline`, `overline`, `line-through`, `no-underline`
- **Text Transform**: `uppercase`, `lowercase`, `capitalize`, `normal-case`
- **Text Overflow**: `truncate`, `text-ellipsis`, `text-clip`
- **Vertical Align**: `align-baseline`, `align-top`, `align-middle`, `align-bottom`, `align-text-top`, `align-text-bottom`, `align-sub`, `align-super`
- **Whitespace**: `whitespace-normal`, `whitespace-nowrap`, `whitespace-pre`, `whitespace-pre-line`, `whitespace-pre-wrap`, `whitespace-break-spaces`
- **Word Break**: `break-normal`, `break-words`, `break-all`, `break-keep`
- **Line Height**: `leading-none`, `leading-tight`, `leading-snug`, `leading-normal`, `leading-relaxed`, `leading-loose`, `leading-{n}`
- **Letter Spacing**: `tracking-tighter`, `tracking-tight`, `tracking-normal`, `tracking-wide`, `tracking-wider`, `tracking-widest`
- **Text Indent**: `indent-{n}`

### Colors

**Complete Palette** (50-950 shades for each):

- **Neutrals**: `slate`, `gray`, `zinc`, `neutral`, `stone`
- **Reds**: `red`, `rose`
- **Oranges**: `orange`, `amber`
- **Yellows**: `yellow`, `lime`
- **Greens**: `green`, `emerald`, `teal`
- **Blues**: `cyan`, `sky`, `blue`, `indigo`
- **Purples**: `violet`, `purple`, `fuchsia`
- **Pinks**: `pink`
- **Special**: `black`, `white`, `transparent`, `current`

**Usage Examples:**
```python
style="bg-cyan-500 text-white"        # Cyan background
style="bg-emerald-600 text-slate-50"  # Emerald background with light slate text
style="bg-fuchsia-500 text-rose-100"  # Fuchsia background with light rose text
style="bg-amber-400 text-zinc-900"    # Amber background with dark zinc text
```

### Backgrounds

- **Background Color**: `bg-{color}-{shade}`, `bg-[#f0f0f0]`
- **Background Position**: `bg-bottom`, `bg-center`, `bg-left`, `bg-left-bottom`, `bg-left-top`, `bg-right`, `bg-right-bottom`, `bg-right-top`, `bg-top`
- **Background Repeat**: `bg-repeat`, `bg-no-repeat`, `bg-repeat-x`, `bg-repeat-y`, `bg-repeat-round`, `bg-repeat-space`
- **Background Size**: `bg-auto`, `bg-cover`, `bg-contain`
- **Background Attachment**: `bg-fixed`, `bg-local`, `bg-scroll`
- **Background Clip**: `bg-clip-border`, `bg-clip-padding`, `bg-clip-content`, `bg-clip-text`
- **Background Origin**: `bg-origin-border`, `bg-origin-padding`, `bg-origin-content`
- **Background Blend Mode**: `bg-blend-normal`, `bg-blend-multiply`, `bg-blend-screen`, `bg-blend-overlay`, `bg-blend-darken`, `bg-blend-lighten`, `bg-blend-color-dodge`, `bg-blend-color-burn`, `bg-blend-hard-light`, `bg-blend-soft-light`, `bg-blend-difference`, `bg-blend-exclusion`, `bg-blend-hue`, `bg-blend-saturation`, `bg-blend-color`, `bg-blend-luminosity`

### Borders & Radius

- **Border Width**: `border`, `border-0`, `border-2`, `border-4`, `border-8`
- **Border Width (Sides)**: `border-t-{n}`, `border-r-{n}`, `border-b-{n}`, `border-l-{n}`, `border-x-{n}`, `border-y-{n}`
- **Border Color**: `border-{color}-{shade}`, `border-[#123456]`
- **Border Color (Sides)**: `border-t-{color}`, `border-r-{color}`, `border-b-{color}`, `border-l-{color}`, `border-x-{color}`, `border-y-{color}`
- **Border Style**: `border-solid`, `border-dashed`, `border-dotted`, `border-double`, `border-hidden`, `border-none`
- **Border Radius**: `rounded`, `rounded-none`, `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-2xl`, `rounded-3xl`, `rounded-full`, `rounded-[10px]`
- **Border Radius (Corners)**: `rounded-t-{size}`, `rounded-r-{size}`, `rounded-b-{size}`, `rounded-l-{size}`, `rounded-tl-{size}`, `rounded-tr-{size}`, `rounded-br-{size}`, `rounded-bl-{size}`

### Effects

- **Box Shadow**: `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`, `shadow-inner`, `shadow-none`
- **Opacity**: `opacity-0`, `opacity-25`, `opacity-50`, `opacity-75`, `opacity-100`
- **Mix Blend Mode**: `mix-blend-normal`, `mix-blend-multiply`, `mix-blend-screen`, `mix-blend-overlay`, `mix-blend-darken`, `mix-blend-lighten`, `mix-blend-color-dodge`, `mix-blend-color-burn`, `mix-blend-hard-light`, `mix-blend-soft-light`, `mix-blend-difference`, `mix-blend-exclusion`, `mix-blend-hue`, `mix-blend-saturation`, `mix-blend-color`, `mix-blend-luminosity`

### Filters

- **Blur**: `blur-none`, `blur-sm`, `blur`, `blur-md`, `blur-lg`, `blur-xl`, `blur-2xl`, `blur-3xl`
- **Brightness**: `brightness-{n}` (0-200)
- **Contrast**: `contrast-{n}` (0-200)
- **Grayscale**: `grayscale-{n}` (0-100)
- **Hue Rotate**: `hue-rotate-{n}` (degrees)
- **Invert**: `invert-{n}` (0-100)
- **Saturate**: `saturate-{n}` (0-200)
- **Sepia**: `sepia-{n}` (0-100)
- **Drop Shadow**: `drop-shadow-sm`, `drop-shadow`, `drop-shadow-md`, `drop-shadow-lg`, `drop-shadow-xl`, `drop-shadow-2xl`, `drop-shadow-none`

### Backdrop Filters

- **Backdrop Blur**: `backdrop-blur-{size}`
- **Backdrop Brightness**: `backdrop-brightness-{n}`
- **Backdrop Contrast**: `backdrop-contrast-{n}`
- **Backdrop Grayscale**: `backdrop-grayscale-{n}`
- **Backdrop Hue Rotate**: `backdrop-hue-rotate-{n}`
- **Backdrop Invert**: `backdrop-invert-{n}`
- **Backdrop Opacity**: `backdrop-opacity-{n}`
- **Backdrop Saturate**: `backdrop-saturate-{n}`
- **Backdrop Sepia**: `backdrop-sepia-{n}`

### Transforms

- **Scale**: `scale-{n}`, `scale-x-{n}`, `scale-y-{n}` (e.g., `scale-110` = 110%)
- **Rotate**: `rotate-{n}` (degrees)
- **Translate**: `translate-x-{n}`, `translate-y-{n}`
- **Skew**: `skew-x-{n}`, `skew-y-{n}` (degrees)
- **Transform Origin**: `origin-center`, `origin-top`, `origin-top-right`, `origin-right`, `origin-bottom-right`, `origin-bottom`, `origin-bottom-left`, `origin-left`, `origin-top-left`

### Transitions

- **Transition Property**: `transition-none`, `transition-all`, `transition-colors`, `transition-opacity`, `transition-shadow`, `transition-transform`
- **Transition Duration**: `duration-{ms}` (e.g., `duration-300`, `duration-500`)
- **Transition Delay**: `delay-{ms}`
- **Transition Timing**: `ease-linear`, `ease-in`, `ease-out`, `ease-in-out`

### Positioning

- **Position**: `static`, `fixed`, `absolute`, `relative`, `sticky`
- **Top/Right/Bottom/Left**: `top-{n}`, `right-{n}`, `bottom-{n}`, `left-{n}`
- **Inset**: `inset-{n}`, `inset-x-{n}`, `inset-y-{n}`
- **Z-Index**: `z-{n}` (e.g., `z-10`, `z-50`)

### Overflow

- **Overflow**: `overflow-auto`, `overflow-hidden`, `overflow-clip`, `overflow-visible`, `overflow-scroll`
- **Overflow X**: `overflow-x-auto`, `overflow-x-hidden`, `overflow-x-clip`, `overflow-x-visible`, `overflow-x-scroll`
- **Overflow Y**: `overflow-y-auto`, `overflow-y-hidden`, `overflow-y-clip`, `overflow-y-visible`, `overflow-y-scroll`

### Visibility

- **Visibility**: `visible`, `invisible`, `collapse`

### Cursor

- **Cursor Types**: `cursor-auto`, `cursor-default`, `cursor-pointer`, `cursor-wait`, `cursor-text`, `cursor-move`, `cursor-help`, `cursor-not-allowed`, `cursor-none`, `cursor-context-menu`, `cursor-progress`, `cursor-cell`, `cursor-crosshair`, `cursor-vertical-text`, `cursor-alias`, `cursor-copy`, `cursor-no-drop`, `cursor-grab`, `cursor-grabbing`, `cursor-all-scroll`, `cursor-col-resize`, `cursor-row-resize`, `cursor-n-resize`, `cursor-e-resize`, `cursor-s-resize`, `cursor-w-resize`, `cursor-ne-resize`, `cursor-nw-resize`, `cursor-se-resize`, `cursor-sw-resize`, `cursor-ew-resize`, `cursor-ns-resize`, `cursor-nesw-resize`, `cursor-nwse-resize`, `cursor-zoom-in`, `cursor-zoom-out`

### Pointer Events & User Select

- **Pointer Events**: `pointer-events-none`, `pointer-events-auto`
- **User Select**: `select-none`, `select-text`, `select-all`, `select-auto`

### Object Fit & Position

- **Object Fit**: `object-contain`, `object-cover`, `object-fill`, `object-none`, `object-scale-down`
- **Object Position**: `object-bottom`, `object-center`, `object-left`, `object-left-bottom`, `object-left-top`, `object-right`, `object-right-bottom`, `object-right-top`, `object-top`

### Aspect Ratio

- **Aspect Ratio**: `aspect-auto`, `aspect-square`, `aspect-video`, `aspect-{w}-{h}` (e.g., `aspect-16-9`)

### Float & Clear

- **Float**: `float-right`, `float-left`, `float-none`
- **Clear**: `clear-left`, `clear-right`, `clear-both`, `clear-none`

### Box Sizing

- **Box Sizing**: `box-border`, `box-content`

### Isolation

- **Isolation**: `isolate`, `isolation-auto`

### List Styles

- **List Style Type**: `list-none`, `list-disc`, `list-decimal`
- **List Style Position**: `list-inside`, `list-outside`

### Appearance

- **Appearance**: `appearance-none`, `appearance-auto`

### Resize

- **Resize**: `resize-none`, `resize-y`, `resize-x`, `resize`

### Scroll Behavior

- **Scroll Behavior**: `scroll-auto`, `scroll-smooth`
- **Scroll Snap Align**: `snap-start`, `snap-end`, `snap-center`, `snap-align-none`
- **Scroll Snap Stop**: `snap-normal`, `snap-always`
- **Scroll Snap Type**: `snap-none`, `snap-x`, `snap-y`, `snap-both`, `snap-mandatory`, `snap-proximity`

### Scroll Margin & Padding

- **Scroll Margin**: `scroll-m-{n}`, `scroll-mx-{n}`, `scroll-my-{n}`, `scroll-mt-{n}`, `scroll-mr-{n}`, `scroll-mb-{n}`, `scroll-ml-{n}`
- **Scroll Padding**: `scroll-p-{n}`, `scroll-px-{n}`, `scroll-py-{n}`, `scroll-pt-{n}`, `scroll-pr-{n}`, `scroll-pb-{n}`, `scroll-pl-{n}`

### Touch Action

- **Touch Action**: `touch-auto`, `touch-none`, `touch-pan-x`, `touch-pan-left`, `touch-pan-right`, `touch-pan-y`, `touch-pan-up`, `touch-pan-down`, `touch-pinch-zoom`, `touch-manipulation`

### Will Change

- **Will Change**: `will-change-auto`, `will-change-scroll`, `will-change-contents`, `will-change-transform`

### Columns

- **Columns**: `columns-{n}`

### Break After/Before/Inside

- **Break After**: `break-after-{value}`
- **Break Before**: `break-before-{value}`
- **Break Inside**: `break-inside-{value}`

## Arbitrary Values

For values not covered by the standard scale, use square brackets `[]`:

```python
Container(
    style="w-[350px] bg-[#1a2b3c] z-[100] top-[50px] fs-[24px]"
)
```

**Arbitrary value features:**
- Use underscores for spaces: `bg-[url('image.jpg')]` → `bg-[url('image.jpg')]`
- Works with any property: `p-[20px]`, `m-[5%]`, `w-[calc(100%-50px)]`

## State Variants

You can define styles for specific states using `hover_style` and `active_style` arguments.

```python
Button(
    "Click Me",
    style="bg-blue-500 text-white px-4 py-2 rounded transition-all duration-300",
    hover_style="bg-blue-600 shadow-lg scale-105",
    active_style="bg-blue-700 scale-95"
)
```

## Complete Example Styling

```python
from dars.all import *

app = App("Styling Demo")

@route("/")
def index():
    return Page(
        Container(
            # Header with gradient text
            Text(
                "Welcome to Dars",
                style="fs-[48px] font-black text-center mb-8"
            ),
            
            # Card with new colors
            Container(
                Text("Cyan Card", style="text-xl font-bold mb-2"),
                Text("Using the new cyan color palette", style="text-cyan-100"),
                style="bg-cyan-600 p-6 rounded-xl shadow-xl mb-4"
            ),
            
            Container(
                Text("Emerald Card", style="text-xl font-bold mb-2"),
                Text("With emerald green background", style="text-emerald-100"),
                style="bg-emerald-600 p-6 rounded-xl shadow-xl mb-4"
            ),
            
            # Interactive button
            Button(
                "Hover Me",
                style="bg-fuchsia-500 text-white px-6 py-3 rounded-lg transition-all duration-300",
                hover_style="bg-fuchsia-600 scale-110 shadow-2xl",
                active_style="scale-95"
            ),
            
            style="max-w-4xl mx-auto p-8"
        ),
        style="min-h-screen bg-gradient-to-br from-slate-50 to-zinc-100"
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

## Performance

The parsing happens in Python before the HTML/CSS is generated. This means:

1. **Zero Runtime Overhead**: The browser receives standard CSS
2. **No JavaScript Dependency**: No need to load a large utility CSS library or run JS parsers in the browser
3. **Optimized Output**: Only the styles you use are generated (as inline styles or extracted CSS)
4. **Python-Native**: No Node.js, PostCSS, or build tools required

## Best Practices

1. **Use semantic spacing**: Stick to the `0.25rem` scale (4, 8, 12, 16, etc.) for consistency
2. **Leverage the color palette**: Use the predefined color shades for a cohesive design
3. **Combine with transitions**: Add `transition-all duration-300` for smooth hover effects
4. **Use arbitrary values sparingly**: Prefer standard utilities when possible
5. **Keep it readable**: Break long utility strings into multiple lines if needed

```python
style="""
    bg-gradient-to-r from-purple-600 to-pink-600
    text-white px-8 py-4 rounded-xl shadow-2xl
    transition-all duration-300
"""
```

---

For animations, see the [Animation System](animations.md) documentation.
