import os
import django
import sys
import random
from faker import Faker
from datetime import datetime, timedelta

# === Configurar entorno Django ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'biblioteca_virtual'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_virtual.settings')
django.setup()

# === Imports Django ===
from django.contrib.auth.models import User
from libros.models import Libro, Reseña, Calificación

fake = Faker('es_ES')

# === Crear usuarios ficticios ===
def crear_usuarios_si_faltan(cantidad=10):
    actuales = User.objects.count()
    faltan = cantidad - actuales
    if faltan <= 0:
        return
    for i in range(faltan):
        User.objects.create_user(username=f'usuario{i}', password='test123')
        print(f"👤 Usuario creado: usuario{i}")

# === Crear calificaciones y reseñas ===
def generar_calificaciones_y_resenas():
    libros = list(Libro.objects.all())
    usuarios = list(User.objects.all())

    for usuario in usuarios:
        libros_seleccionados = random.sample(libros, k=random.randint(5, 15))
        for libro in libros_seleccionados:
            puntaje = random.randint(1, 5)
            positiva = puntaje >= 4
            comentario = fake.sentence(nb_words=12)

            # Calificación (una por usuario/libro)
            calif, creada = Calificación.objects.get_or_create(
                usuario=usuario,
                libro=libro,
                defaults={'puntaje': puntaje, 'fecha': datetime.now()}
            )
            if creada:
                print(f"⭐ Calificación: {usuario.username} → {libro.titulo} = {puntaje} estrellas")

            # Reseña
            Reseña.objects.create(
                usuario=usuario,
                libro=libro,
                comentario=comentario,
                positiva=positiva,
                fecha=datetime.now() - timedelta(days=random.randint(0, 1000))
            )

# === Ejecutar ===
if __name__ == '__main__':
    crear_usuarios_si_faltan(10)
    generar_calificaciones_y_resenas()
    print("\n✅ Reseñas y calificaciones generadas.")
