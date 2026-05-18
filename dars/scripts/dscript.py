# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Optional, Dict, Any
from .script import Script

class dScript(Script):
    """
    Script that can be defined as:
    - Structured DAP action (data={...}) - PREFERRED, secure
    - Inline JS code (code="...") - Legacy, converted to DAP at compile-time
    - External file reference (file_path="...") - Legacy
    
    Security: At browser runtime, only structured DAP actions are executed.
    The 'code' parameter is for backward compatibility and developer convenience,
    but is converted to structured actions during export.
    """
    def __init__(
        self, 
        code: Optional[str] = None, 
        file_path: Optional[str] = None, 
        data: Optional[Dict[str, Any]] = None,
        target_language: str = "javascript", 
        module: bool = False
    ):
        super().__init__(target_language, module=module)
        
        # Validate: need exactly one of code, file_path, or data
        provided = sum([code is not None, file_path is not None, data is not None])
        if provided == 0:
            raise ValueError("You must specify one of: 'data' (DAP action), 'code' (inline), or 'file_path' (external).")
        if provided > 1:
            raise ValueError("You can only specify one of: 'data', 'code', or 'file_path'.")
        
        self.code = code
        self.file_path = file_path
        self.data = data  # Structured DAP action
    
    def get_action(self) -> Optional[Dict[str, Any]]:
        """Return structured DAP action for secure browser execution.
        
        This is the primary method used by the exporter to get the action
        that will be dispatched at runtime. Returns None if this is a
        legacy code-based script that hasn't been converted.
        """
        if self.data is not None:
            return self.data
        return None
    
    def has_action(self) -> bool:
        """Check if this script has a structured DAP action."""
        return self.data is not None

    def get_code(self) -> str:
        """Get raw JS code (legacy method for backward compatibility).
        
        Note: This method is used for legacy inline scripts. New code should
        use get_action() instead and let the DAP dispatcher handle execution.
        """
        if self.code is not None:
            return self.code
        elif self.file_path is not None:
            try:
                with open(self.file_path, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"The script file was not found: {self.file_path}")
        elif self.data is not None:
            return compile_action(self.data)
        else:
            raise ValueError("No code, file path, or action data defined for this dScript.")


    def then(self, script: 'dScript') -> 'dScript':
        """
        Chain another script to execute after this one resolves.
        Wraps the current script in an async IIFE if needed and appends .then().
        """
        current_code = self.get_code().strip()
        next_code = script.get_code().strip()
        
        combined_code = f"""
(async () => {{
    try {{
        const result = await {current_code};
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => {{ 
            {next_code} 
        }})(result);
        return result;
    }} catch (e) {{
        console.error("Chained script error:", e);
        throw e;
    }}
}})()
""".strip()
        return dScript(code=combined_code)

    # Helper for placeholder argument
    ARG = "value"

def compile_val(v, is_async=False):
    """Recursively compile DAP expressions/values into native JS code strings."""
    import json
    
    def _ser(obj):
        if isinstance(obj, RawJS):
            return obj.code
        if hasattr(obj, 'get_code'):
            return obj.get_code()
        if hasattr(obj, '_to_structure'):
            return obj._to_structure()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return str(obj)

    if isinstance(v, RawJS):
        return v.code
    if hasattr(v, 'get_code'):
        code = v.get_code()
        return f"(await {code})" if is_async else code
    if hasattr(v, '_to_structure'):
        v = v._to_structure()
        
    # Handle basic types
    if isinstance(v, (int, float, bool, type(None))):
        return json.dumps(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    
    # Handle collections
    if isinstance(v, list):
        items = [compile_val(i, is_async=is_async) for i in v]
        return f"[{', '.join(items)}]"
    
    if isinstance(v, dict) and 'op' not in v:
        pairs = [f"{json.dumps(k)}: {compile_val(v2, is_async=is_async)}" for k, v2 in v.items()]
        return f"{{ {', '.join(pairs)} }}"

    if not isinstance(v, dict) or 'op' not in v:
        # Fallback for unknown objects
        return json.dumps(v, ensure_ascii=False, default=_ser)
    
    op = v.get('op', '')
    args = v.get('args', {})
    
    if op in ('get_state', 'state_get', 'get_state_value'):
        sid = args.get('id') or args.get('state_id', '')
        prop = args.get('property') or args.get('prop_name', 'text')
        return f"((window.Dars && window.Dars.getState('{sid}') && window.Dars.getState('{sid}').values && window.Dars.getState('{sid}').values['{prop}'] !== undefined) ? window.Dars.getState('{sid}').values['{prop}'] : 0)"
    
    elif op == 'get_dom_value':
        sel = args.get('selector', '')
        return f"(function() {{ if (window.__DARS_VREF_VALUES__ && {json.dumps(sel)} in window.__DARS_VREF_VALUES__) return window.__DARS_VREF_VALUES__[{json.dumps(sel)}]; var _e = document.querySelector({json.dumps(sel)}); if(!_e) return ''; return (_e.tagName === 'INPUT' || _e.tagName === 'SELECT' || _e.tagName === 'TEXTAREA') ? _e.value : (_e.textContent || ''); }})()"
    
    elif op == 'transform':
        sub = compile_val(args.get('input'), is_async=is_async)
        method = args.get('method', '')
        if method == 'int':
            return f"parseInt({sub}, 10)"
        elif method == 'float':
            return f"parseFloat({sub})"
        elif method == 'upper':
            return f"String({sub}).toUpperCase()"
        elif method == 'lower':
            return f"String({sub}).toLowerCase()"
        elif method == 'trim':
            return f"String({sub}).trim()"
        elif method == 'length':
            return f"String({sub} || '').trim().length"
        elif method == 'is_email':
            return f"/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(String({sub} || '').trim())"
        elif method == 'test_pattern':
            pat = json.dumps(args.get('pattern', ''))
            return f"(function() {{ try {{ return new RegExp({pat}).test(String({sub} || '')); }} catch(_) {{ return false; }} }})()"
        elif method == 'validate_operator':
            ops = json.dumps(args.get('valid_ops', ['+', '-', '*', '/']), default=_ser)
            return f"(({ops}).includes({sub}) ? {sub} : '+')"
        return sub
    
    elif op == 'bool_expr':
        left = compile_val(args.get('left'), is_async=is_async)
        right = compile_val(args.get('right'), is_async=is_async)
        op_map = {
            '==': '==', '===': '===', '!=': '!=', '!==': '!==',
            '>': '>', '<': '<', '>=': '>=', '<=': '<=',
            '&&': '&&', '||': '||'
        }
        js_op = op_map.get(args.get('operator'), '==')
        return f"({left} {js_op} {right})"
    
    elif op == 'math_expr':
        left = compile_val(args.get('left'), is_async=is_async)
        right = compile_val(args.get('right'), is_async=is_async)
        js_op = args.get('operator', '+')
        
        if isinstance(js_op, dict):
            # Dynamic operator
            op_val = compile_val(js_op, is_async=is_async)
            return f"((l, o, r) => {{ switch(String(o).trim()) {{ case '+': return Number(l) + Number(r); case '-': return Number(l) - Number(r); case '*': return Number(l) * Number(r); case '/': return Number(l) / Number(r); case '%': return Number(l) % Number(r); case '**': return Math.pow(Number(l), Number(r)); default: return Number(l) + Number(r); }} }})({left}, {op_val}, {right})"
        
        # Static operator
        if js_op == '+':
            # We use native JS `+` so that string concatenation works correctly.
            # If the user wants strict numeric addition from a DOM string, they must use `.float()` or `.int()`.
            return f"({left} + {right})"
        
        # Use Number() for other arithmetic ops to ensure numeric results
        return f"(Number({left} || 0) {js_op} Number({right} || 0))"
    
    elif op == 'cond_expr':
        cond = compile_val(args.get('condition'), is_async=is_async)
        t_val = compile_val(args.get('true_val'), is_async=is_async)
        f_val = compile_val(args.get('false_val'), is_async=is_async)
        return f"({cond} ? {t_val} : {f_val})"
    
    elif op in ('not_expr', 'not'):
        val = compile_val(args.get('value', args), is_async=is_async)
        return f"(!{val})"
    
    elif op == 'str_expr':
        parts = args.get('parts', [])
        if not parts and isinstance(args, list): parts = args
        js_parts = [compile_val(p, is_async=is_async) for p in parts]
        return " + ".join([f"String({p})" for p in js_parts])
    
    elif op == 'inline':
        return args.get('code', '')
    
    # Fallback
    return json.dumps(v, ensure_ascii=False, default=_ser)

def compile_action(action):
    """Compile a DAP action dict into native JS code."""
    import json
    
    def _ser(obj):
        if isinstance(obj, RawJS):
            return obj.code
        if hasattr(obj, 'get_code'):
            return obj.get_code()
        if hasattr(obj, '_to_structure'):
            return obj._to_structure()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return str(obj)

    if isinstance(action, RawJS):
        return action.code
    if hasattr(action, '_to_structure'):
        action = action._to_structure()
    if not isinstance(action, dict):
        return json.dumps(action, ensure_ascii=False, default=_ser)
        
    op = action.get('op', '')
    args = action.get('args', {})
    
    if op == 'change':
        # Extract meta properties
        target_id = args.get('id', '')
        is_dynamic = args.get('dynamic', False)
        
        # Gather and compile properties (always async for actions)
        kv_pairs = []
        for k, v in args.items():
            if k in ('id', 'dynamic'): continue
            
            if k == 'attrs' and isinstance(v, dict):
                attr_pairs = [f"{json.dumps(ak)}: {compile_val(av, is_async=True)}" for ak, av in v.items()]
                kv_pairs.append(f"attrs: {{ {', '.join(attr_pairs)} }}")
            elif k == 'style' and isinstance(v, dict):
                style_pairs = [f"{json.dumps(sk)}: {compile_val(sv, is_async=True)}" for sk, sv in v.items()]
                kv_pairs.append(f"style: {{ {', '.join(style_pairs)} }}")
            elif k == 'classes' and isinstance(v, dict):
                cls_parts = []
                for ck, cv in v.items():
                    if isinstance(cv, list):
                        comp_list = [f"{compile_val(it, is_async=True)}" for it in cv]
                        cls_parts.append(f"{json.dumps(ck)}: [{', '.join(comp_list)}]")
                    else:
                        cls_parts.append(f"{json.dumps(ck)}: {compile_val(cv, is_async=True)}")
                kv_pairs.append(f"classes: {{ {', '.join(cls_parts)} }}")
            else:
                # Standard property
                kv_pairs.append(f"{json.dumps(k)}: {compile_val(v, is_async=True)}")
        
        # Construct call
        id_j = json.dumps(target_id)
        dyn_j = "true" if is_dynamic else "false"
        kv_str = ", " + ", ".join(kv_pairs) if kv_pairs else ""
        return f"if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change({{ id: {id_j}, dynamic: {dyn_j}{kv_str} }});"

    elif op == 'start_loop':
        id_j = json.dumps(args.get('id', ''))
        cfg_pairs = []
        for k, v in args.items():
            if k == 'id': continue
            cfg_pairs.append(f"{json.dumps(k)}: {compile_val(v, is_async=True)}")
        cfg_str = "{{ " + ", ".join(cfg_pairs) + " }}"
        return f"if (window.Dars && typeof window.Dars.startLoop === 'function') window.Dars.startLoop({id_j}, {cfg_str});"
    
    elif op == 'stop_loop':
        id_j = json.dumps(args.get('id', ''))
        return f"if (window.Dars && typeof window.Dars.stopLoop === 'function') window.Dars.stopLoop({id_j});"
        
    elif op == 'navigate':
        path = args.get('path', '/')
        return f"window.location.href = {json.dumps(path)};"
    elif op == 'sequence':
        # Compile a sequence of actions into sequential JS statements
        actions_list = args if isinstance(args, list) else args.get('actions', [])
        parts = []
        for sub in actions_list:
            if sub:
                parts.append(compile_action(sub))
        return "\n".join(parts)
    elif op in ('vref_update', 'vref_set'):
        selector = args.get('selector', '')
        value = args.get('value')
        value_js = compile_val(value, is_async=True)
        return (
            f"(async () => {{ try {{ const _dap = await import('./lib/dap.js'); "
            f"await _dap.dispatch({{op:'vref_update',args:{{selector:{json.dumps(selector)},value:{value_js}}}}});"
            f"}} catch(_e) {{}} }})();"
        )
    elif op == 'network_request':
        action_json = json.dumps(action, ensure_ascii=False, default=str)
        return (
            f"(async () => {{ try {{ const _dap = await import('./lib/dap.js'); "
            f"await _dap.dispatch({action_json}); }} catch(_e) {{ "
            f"console.error('[Dars] network_request failed', _e); }} }})();"
        )
    elif op == 'dom_set_text':
        eid = args.get('id', '')
        text_expr = compile_val(args.get('text', ''), is_async=True)
        return f"(function(){{ var _e = document.getElementById({json.dumps(eid)}); if(_e) _e.textContent = String({text_expr}); }})();"
    elif op == 'conditional':
        cond = compile_val(args.get('condition'), is_async=True)
        on_true = compile_action(args['on_true']) if args.get('on_true') else ''
        on_false = compile_action(args['on_false']) if args.get('on_false') else ''
        return f"if ({cond}) {{ {on_true} }} else {{ {on_false} }}"
    elif op == 'storage_set':
        key = json.dumps(args.get('key', ''))
        val_expr = compile_val(args.get('value', ''), is_async=True)
        return f"localStorage.setItem({key}, String({val_expr}));"
    elif op == 'storage_remove':
        key = json.dumps(args.get('key', ''))
        return f"localStorage.removeItem({key});"
    elif op == 'navigate_new':
        path = args.get('path', '/')
        return f"window.open({json.dumps(path)}, '_blank');"
    elif op == 'reload':
        return "window.location.reload();"
    elif op == 'class_add':
        eid = args.get('id', '')
        cn = args.get('className', '')
        return f"var _el = document.getElementById({json.dumps(eid)}); if(_el) _el.classList.add({json.dumps(cn)});"
    elif op == 'class_remove':
        eid = args.get('id', '')
        cn = args.get('className', '')
        return f"var _el = document.getElementById({json.dumps(eid)}); if(_el) _el.classList.remove({json.dumps(cn)});"
    elif op == 'class_toggle':
        eid = args.get('id', '')
        cn = args.get('className', '')
        return f"var _el = document.getElementById({json.dumps(eid)}); if(_el) _el.classList.toggle({json.dumps(cn)});"
    elif op == 'clipboard_copy_element':
        eid = args.get('id', '')
        return f"var _el = document.getElementById({json.dumps(eid)}); if(_el) navigator.clipboard.writeText(_el.textContent || '');"
    elif op == 'clipboard_write':
        text_expr = compile_val(args.get('text', ''), is_async=True)
        return f"navigator.clipboard.writeText(String({text_expr}));"
    elif op == 'alert':
        msg_expr = compile_val(args.get('message', ''), is_async=True)
        return f"alert(String({msg_expr}));"
    elif op == 'log':
        msg_expr = compile_val(args.get('message', ''), is_async=True)
        return f"console.log({msg_expr});"
    elif op == 'modal_show':
        id_expr = compile_val(args.get('id', ''), is_async=True)
        return f"if (window.DarsModal) window.DarsModal.show({id_expr});"
    elif op == 'modal_hide':
        id_expr = compile_val(args.get('id', ''), is_async=True)
        return f"if (window.DarsModal) window.DarsModal.hide({id_expr});"
    else:
        # Generic DAP action — dispatch via dap.js
        # Use async import to ensure dap.js is loaded before dispatching
        action_json = json.dumps(action, ensure_ascii=False, default=str)
        return (
            f"(async () => {{ try {{ const _dap = await import('./lib/dap.js'); "
            f"await _dap.dispatch({action_json}); }} catch(_e) {{ "
            f"if (window.Dars && typeof window.Dars.dispatch === 'function') "
            f"window.Dars.dispatch({action_json}); }} }})();"
        )

class RawJS:
    """
    Wrapper to indicate that a string should be treated as raw JavaScript code
    instead of a string literal when serialized.
    """
    def __init__(self, code: str):
        self.code = code
    
    def then(self, next_script: Any) -> 'RawJS':
        """
        Chain another script to execute after this one resolves.
        Wraps the current script in an async IIFE if needed and runs next_script.
        """
        current_code = self.code.strip()
        
        if hasattr(next_script, 'code'):
            next_code = next_script.code.strip()
        elif hasattr(next_script, 'get_code'):
            next_code = next_script.get_code().strip()
        else:
            next_code = str(next_script).strip()
            
        combined_code = f"""
(async () => {{
    try {{
        const result = await {current_code};
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => {{ 
            {next_code} 
        }})(result);
        return result;
    }} catch (e) {{
        console.error("Chained script error:", e);
        throw e;
    }}
}})()
""".strip()
        return RawJS(code=combined_code)

    def __str__(self):
        return self.code
    
    def __repr__(self):
        return self.code

# Pythonic helper for dScript.ARG access
class _ArgHelper(RawJS):
    """Pythonic wrapper for dScript.ARG to avoid raw JS strings.
    
    Usage:
        Arg.text -> RawJS("dScript.ARG.text")
        Arg.value -> RawJS("dScript.ARG.value")
        Arg -> RawJS("dScript.ARG")
    """
    def __init__(self):
        super().__init__("dScript.ARG")

    def __getattr__(self, name: str):
        return RawJS(f"dScript.ARG.{name}")

# Singleton instance
Arg = _ArgHelper()

# Special constant for referencing dScript.ARG in .then() chains
ARG = "dScript.ARG"
