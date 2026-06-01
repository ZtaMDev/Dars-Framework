# Operations in Dars (DAP)

Dars Action Protocol (DAP) is the secure command system that powers all client-side interactivity. Every event handler, animation, and state mutation compiles down to structured DAP payloads — never `eval()` or `new Function()`.

## All DAP Operations

### Navigation
| Operation | Description | Python Helper |
|---|---|---|
| `navigate` | Navigate to path | `goTo(path)` |
| `navigate_new` | Open in new tab | `goToNew(path)` |
| `reload` | Reload page | `reload()` |
| `history_back` | Go back | `historyBack()` |
| `history_forward` | Go forward | `historyForward()` |

### State Management
| Operation | Description | Python Helper |
|---|---|---|
| `change` | Change state value | `state.count.set(n)` |

### Modal
| Operation | Description | Python Helper |
|---|---|---|
| `modal_show` | Show modal | `showModal(id)` |
| `modal_hide` | Hide modal | `hideModal(id)` |

### DOM Visibility
| Operation | Description | Python Helper |
|---|---|---|
| `dom_show` | Show element | `show(id)` |
| `dom_hide` | Hide element | `hide(id)` |
| `dom_toggle` | Toggle visibility | `toggle(id)` |

### DOM Content
| Operation | Description | Python Helper |
|---|---|---|
| `dom_set_text` | Set text content | `setText(id, text)` |
| `dom_set_html` | Set inner HTML (sanitized) | `setHTML(id, html)` |
| `dom_set_style` | Set inline style | `setStyle(id, styles)` |
| `dom_set_value` | Set form value | `setValue(id, val)` |
| `dom_set_attr` | Set attribute | `setAttr(id, name, val)` |
| `dom_reflow` | Force browser reflow | `reflow(id)` |
| `dom_animate` | Animate element | `animate(id, keyframes)` |

### CSS Classes
| Operation | Description | Python Helper |
|---|---|---|
| `class_add` | Add CSS class | `addClass(id, cls)` |
| `class_remove` | Remove CSS class | `removeClass(id, cls)` |
| `class_toggle` | Toggle CSS class | `toggleClass(id, cls)` |

### Scroll
| Operation | Description | Python Helper |
|---|---|---|
| `scroll_to` | Scroll to position | `scrollTo(x, y)` |
| `scroll_top` | Scroll to top | `scrollTop()` |
| `scroll_bottom` | Scroll to bottom | `scrollBottom()` |
| `scroll_to_element` | Scroll element into view | `scrollToElement(id)` |

### Forms
| Operation | Description | Python Helper |
|---|---|---|
| `form_submit` | Submit form | `formSubmit(id)` |
| `form_reset` | Reset form | `formReset(id)` |
| `input_clear` | Clear input | `clearInput(id)` |
| `input_set` | Set input value | `inputSet(id, value)` |

### Clipboard
| Operation | Description | Python Helper |
|---|---|---|
| `clipboard_write` | Write to clipboard | `copyToClipboard(text)` |
| `clipboard_copy_element` | Copy element text | `copyElementText(id)` |

### Control Flow
| Operation | Description | Python Helper |
|---|---|---|
| `sequence` | Run actions in sequence | `sequence(*actions)` |
| `delay` | Delay then run action | `delay(ms, action)` |
| `conditional` | Conditionally run action | `condition(expr, then, else)` |

### VRef
| Operation | Description | Python Helper |
|---|---|---|
| `vref_update` | Update VRef value | `updateVRef(sel, val)` |
| `vref_get` | Get VRef value | — |

### Dynamic Components
| Operation | Description | Python Helper |
|---|---|---|
| `comp_create` | Create component dynamically | `createComp(data, root)` |
| `comp_delete` | Delete component | `deleteComp(id)` |
| `comp_update` | Update component props | `updateComp(id, props)` |

### Network
| Operation | Description | Python Helper |
|---|---|---|
| `fetch` | HTTP request | `fetch(url, ...)` |
| `call_server` | Call server action | `call_server(name, **kwargs)` |

### Dialogs
| Operation | Description | Python Helper |
|---|---|---|
| `alert` | Show alert | `alert(msg)` |
| `confirm` | Show confirmation | `confirm(msg, on_ok, on_cancel)` |
| `log` | Console log | `log(msg)` |

## Security Model

1. **Compile-time**: Python code is compiled to structured DAP `{op, args}` payloads
2. **No eval**: The browser runtime's `_dispatch()` function only executes predefined operations
3. **No new Function**: Dynamic scripts use secure IIFE injection, not `new Function()`
4. **DOMPurify**: All `dom_set_html` operations sanitize input before DOM injection
