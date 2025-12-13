# Markdown Template Example

## 📋 About This Template

This template demonstrates how to use the **Markdown Component** in Dars framework to render markdown files directly in your web application.

## 🚀 How It Works

### 1. Import Required Modules

```python
from dars.core.app import *
from personalizedcomp import *
from dars.components.basic.markdown import Markdown
```

### 2. Create the App Instance

```python
app = App(title="Component Customization")
```

### 3. Load Markdown from File

```python
markdown_component = Markdown(
    file_path="README.md",          # Path to your markdown file
    id="my-markdown",               # Unique ID for the component
    class_name="custom-markdown",   # Custom CSS class
    style={                         # Inline styles
        "padding": "20px", 
        "backgroundColor": "#f8f9fa"
    }
)
```

### 4. Wrap in Container

```python
Mic = Container(markdown_component)
```

### 5. Set as Root Component
```python
app.set_root(Mic)
```

### 6. Run the Application
```python
if __name__ == "__main__":
    app.rTimeCompile()
```

## 📁 File Structure
```
your-project/
├── main.py              # This template file
├── README.md           # Markdown file to render
├── personalizedcomp.py # Your custom components
└── requirements.txt    # Dependencies
```

## 🎨 Customization Options

### Styling
You can customize the appearance through:
- **Inline styles** via `style` parameter
- **CSS classes** via `class_name` parameter
- **Global CSS** in your stylesheet

# 🎨 Markdown Template with Dark Theme

## 🌙 Dark Theme Support

This template now includes **automatic dark theme support**! The Markdown component can switch between light and dark modes.

### How to Use Dark Theme

```python
# Enable dark theme on creation
markdown_component = Markdown(
    file_path="README.md",
    dark_theme=True,  # ← Set to True for dark mode
    style={"padding": "20px"}
)

# Or toggle dynamically
markdown_component.set_dark_theme(True)   # Enable dark theme
markdown_component.set_dark_theme(False)  # Disable dark theme


### Content Sources
- **File path**: Load from `.md` files
- **String content**: Direct markdown text
- **Dynamic updates**: Change content at runtime

## 🔄 Dynamic Content

Update markdown content dynamically:

```python
# Update from different file
markdown_component.update_content(new_file_path="other_docs.md")

# Or update with string content
markdown_component.update_content(new_content="# New Content\nYour markdown here")
```

## 📋 Supported Markdown Features

- ✅ Headers (`#`, `##`, `###`)
- ✅ **Bold** and *italic* text
- ✅ Lists (ordered and unordered)
- ✅ [Links](https://example.com)
- ✅ `Inline code` and code blocks (partialy supported)
- ✅ Tables
- ✅ Blockquotes
- ✅ Images
- ✅ Horizontal rules

## 🚨 Important Notes

1. **File Paths**: Use relative paths from your project root
2. **Encoding**: Files should be UTF-8 encoded
3. **File Existence**: Ensure the markdown file exists
4. **Dependencies**: Already installed with dars framework

## 💡 Usage Ideas

- Documentation pages
- Blog posts
- Content management systems
- Tutorial sections
- FAQ pages
- Project readmes

## 🛠️ Troubleshooting

**Common issues:**
- `FileNotFoundError`: Check file path
- `ImportError`: Install markdown2
- `Encoding issues`: Use UTF-8 files

**Debug tips:**
```python
print(f"File exists: {os.path.exists('README.md')}")
```

## 📚 Next Steps

1. Add more markdown files
2. Create navigation between pages
3. Add custom CSS styling
4. Implement markdown editor functionality

---

*This template showcases the power of Dars framework for content-rich applications!*
```