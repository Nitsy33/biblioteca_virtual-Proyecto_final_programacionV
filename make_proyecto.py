import os
import sys
import django
import random
from faker import Faker
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
from datetime import datetime, timedelta
from django.core.files import File

# === CONFIGURACIÓN DJANGO CORRECTA ===
# Añadir la ruta del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'biblioteca_virtual'))

# Ruta correcta al settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_virtual.settings')
django.setup()

# === IMPORTAR MODELOS ===
from libros.models import Autor, Genero, Libro
from django.contrib.auth.models import User

# === CONFIGURACIÓN DE ARCHIVOS ===
fake = Faker('es_ES')
MEDIA = os.path.join(BASE_DIR, 'media')
AUTORES_DIR = os.path.join(MEDIA, 'autores')
PORTADAS_DIR = os.path.join(MEDIA, 'libros', 'portadas')
PDF_DIR = os.path.join(MEDIA, 'libros', 'pdf')

os.makedirs(AUTORES_DIR, exist_ok=True)
os.makedirs(PORTADAS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

try:
    FONT = ImageFont.truetype("arial.ttf", 18)
except:
    FONT = ImageFont.load_default()

def generar_imagen(texto, ruta, size=(300, 400), bg=(255, 255, 255)):
    img = Image.new('RGB', size, bg)
    draw = ImageDraw.Draw(img)
    draw.text((10, size[1] // 2 - 10), texto, fill=(0, 0, 0), font=FONT)
    img.save(ruta)

def generar_pdf(texto, ruta):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linea in texto.split('\n'):
        pdf.cell(200, 10, txt=linea, ln=1)
    pdf.output(ruta)

def crear_generos():
    generos = ["Terror", "Romance", "Fantasía", "Ciencia Ficción", "Histórico", "Drama", "Aventura", "Misterio"]
    for nombre in generos:
        obj, creado = Genero.objects.get_or_create(nombre=nombre)
        if creado:
            print(f"✅ Género creado: {nombre}")

def crear_autores(n=30):
    autores = []
    for i in range(n):
        nombre = fake.name()
        nacionalidad = fake.country()
        img_path = os.path.join(AUTORES_DIR, f'autor{i+1}.jpg')
        generar_imagen(nombre, img_path)

        with open(img_path, 'rb') as f:
            autor = Autor.objects.create(
                nombre=nombre,
                nacionalidad=nacionalidad,
                foto=File(f, name=f'autor{i+1}.jpg')
            )
            autores.append(autor)
            print(f"👤 Autor creado: {nombre}")
    return autores

def crear_libros(autores, n=120):
    generos = list(Genero.objects.all())
    usuario = User.objects.first()
    if not usuario:
        usuario = User.objects.create_user(username='admin', password='admin123')
        print("👤 Usuario admin creado automáticamente")

    for i in range(n):
        titulo = fake.sentence(nb_words=4).replace('.', '')
        descripcion = fake.paragraph(nb_sentences=5)
        isbn = fake.isbn13(separator="")[:13]  # sin guiones y limitado a 13 caracteres

        editorial = fake.company()
        idioma = random.choice(['Español', 'Inglés'])
        fecha = datetime.now().date() - timedelta(days=random.randint(0, 4000))
        autor = random.choice(autores)
        genero_sel = random.sample(generos, random.randint(1, 3))

        pdf_path = os.path.join(PDF_DIR, f'libro{i+1}.pdf')
        portada_path = os.path.join(PORTADAS_DIR, f'portada{i+1}.jpg')

        generar_imagen(titulo, portada_path)
        generar_pdf(f"{titulo}\n\n{descripcion}", pdf_path)

        libro = Libro(
            titulo=titulo,
            descripcion=descripcion,
            isbn=isbn,
            editorial=editorial,
            idioma=idioma,
            fecha_emision=fecha,
            autor=autor,
            usuario_subio=usuario,
        )

        with open(pdf_path, 'rb') as pdf_file:
            libro.pdf_url.save(f'libro{i+1}.pdf', File(pdf_file), save=False)

        with open(portada_path, 'rb') as img_file:
            libro.imagen_portada.save(f'portada{i+1}.jpg', File(img_file), save=False)

        libro.save()
        libro.generos.set(genero_sel)

        print(f"📘 Libro {i+1} creado: {titulo}")

# === EJECUCIÓN ===
if __name__ == '__main__':
    print("📦 Cargando géneros...")
    crear_generos()

    print("\n🧑‍🎨 Generando autores...")
    autores = crear_autores()

    print("\n📚 Generando libros...")
    crear_libros(autores)

    print("\n✅ Carga finalizada con éxito.")
