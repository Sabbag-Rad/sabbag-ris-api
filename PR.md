# 🧾 Portal de Resultados – Historias de Usuario y Criterios de Aceptación

---

## ✅ US02A - Inicio de sesión de pacientes

**Como** paciente
**Quiero** iniciar sesión con mi tipo y número de documento más una contraseña
**Para** acceder de forma segura a mis estudios médicos.

**Criterios de Aceptación:**

* El formulario de login permite seleccionar tipo de documento (CC, TI, CE, etc.).
* Se ingresan los campos: tipo\_documento, documento, contraseña.
* El sistema valida las credenciales contra la base de datos.
* Si son válidas, se retorna un token JWT con el rol `paciente`.
* Si son inválidas, se muestra un mensaje claro.
* El token tiene expiración y permite acceder solo a rutas de paciente.

---

## ✅ US02B - Inicio de sesión de médicos

**Como** médico
**Quiero** iniciar sesión con mi usuario y contraseña
**Para** acceder a los estudios de mis pacientes y sus resultados.

**Criterios de Aceptación:**

* El formulario de login muestra los campos: usuario, contraseña.
* El sistema valida contra la base de datos o Cognito.
* Si son válidas, se retorna un token JWT con el rol `medico`.
* Si son inválidas, se muestra mensaje de error.
* El token permite acceder a rutas específicas para médicos.

---

## ✅ US03 - Listado de estudios

**Como** paciente
**Quiero** ver un listado de mis estudios médicos
**Para** poder consultar su estado y resultado.

**Criterios de Aceptación:**

* El endpoint `/studies` muestra la lista de estudios del usuario autenticado.
* La lista incluye: nombre del estudio, tipo, estado, fecha.
* Respuesta paginada.
* Acceso sin autenticación da error 401.

---

## ✅ US04 - Filtrar estudios

**Como** paciente
**Quiero** filtrar mis estudios por fecha o tipo
**Para** encontrar resultados específicos.

**Criterios de Aceptación:**

* Se pueden aplicar filtros desde el frontend.
* Se pueden combinar filtros (tipo + fecha).
* Solo se muestran estudios que cumplan los filtros.

---

## ✅ US05 - Ver resultados PDF

**Como** paciente
**Quiero** visualizar el resultado en PDF de un estudio
**Para** poder consultarlo o imprimirlo.

**Criterios de Aceptación:**

* “Ver PDF” solo aparece si el estudio está “finalizado”.
* El PDF se abre en modal o nueva pestaña.
* Si no hay PDF, se muestra mensaje informativo.

---

## ✅ US06 - Ver imágenes diagnósticas

**Como** paciente
**Quiero** visualizar las imágenes de mi estudio
**Para** consultarlas junto al informe.

**Criterios de Aceptación:**

* El botón está disponible solo si hay imágenes.
* Se muestra visor o enlace al recurso (S3/DICOM).
* Se valida permiso antes de mostrar.

---

## ✅ US07 - Cierre de sesión

**Como** paciente
**Quiero** cerrar sesión del portal
**Para** evitar accesos no autorizados.

**Criterios de Aceptación:**

* El botón de logout elimina el token del frontend.
* El usuario es redirigido al login.
* Las rutas protegidas no se pueden acceder sin autenticación.

---

## ✅ US09 - Documentación de API

**Como** QA o desarrollador
**Quiero** tener documentación clara de la API
**Para** poder probarla y consumirla correctamente.

**Criterios de Aceptación:**

* La API está documentada con Swagger/OpenAPI.
* Se incluyen ejemplos, headers, body y respuestas.
* Se indica qué rutas requieren autenticación.

---

## ✅ US10 - Auditoría de accesos

**Como** administrador
**Quiero** registrar accesos de los usuarios
**Para** tener trazabilidad del uso del portal.

**Criterios de Aceptación:**

* Cada login o consulta de estudio genera un registro.
* El log incluye: `user_id`, acción, IP, timestamp.
* Se guarda en DynamoDB o S3.
