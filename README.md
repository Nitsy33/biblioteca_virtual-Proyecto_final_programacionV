
# 📚 Biblioteca Virtual

Proyecto final para la materia de Programación V – Universidad. Este proyecto implementa una plataforma en Django para registrar, listar y analizar libros, autores, calificaciones y reseñas, con autenticación por token y soporte de análisis de datos en Google Colab.

---

## ✅ 1. Versiones de Herramientas

- Python: 3.11+
- Django: 5.2.4
- PostgreSQL: 15+
- Pandas: 2.x
- matplotlib: 3.x
- seaborn: 0.13.x
- djangorestframework: 3.15+
- Simple JWT: 5.x
- Faker: 24.10
- fpdf, Pillow (para generación de libros PDF y portadas)

---

## ⚙️ 2. Instalaciones y Configuración

### Crear entorno virtual:
```bash
python -m venv env
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

### Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Crear proyecto y app Django:
```bash
django-admin startproject biblioteca_virtual
cd biblioteca_virtual
python manage.py startapp libros
```

### Configurar base de datos (PostgreSQL):
Editar en `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_db',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📖 3. Explicación del Programa

Este sistema permite:
- Registrar autores y libros con PDF y portada.
- Guardar calificaciones y reseñas.
- Autenticarse con tokens JWT.
- Listar libros y aplicar filtros por género o autor.
- Analizar puntuaciones promedio por género/autor.
- Generar gráficas y exportar datos para Colab.

Incluye endpoints para autenticación, registro, análisis y sugerencias, además de scripts generadores automáticos de contenido de prueba.

---

## ✍️ 4. Registro de Libros (código y prueba Postman)

### Endpoint:
`POST /api/libros/` *(requiere autenticación con token)*

### Ejemplo JSON:
```json
{
  "titulo": "La Sombra del Viento",
  "fecha_emision": "2020-10-10",
  "descripcion": "Novela gótica ambientada en Barcelona.",
  "isbn": "1234567890123",
  "editorial": "Planeta",
  "idioma": "Español",
  "autor_id": 1,
  "generos_id": [1, 3]
}
```

El archivo PDF y la portada se deben cargar con `multipart/form-data` en Postman.

---

## 📚 5. Listado de Libros

### Endpoint:
`GET /api/libros/`

Opciones de filtro:

- `?autor_id=1` → libros de un autor específico.
- `?q=palabra` → búsqueda por título.

---

## ⚙️ 6. Scripts incluidos

### 📦 `make_proyecto.py`
Script que genera:
- 30 autores con fotos ficticias
- 120 libros con portadas y archivos PDF generados
- Asociación de libros con autores y géneros

### 🧠 `generar_resenas_y_calificaciones.py`
Genera automáticamente:
- Usuarios ficticios
- Calificaciones de 1 a 5 estrellas
- Reseñas positivas/negativas simuladas

---

## 🧪 7. Análisis de Datos y Gráficos

### 🔎 Script: `analisis.py`
Este script extrae datos de calificaciones y genera:
- Archivo `calificaciones.csv`
- Gráficos de barras (puntaje promedio por género)
- Boxplot de distribución por género
- Recomendaciones de libros con puntuación ≥ 4.5
![grafico_distribucion_puntajes](https://github.com/user-attachments/assets/faabff6d-adb9-4f98-b13e-d7a292537cd8)


### 🧮 Endpoint: `/api/analisis/`
Devuelve JSON con:
- Promedios por autor/género
- Libros recomendados
- Gráficos en base64 listos para frontend
![grafico_libros_recomendados](https://github.com/user-attachments/assets/2c58a64d-6314-4bcc-a501-45ad3c93079a)
![grafico_promedios_por_genero](https://github.com/user-attachments/assets/8bd8b578-449b-4de4-92f9-0eaa22776546)

---

## 🧠 8. Sugerencias por Género

Tanto el endpoint `/api/analisis/` como el script de análisis identifican automáticamente los libros mejor puntuados por género para sugerencias dinámicas o dashboards.

---

## 📝 9. Licencia de Herramientas

Este proyecto utiliza herramientas y librerías con licencias open source:

| Tecnología      | Licencia               |
|----------------|------------------------|
| Python         | PSF License            |
| Django         | BSD                    |
| PostgreSQL     | PostgreSQL License     |
| Pandas         | BSD                    |
| matplotlib     | PSF-based              |
| seaborn        | BSD                    |
| Faker          | MIT                    |
| fpdf           | LGPL                   |
| Pillow         | HPND                   |

---

## 🚀 Ejecutar en local

```bash
python manage.py runserver
```

Luego visitar: http://127.0.0.1:8000/api/libros/

---
