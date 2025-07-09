import os
import sys
import django
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'biblioteca_virtual'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_virtual.settings')
django.setup()

from libros.models import Calificación, Libro

print("🔎 Analizando calificaciones...")

# Consulta ORM
calificaciones_qs = Calificación.objects.select_related('libro').all()
total = calificaciones_qs.count()
print(f"📊 Total de calificaciones encontradas: {total}")

if total == 0:
    print("⚠️ No se encontraron calificaciones. Ejecutá el generador primero.")
    exit()

# Convertir a lista de diccionarios
data = []
for c in calificaciones_qs:
    libro = c.libro
    generos = [g.nombre for g in libro.generos.all()]
    data.append({
        'Libro': libro.titulo,
        'Autor': str(libro.autor),
        'Géneros': ', '.join(generos),
        'Puntaje': c.puntaje
    })

# Crear DataFrame
df = pd.DataFrame(data)
print("\n📄 Primeros registros:")
print(df.head(10))

# Guardar CSV para usar en Colab o Excel
csv_path = os.path.join(BASE_DIR, "calificaciones.csv")
df.to_csv(csv_path, index=False)
print(f"\n💾 CSV exportado exitosamente en: {csv_path}")

# Explosión por género para análisis por categoría
df_explotado = df.copy()
df_explotado['Géneros'] = df_explotado['Géneros'].str.split(', ')
df_explotado = df_explotado.explode('Géneros')

# Promedio por género
print("\n📈 Promedio de puntaje por género:")
print(df_explotado.groupby('Géneros')['Puntaje'].mean().sort_values(ascending=False))

# Gráfico 1: Promedio de puntaje por género
promedios = df_explotado.groupby('Géneros')['Puntaje'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
promedios.plot(kind='bar', color='skyblue')
plt.title('📊 Promedio de Puntaje por Género')
plt.xlabel('Género')
plt.ylabel('Puntaje Promedio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_promedios_por_genero.png"))
plt.show()

# Gráfico 2: Distribución de puntajes por género (boxplot)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_explotado, x='Géneros', y='Puntaje', palette='pastel')
plt.title('🎯 Distribución de Puntajes por Género')
plt.xlabel('Género')
plt.ylabel('Puntaje')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_distribucion_puntajes.png"))
plt.show()

# Libros top por género con puntaje >= 4.5
print("\n🏆 Libros recomendados por género (Puntaje >= 4.5):")
top_libros = df_explotado[df_explotado['Puntaje'] >= 4.5].groupby('Géneros')['Libro'].unique()
print(top_libros)

# Gráfico 3: Cantidad de libros recomendados (>=4.5) por género
recomendados = df_explotado[df_explotado['Puntaje'] >= 4.5]
conteo_top = recomendados.groupby('Géneros')['Libro'].nunique().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
conteo_top.plot(kind='bar', color='lightgreen')
plt.title('🏆 Libros Recomendados por Género (Puntaje ≥ 4.5)')
plt.xlabel('Género')
plt.ylabel('Cantidad de Libros')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_libros_recomendados.png"))
plt.show()