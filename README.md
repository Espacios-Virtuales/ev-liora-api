# 🌐 EV-Liora-API

**EV-Liora-API** es una API desarrollada con Flask que integra gestión de usuarios, membresías y documentos, además de enrutar mensajes hacia *Skills* (Ecommerce, Vida Sana, Reciclaje y Código).  
Forma parte del ecosistema [Espacios Virtuales](https://espaciosvirtuales.lat), enfocado en soluciones digitales conscientes.

---

## 📁 Documentación

La documentación detallada está en [`docs/`](docs/):

- 📊 **Diagramas**
  - [Flujos principales](docs/diagrams/flow.md)
  - [Modelos de datos](docs/diagrams/models.md)
  - [Visión arquitectónica](docs/diagrams/vision.md)

- 🐞 **Proceso & Debug**
  - [Checklist de desarrollo](docs/debug/checklist.md)

- 🧩 **Módulos**
  - [Skills & extensiones](docs/modules/skills.md)

- 🌱 **Agente Vida Sana**
  - [README Agente Vida Sana](README_ev_agente_vida_sana.md)

- 🗂 **Estructura del Proyecto**
  - [Project Structure](docs/structure.md)

---

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/dutreras369/ev-liora-api.git
   cd ev-liora-api
   ```

2. **Crear y activar un entorno virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**

   Crear archivo `.env`:

   ```ini
   FLASK_APP=main.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///liora.db
   ```

5. **Inicializar la base de datos:**

   ```bash
   flask shell
   >>> from app.models.db_models import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Ejecutar la aplicación:**

   ```bash
   flask run
   ```

   Disponible en `http://localhost:5000/`.

---

## 🧪 Endpoints Principales

- **Usuarios**
  - `POST /usuarios` – Crear un nuevo usuario.
  - `GET /usuarios` – Obtener lista de usuarios.

- **WhatsApp**
  - `POST /whatsapp` – Procesar mensajes entrantes.

---

## 🔧 Configuración Google Sheets

1. Crear credenciales en [Google Cloud Console](https://console.cloud.google.com/).  
2. Guardar archivo `credenciales.json` en la raíz.  
3. Compartir el documento con el correo de la cuenta de servicio.  

---

## 📌 Estado del Proyecto

- [x] Base Flask multi-tenant (usuarios, clientes, waba account).  
- [x] Webhook Meta integrado.  
- [ ] Skill Ecommerce (catálogo + Bitly).  
- [ ] Skill Vida Sana.  
- [ ] Skill Reciclaje (Enraiza).  
- [ ] Skill Código (interno).  

👉 Detalle: [Checklist de desarrollo](docs/debug/checklist.md)

---

## 📌 Notas Adicionales

- **Producción:** usar contenedores (Heroku, Render, Railway).  
- **Pruebas:** unitarias e integración recomendadas.  
- **Contribuciones:** issues o PRs son bienvenidos.  

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
