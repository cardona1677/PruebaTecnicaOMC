# OMC Leads API 🚀

API REST para gestión de leads de **One Million Copy SAS**.  
Construida con Python, Django REST Framework y MySQL.

---

## 🛠️ Tecnologías

| Tecnología | Razón |
|---|---|
| Python + Django | Rápido desarrollo, ORM potente, ecosistema maduro |
| Django REST Framework | Serializers, validaciones y vistas basadas en clases |
| MySQL | Base de datos relacional robusta y ampliamente usada |
| drf-spectacular | Generación automática de Swagger/OpenAPI |
| pytest | Tests claros y fáciles de mantener |
| Faker | Generación de datos realistas para el seed |
| python-dotenv | Manejo seguro de variables de entorno |

---

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/cardona1677/PruebaTecnicaOMC.git
cd PruebaTecnicaOMC
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita el .env con tus credenciales de MySQL
```

### 5. Crear la base de datos en MySQL
```sql
CREATE DATABASE omc_leads CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Ejecutar el seed
```bash
python manage.py seed
```

### 8. Correr el servidor
```bash
python manage.py runserver
```

---

## 📖 Documentación Swagger

Una vez corriendo el servidor, visita:
```
http://localhost:8000/api/docs/
```

---

## 🔌 Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| POST | /leads/ | Crear un lead |
| GET | /leads/ | Listar leads (paginado, filtros) |
| GET | /leads/stats/ | Estadísticas generales |
| GET | /leads/:id/ | Obtener lead por ID |
| PATCH | /leads/:id/ | Actualizar lead |
| DELETE | /leads/:id/ | Eliminar lead (soft delete) |
| POST | /leads/ai/summary/ | Resumen ejecutivo con IA |
| POST | /leads/webhook/ | Webhook simulando Typeform |

---

## 🧪 Ejemplos de uso

### Crear un lead
```bash
curl -X POST http://localhost:8000/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos López",
    "email": "carlos@gmail.com",
    "telefono": "3001234567",
    "fuente": "instagram",
    "producto_interes": "Curso de Marketing",
    "presupuesto": 250
  }'
```

### Listar leads con filtros
```bash
curl "http://localhost:8000/leads/?fuente=instagram&page=1&limit=5"
```

### Filtrar por rango de fechas
```bash
curl "http://localhost:8000/leads/?fecha_inicio=2024-01-01&fecha_fin=2024-12-31"
```

### Obtener estadísticas
```bash
curl http://localhost:8000/leads/stats/
```

### Resumen con IA
```bash
curl -X POST http://localhost:8000/leads/ai/summary/ \
  -H "Content-Type: application/json" \
  -d '{"fuente": "instagram"}'
```

### Webhook simulando Typeform
```bash
curl -X POST http://localhost:8000/leads/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lead Webhook",
    "email": "webhook@gmail.com",
    "fuente": "landing_page",
    "presupuesto": 100
  }'
```

---

## 🧪 Correr tests
```bash
pytest --tb=short -v
```

---

## 🤖 Integración IA

El endpoint `POST /leads/ai/summary/` usa **Anthropic Claude** para generar
resúmenes ejecutivos. Si no tienes API key, la arquitectura incluye un
**mock documentado** que simula la respuesta del LLM.

Para activar el LLM real, agrega en tu `.env`:
```
ANTHROPIC_API_KEY=tu-api-key-aqui
```

---

## 📁 Estructura del proyecto
```
omc-leads-api/
├── config/
│   ├── settings.py
│   └── urls.py
├── leads/
│   ├── management/commands/seed.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```