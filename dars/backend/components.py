from __future__ import annotations
from typing import Any, Union
import json

from dars.scripts.dscript import dScript, RawJS

# VDOM builder to serialize Component -> vdom dict
try:
    from dars.exporters.web.vdom import VDomBuilder
    from dars.core.component import Component
except Exception:
    VDomBuilder = None  # type: ignore
    Component = object  # type: ignore


def deleteComp(id: str) -> dScript:
    """Return a dScript that deletes a component on the client by DOM id.
    Calls: Dars.runtime.deleteComponent(id)
    """
    code = f"if (window.Dars && window.Dars.runtime && typeof window.Dars.runtime.deleteComponent === 'function') window.Dars.runtime.deleteComponent({json.dumps(id)});"
    return dScript(code=code)


def createComp(target: Union[Component, Any], root: Union[str, Component], position: str = "append") -> dScript:
    """Return a dScript that creates a new component on the client.
    Uses compiled HTML + metadata instead of VDOM.

    - target: Component instance (or callable returning one)
    - root: parent DOM id (or Component with .id)
    - position: "append" | "prepend" | "before:id" | "after:id"
    """
    # Normalize root id
    if isinstance(root, Component):  # type: ignore
        root_id = getattr(root, 'id', None)
    else:
        root_id = str(root)
    if not root_id:
        return dScript(code="/* Dars.createComp: invalid root id */")

    # Normalize/create component
    comp = target
    try:
        if callable(target) and not isinstance(target, Component):  # type: ignore
            comp = target()
    except Exception:
        pass

    # Build comp_data using VDomBuilder for events + manual HTML rendering
    comp_data: dict[str, Any] = {}
    if VDomBuilder is not None and isinstance(comp, Component):  # type: ignore
        try:
            builder = VDomBuilder()
            vdom_data = builder.build(comp)  # type: ignore
            events_map = dict(getattr(builder, 'events_map', {}))  # type: ignore
            
            # Extract lifecycle
            lifecycle = {}
            def _extract_lifecycle(node):
                if node.get('lifecycle'):
                    lifecycle[node['id']] = node['lifecycle']
                for child in node.get('children', []):
                    _extract_lifecycle(child)
            _extract_lifecycle(vdom_data)
            
            # Build HTML from VDOM structure for runtime insertion
            def _vdom_to_html(vnode):
                if not vnode:
                    return ''
                tag_map = {
                    'Text': 'span', 'Button': 'button', 'Section': 'section',
                    'Div': 'div', 'Container': 'div', 'Input': 'input',
                    'Link': 'a', 'Image': 'img', 'Video': 'video', 'Audio': 'audio',
                    'Select': 'select', 'Textarea': 'textarea', 'Checkbox': 'input',
                    'RadioButton': 'input', 'Slider': 'input', 'DatePicker': 'input',
                    'ProgressBar': 'div', 'Spinner': 'div', 'Tooltip': 'div',
                    'Markdown': 'div', 'Head': 'div', 'Outlet': 'div',
                    'Show': 'div', 'Each': 'div', 'Card': 'div', 'Modal': 'div',
                    'Navbar': 'nav', 'Table': 'table', 'Tabs': 'div',
                    'Accordion': 'div', 'FileUpload': 'div', 'FlexLayout': 'div',
                    'GridLayout': 'div', 'AnchorPoint': 'div',
                }
                tag = tag_map.get(vnode.get('type', ''), 'div')
                attrs = []
                
                vid = vnode.get('id')
                if vid:
                    attrs.append(f'id="{vid}"')
                
                vclass = vnode.get('class')
                if vclass:
                    attrs.append(f'class="{vclass}"')
                
                vstyle = vnode.get('style', {})
                if vstyle:
                    style_str = '; '.join([f"{k}: {v}" for k, v in vstyle.items()])
                    attrs.append(f'style="{style_str}"')
                
                vprops = vnode.get('props', {})
                for pk, pv in vprops.items():
                    if pk not in ('id', 'class', 'style', 'children', 'parent'):
                        if isinstance(pv, bool):
                            if pv:
                                attrs.append(pk)
                        elif pv is not None:
                            attrs.append(f'{pk}="{pv}"')
                
                attrs_str = ' '.join(attrs)
                
                vtext = vnode.get('text')
                vchildren = vnode.get('children', [])
                
                if vtext:
                    return f'<{tag} {attrs_str}>{vtext}</{tag}>'
                elif vchildren:
                    children_html = ''.join([_vdom_to_html(c) for c in vchildren])
                    return f'<{tag} {attrs_str}>{children_html}</{tag}>'
                else:
                    return f'<{tag} {attrs_str}></{tag}>'
            
            html = _vdom_to_html(vdom_data)
            
            comp_data = {
                'html': html,
                'id': vdom_data.get('id'),
                'type': vdom_data.get('type'),
                'events': events_map,
                'lifecycle': lifecycle,
                'states': [],
                'bindings': ''
            }
        except Exception:
            comp_data = {
                'html': f'<div id="{root_id}">{str(comp)}</div>',
                'id': None,
                'type': 'Div',
                'events': {},
                'lifecycle': {},
                'states': [],
                'bindings': ''
            }
    else:
        comp_data = {
            'html': f'<div>{str(comp)}</div>',
            'id': None,
            'type': 'Div',
            'events': {},
            'lifecycle': {},
            'states': [],
            'bindings': ''
        }

    code = (
        "try{ (function(){\n"
        f"  const rootId = {json.dumps(root_id)};\n"
        f"  const compData = {json.dumps(comp_data)};\n"
        f"  const pos = {json.dumps(position)};\n"
        "  if (globalThis.Dars && typeof Dars.runtime.createComponent === 'function') {\n"
        "    Dars.runtime.createComponent(rootId, compData, pos);\n"
        "  } else { console.warn('[Dars] runtime.createComponent not available'); }\n"
        "})(); }catch(e){ console.error(e); }"
    )
    return dScript(code=code)


def updateComp(target: Union[str, Component], **kwargs) -> dScript:
    """
    Update a component's state/properties by ID or reference.
    
    Args:
        target: Component instance or string ID
        **kwargs: Properties to update (text, style, class_name, etc.)
    """
    # Resolve ID
    if hasattr(target, 'id') and target.id:
        target_id = target.id
    else:
        target_id = str(target)
        
    # Build payload similar to this().state()
    parts = [f"id: '{target_id}'", "dynamic: true"]
    
    for k, v in kwargs.items():
        if isinstance(v, dScript):
            expr = (v.code or "").rstrip()
            if expr.endswith(";"):
                expr = expr[:-1]
            parts.append(f"{k}: {expr}")
        elif hasattr(v, 'code'):
            expr = (getattr(v, 'code', "") or "").rstrip()
            if expr.endswith(";"):
                expr = expr[:-1]
            parts.append(f"{k}: {expr}")
        elif k == 'style' and isinstance(v, dict):
            parts.append(f"style: {json.dumps(v)}")
        elif k == 'attrs' and isinstance(v, dict):
            parts.append(f"attrs: {json.dumps(v)}")
        elif k == 'classes' and isinstance(v, dict):
            parts.append(f"classes: {json.dumps(v)}")
        else:
            parts.append(f"{k}: {json.dumps(v)}")
            
    payload = ", ".join(parts)
    
    code = (
        "(async () => {\n"
        "  try {\n"
        "    let ch = window.__DARS_CHANGE_FN;\n"
        "    if (!ch) {\n"
        "      if (window.Dars && typeof window.Dars.change === 'function') {\n"
        "        ch = window.Dars.change.bind(window.Dars);\n"
        "      } else {\n"
        "        const m = await import('./lib/dars.min.js');\n"
        "        ch = (m.change || (m.default && m.default.change));\n"
        "      }\n"
        "      if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;\n"
        "    }\n"
        f"    if (typeof ch === 'function') ch({{{payload}}});\n"
        "  } catch (e) { /* noop */ }\n"
        "})();\n"
    )

    return dScript(code=code)
