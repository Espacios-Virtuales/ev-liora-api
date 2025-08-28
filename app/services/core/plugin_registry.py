import importlib, json, importlib.resources as pkgres
from typing import List, Dict, Any
from .plugin_contracts import SkillPlugin

class PluginRegistry:
    def __init__(self):
        self._plugins: List[SkillPlugin] = []
        self._manifests: Dict[str, Dict[str, Any]] = {}

    def load(self, module_paths: List[str]):
        for path in module_paths:
            mod = importlib.import_module(path)                     # p.ej. "app.plugins.ecommerce.plugin"
            plugin: SkillPlugin = getattr(mod, "get_plugin")()
            self._plugins.append(plugin)
            # intenta leer manifest.json del paquete del plugin
            pkg = path.rsplit(".", 1)[0]                            # "app.plugins.ecommerce"
            try:
                with pkgres.files(pkg).joinpath("manifest.json").open("r", encoding="utf-8") as f:
                    self._manifests[plugin.name] = json.load(f)
            except Exception:
                self._manifests[plugin.name] = {"name": plugin.name, "version": plugin.version, "intents": plugin.intents}

    def find_for_intent(self, intent: str) -> List[SkillPlugin]:
        return [p for p in self._plugins if p.can_handle(intent)]

    def manifest(self, plugin_name: str) -> Dict[str, Any]:
        return self._manifests.get(plugin_name, {})
