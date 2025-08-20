# app/models/__init__.py
from app.extensions import db

try:    from .cliente import Cliente
except: pass
try:    from .usuario import Usuario
except: pass
try:    from .waba_account import WabaAccount
except: pass
try:    from .convo_state import ConvoState
except: pass
try:    from .conversation_log import ConversationLog
except: pass
try:    from .catalog_active import CatalogActive
except: pass
try:    from .catalog_snapshot import CatalogSnapshot
except: pass
try:    from .ingest_log import IngestLog
except: pass
try:    from .documento import Documento
except: pass
try:    from .membresia import Membresia
except: pass

# ★ añade estos si existen en tu repo (Alembic ya detectó 'client_contexts' y 'user_contexts')
try:    from .client_context import ClientContext
except: pass
try:    from .user_context import UserContext
except: pass

__all__ = [
    name for name in (
        "Cliente", "Usuario", "WabaAccount",
        "ConvoState", "ConversationLog",
        "CatalogActive", "CatalogSnapshot", "IngestLog",
        "Documento", "Membresia",
        "ClientContext", "UserContext",
    )
    if name in globals()
]
