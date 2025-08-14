# 🌐 EV-Liora-API

**EV-Liora-API** es una API desarrollada con Flask que integra funcionalidades de gestión de usuarios, membresías y documentos, así como la capacidad de interactuar con Google Sheets para procesar mensajes, especialmente aquellos provenientes de WhatsApp. Este proyecto forma parte del ecosistema de [Espacios Virtuales](https://espaciosvirtuales.lat), enfocado en brindar soluciones digitales conscientes.

## 📁 Estructura del Proyecto

```
ev-liora-api/
├── app/
│   ├── models/
│   │   ├── waba_account.py      # NUEVO (sustituye numero_whatsapp.py)
│   │   ├── cliente.py           # NUEVO
│   │   ├── catalog_active.py    # NUEVO
│   │   ├── catalog_snapshot.py  # NUEVO
│   │   ├── convo_state.py       # NUEVO
│   │   ├── ingest_log.py        # NUEVO
│   │   ├── usuario.py
│   │   ├── membresia.py
│   │   ├── documento.py
│   │   ├── chat_model.py
│   ├── controllers/
│   │   ├── meta_webhook_controller.py  # RENOMBRAR desde wsp_controller.py
│   │   ├── chat_controller.py
│   │   ├── documento_controller.py
│   │   ├── membresia_controller.py
│   │   ├── user_controller.py
│   ├── services/
│   │   ├── whatsapp_service.py
│   │   ├── router_service.py     # NUEVO: orquesta intención/slots y handoff
│   │   ├── catalog_service.py    # NUEVO: snapshots + validadores + activo
│   │   ├── bitly_service.py      # NUEVO: UTM + short links
│   │   ├── nlp_service.py        # NUEVO: fallback GPT-4o mini (opcional)
│   │   ├── chat_service.py
│   │   ├── documento_service.py
│   │   ├── membresia_service.py
│   └── views/
│       ├── whatsapp_view.py
│       └── api_view.py
```

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**

   ```
   git clone https://github.com/dutreras369/ev-liora-api.git
   cd ev-liora-api
   ```

2. **Crear y activar un entorno virtual:**

   ```
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**

   ```
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///liora.db
   ```

5. **Inicializar la base de datos:**

   ```
   flask shell
   >>> from app.models.db_models import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Ejecutar la aplicación:**

   ```
   flask run
   ```

   La API estará disponible en `http://localhost:5000/`.

## 🧪 Endpoints Principales

- **Usuarios:**
  - `POST /usuarios` – Crear un nuevo usuario.
  - `GET /usuarios` – Obtener la lista de usuarios.

- **WhatsApp:**
  - `POST /whatsapp` – Procesar mensajes entrantes de WhatsApp.

## 🔧 Configuración de Google Sheets

Para habilitar la interacción con Google Sheets:

1. **Crear credenciales de servicio en Google Cloud:**
   - Accede a [Google Cloud Console](https://console.cloud.google.com/).
   - Crea un proyecto y habilita las APIs de Google Sheets y Google Drive.
   - Crea una cuenta de servicio y descarga el archivo JSON de credenciales.

2. **Guardar el archivo de credenciales:**
   - Renombra el archivo descargado a `credenciales.json`.
   - Colócalo en la raíz del proyecto.

3. **Compartir el documento de Google Sheets:**
   - Comparte el documento con el correo electrónico de la cuenta de servicio.

## 📌 Notas Adicionales

- **Despliegue en Producción:**
  - Para desplegar la aplicación en un entorno de producción, considera utilizar servicios como Heroku, Render o Railway.
  - Asegúrate de configurar las variables de entorno adecuadas y utilizar una base de datos persistente.

- **Pruebas:**
  - Se recomienda implementar pruebas unitarias y de integración para asegurar la calidad del código.

- **Contribuciones:**
  - Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para discutir cambios importantes.

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
