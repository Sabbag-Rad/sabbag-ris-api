# 🏥 Sabbag RIS API Backend

Proyecto serverless en AWS para la gestión de estudios, informes médicos, recuperación de contraseña y visualización DICOM.

---

## ⚙️ Arquitectura

- **Lenguaje:** Python 3.9
- **Framework:** Serverless Framework v4
- **Proveedor:** AWS Lambda + API Gateway (HTTP API)
- **Servicios AWS:** Lambda, S3, Secrets Manager, CloudWatch, Redis (externo)
- **Autenticación:** JWT
- **PDF:** xhtml2pdf (HTML -> PDF)
- **RTF Parser:** Custom RTF to Text

---

## 📁 Estructura de Carpetas

```
src/
│
├── handlers/           # Lambda handlers (API endpoints)
├── services/           # Lógica de negocio por dominio
├── repositories/       # Acceso a datos y consultas SQL
├── schemas/            # Validaciones Pydantic
├── common/             # Decoradores, utils, logs, auth
├── config/             # Conexión DB, Redis y Secrets Manager
└── templates/          # Plantillas HTML para informes
```

---

## 📦 Endpoints disponibles

### 1. 📄 Obtener listado de estudios de un paciente

- **Método:** `GET`
- **Ruta:** `/studies/{patient_id}`
- **Query Params:** `modality`, `service_name`, `study_number`, `start_date`, `end_date`, `order_by`, `order`, `page`, `limit`

Retorna un listado paginado con los estudios realizados por un paciente.

---

### 2. 📑 Obtener informe PDF de un estudio

- **Método:** `GET`
- **Ruta:** `/report/{report_id}`

Retorna la URL pública de un PDF generado desde el contenido RTF del informe médico.

---

### 3. 🖼️ Obtener URL del visor DICOM

- **Método:** `POST`
- **Ruta:** `/dicom`
- **Body:**

```json
{
  "study_number": "123456-01",
  "username": "usuarioDICOM",
  "password": "claveSegura"
}
```

Construye una URL de acceso al visor DICOM externo con los datos provistos.

---

### 4. 🔐 Recuperación de contraseña - Opciones

- **Método:** `POST`
- **Ruta:** `/recovery/options`

Recibe los datos del usuario y devuelve los canales disponibles para recibir el OTP (email, celular).

---

### 5. 📩 Recuperación de contraseña - Solicitar OTP

- **Método:** `POST`
- **Ruta:** `/recovery/request`
- **Body:**

```json
{
  "document_type": "CC",
  "document": "12345678",
  "method": "email"
}
```

---

### 6. ✅ Recuperación de contraseña - Verificar OTP

- **Método:** `POST`
- **Ruta:** `/recovery/verify`
- **Body:**

```json
{
  "document_type": "CC",
  "document": "12345678",
  "otp": "123456"
}
```

---

## 🔐 Variables de entorno

Estas variables son cargadas desde `.env.dev` o `.env.prod`:

- `JWT_SECRET`
- `DB_MEDILAB_SECRET_ARN`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_IDENTIFIER`
- `DICOM_URL`
- `S3_BUCKET`

---

## 📚 Stack de dependencias clave

- `psycopg2-binary`: Acceso PostgreSQL
- `pydantic`: Validación
- `xhtml2pdf`: Generación PDF
- `jinja2`: Templates HTML
- `boto3`: AWS SDK

---

## 🚀 Despliegue

```bash
sls deploy --stage dev
```

Utiliza `serverless-dotenv-plugin` y `serverless-python-requirements` con Docker para garantizar compatibilidad con Lambda.

---

## 📄 Logs

Cada capa (handler, service, repository) usa `logging` con prefijos como:

- `[Handler]`
- `[Service]`
- `[Repository]`
- `[PDF Service]`
- `[S3]`

Esto permite trazabilidad clara desde CloudWatch.

---

## ✅ Buenas prácticas aplicadas

- Arquitectura limpia desacoplada por capas
- Manejo centralizado de errores (`standard_response`)
- Validación estructurada con Pydantic
- Templates HTML con `|safe` para control seguro
- Variables gestionadas por entorno
- Archivos temporales generados en `/tmp`

---
