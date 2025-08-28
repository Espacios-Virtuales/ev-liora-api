from typing import Dict, Any, List, Protocol

class SkillPlugin(Protocol):
    name: str
    version: str
    intents: List[str]

    def can_handle(self, intent: str) -> bool: ...
    def handle(self, *, intent: str, message: str, ctx: Dict[str, Any], deps: Dict[str, Any]) -> Dict[str, Any]: ...
