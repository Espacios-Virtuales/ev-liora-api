
# 🧩 Guía de Plugins — Liora

Los **plugins** extienden el Core con nuevas capacidades conversacionales. Reemplazan a los *skills* tradicionales con:
- **Contrato mínimo** (`plugin_contracts.py`)
- **Registro central** (`plugin_registry.py`)
- **Manifiesto** por plugin (`manifest.json`)
- **Inyección de dependencias** de servicios core
- **Flags/políticas** por cliente/plan

## Estructura
```
app/plugins/<nombre>/
  plugin.py
  manifest.json
```

## Contrato (interface)
```python
# app/services/core/plugin_contracts.py
from typing import List, Dict, Any, Protocol

class SkillPlugin(Protocol):
    name: str
    version: str
    intents: List[str]

    def can_handle(self, intent: str) -> bool: ...
    def handle(self, *, intent: str, message: str, ctx: Dict[str, Any], deps: Dict[str, Any]) -> Dict[str, Any]: ...
```

## Registry (carga y permisos)
```python
# app/services/core/plugin_registry.py
import importlib, json
from pathlib import Path
from typing import List, Dict, Any

class PluginRegistry:
    def __init__(self):
        self._plugins = []
        self._manifests: Dict[str, Dict[str, Any]] = {}

    def load_from_paths(self, module_paths: List[str]):
        for path in module_paths:
            mod = importlib.import_module(path)
            plugin = mod.get_plugin()
            self._plugins.append(plugin)
            mf = Path(mod.__file__).parent / "manifest.json"
            if mf.exists():
                self._manifests[plugin.name] = json.loads(mf.read_text(encoding="utf-8"))
```

## Router (uso del registry)
```python
# services/core/router_service.py (extracto)
_registry.load_from_paths([
  "app.plugins.ecommerce.plugin",
  "app.plugins.vida_sana.plugin",
])

def handle_incoming(intent, message, ctx, deps):
    candidates = _registry.find_for_intent(intent)
    if not candidates:
        return {"type":"text","body":"No entendí. Escribe 'catalogo' o 'ayuda'."}
    return candidates[0].handle(intent=intent, message=message, ctx=ctx, deps=deps)
```

## Ejemplo: Plugin Ecommerce
```python
# app/plugins/ecommerce/plugin.py
class EcommercePlugin:
    name = "ecommerce"
    version = "0.1.0"
    intents = ["catalogo.ver","catalogo.buscar"]

    def can_handle(self, intent): return intent in self.intents
    def handle(self, *, intent, message, ctx, deps):
        items = deps["catalog_service"].get_active_summary(cliente_id=ctx["cliente_id"], limit=5)
        make = lambda it: f"• {it['name']} → " + deps["bitly_service"].shorten(it["url"], {"utm_source":"wa","utm_medium":"bot","utm_campaign":"catalogo"})
        body = "🛍️ Catálogo:
" + "\n".join(map(make, items)) if items else "No hay artículos activos."
        return {"type":"text","body":body}

def get_plugin(): return EcommercePlugin()
```

**manifest.json**
```json
{
  "name":"ecommerce",
  "version":"0.1.0",
  "intents":["catalogo.ver","catalogo.buscar"],
  "permissions":["catalog.read","bitly.shorten"],
  "limits":{"max_links":5}
}
```

## Migración desde skills
1. Mover `services/skills/ecommerce_skill.py` → `plugins/ecommerce/plugin.py`.
2. Pasar dependencias por `deps` (no import directo).
3. Definir intents explícitos y mapear desde NLU/regex.
4. Cargar plugin en `plugin_registry` y usar en `router_service`.
5. Añadir `manifest.json`; activar por flags/policy.
6. Tests unit/functional (mocks de services).

## Seguridad & Multi‑tenant
- Sin acceso directo a DB; todo por Core Services.
- Validar permisos del manifest antes de acciones (p. ej. `bitly.shorten`).
- Aplicar `policy_service` y feature flags por `cliente_id`.

## Métricas/Logs sugeridos
- `{plugin, version, intent, took_ms, errors}` en `ConversationLog.link_ctrs_json` o `meta`.
- CTR por link acortado (cuando aplica).
