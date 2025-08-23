
# 🚀 Despliegue en OHost (cPanel + Python/WSGI)

**Última actualización:** 2025-08-22 23:59 UTC  
**Alcance:** Liora (Flask + SQLAlchemy + Postgres externo) — *MVP sin scraper ni agente*

---

## 0) Enfoque
Usaremos **cPanel → Application Manager / Setup Python App** con **Passenger (WSGI)** para servir Flask, y **PostgreSQL externo** (Neon/Supabase) para evitar fricciones de base de datos en hosting compartido. SSL se gestiona con **AutoSSL** del proveedor. Variables sensibles via entorno en cPanel.

---

## 1) Pre‑requisitos en OHost
- Acceso a **cPanel** con *Setup Python App* habilitado.
- **SSH/SFTP** para `git clone` o subida de archivos.
- Dominio/subdominio apuntando a OHost y **SSL** activo (AutoSSL).
- Versión de **Python 3.10+** disponible.

---

## 2) Base de datos (externa recomendada)
- Crear Postgres en **Neon** o **Supabase** y obtener el **connection string** con `sslmode=require`.
- Formato recomendado para SQLAlchemy:
  ```
  postgresql+psycopg2://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require
  ```

---

## 3) Ajustes en el repo
### a) Requisitos
Añadir/asegurar en `requirements.txt` (versiones de ejemplo, ajustar a tu stack):
```
psycopg2-binary==2.9.9
python-dotenv==1.0.1
gunicorn==23.0.0    # opcional (útil local), en cPanel sirve Passenger
```
> Mantener Flask/Flask‑SQLAlchemy según tu `requirements.txt` actual.

### b) Archivo WSGI (`passenger_wsgi.py`) en la raíz del proyecto
```python
import os, sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_HOME = str(Path(__file__).resolve().parent)
if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

# Cargar .env si está presente
load_dotenv(os.path.join(PROJECT_HOME, ".env"))

from app import create_app
application = create_app()
```
> `application` es el objeto que Passenger expone.

### c) Configuración de entorno
Variables mínimas en cPanel (Application Manager → Edit):
```
FLASK_ENV=production
DATABASE_URL=postgresql+psycopg2://USER:PASS@HOST:5432/DB?sslmode=require
WABA_VERIFY_TOKEN=changeme
META_ACCESS_TOKEN=mock
BITLY_TOKEN=mock
JWT_SECRET=changeme
ENCRYPTION_KEY=changeme
LOG_LEVEL=INFO
```

---

## 4) Despliegue en cPanel (pasos)
1. **Crear App Python**: cPanel → *Setup Python App / Application Manager* → *Create Application*  
   - Python: 3.10+  
   - App Root: `liora` (o el path del proyecto)  
   - App URI: `/` (si será el sitio principal) o `/liora`  
   - WSGI file: `passenger_wsgi.py`
2. **Crear virtualenv** desde el panel (se crea automáticamente) y **Instalar dependencias** con *pip install -r requirements.txt* desde el botón o por **SSH** dentro del venv.
3. **Git/SFTP**: subir el repo a `~/liora` o clonar con `git clone`.  
4. **Variables de entorno**: añadir en *Application Manager → Edit → Environment Variables*.
5. **Reiniciar la App** desde cPanel para aplicar cambios.
6. **Probar** `GET /health` y endpoints de API (`/api/v1/...`).

---

## 5) Webhooks WhatsApp (Meta)
- Apuntar el **Webhook URL** a `https://tu-dominio.com/api/v1/webhook/meta`.
- **Verificación**: `GET /webhook/meta` con `hub.verify_token` (configurado vía env).  
- **Eventos**: `POST /webhook/meta` → enruta a `router_service` (MVP).

---

## 6) Logs y observabilidad básica
- Logs de acceso/error vía cPanel.  
- Logging de aplicación: `LOG_LEVEL=INFO` y traza por request.  
- (Opcional) Enviar logs a un collector externo (Papertrail/Logtail) usando handler Python.

---

## 7) Migraciones y seeds
- Ejecutar **Alembic** contra el Postgres externo desde local/CI:
  ```bash
  alembic upgrade head
  python scripts/seed_demo.py   # si aplica
  ```

---

## 8) Troubleshooting rápido
- **500 al arrancar**: revisar `passenger_wsgi.py` (ruta y `application`).  
- **Módulos faltantes**: reinstalar en el venv desde cPanel/SSH.  
- **Driver Postgres**: usar `psycopg2-binary` o `psycopg` con `?sslmode=require`.  
- **Rutas estáticas**: servirlas desde Flask o directorio `static/` mapeado por Passenger.  
- **Time‑outs**: evitar operaciones bloqueantes en request; mover tareas pesadas fuera del request (no aplican al MVP).

---

## 9) Checklist de “listo para OHost”
- [ ] `passenger_wsgi.py` en raíz y `create_app()` importable.
- [ ] `requirements.txt` actualizado e instalado en venv cPanel.
- [ ] `DATABASE_URL` (Neon/Supabase) con `sslmode=require`.
- [ ] Variables de entorno cargadas en cPanel (WABA/Bitly/JWT/etc.).
- [ ] App reiniciada y `GET /health` ok.
- [ ] Webhook Meta verificado.
- [ ] Catálogo `publish/activate` probado con CSV demo.

---

> **Nota**: Para staging, crear subdominio `staging.tu-dominio.com` con una segunda App Python en cPanel y otra base de datos/branch de Neon.
