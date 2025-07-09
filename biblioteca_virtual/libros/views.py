import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Autor, Libro, Genero, Calificación, Reseña
from .serializers import *

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(usuario_subio=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        autor_id = self.request.query_params.get('autor_id')
        q = self.request.query_params.get('q')
        if autor_id:
            queryset = queryset.filter(autor_id=autor_id)
        if q:
            queryset = queryset.filter(titulo__icontains=q)
        return queryset

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificación.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['POST'])
def registro_view(request):
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analisis_view(request):
    calificaciones = Calificación.objects.select_related('libro', 'libro__autor').prefetch_related('libro__generos')

    if not calificaciones.exists():
        return JsonResponse({'error': 'No hay calificaciones cargadas'}, status=404)

    data = []
    for c in calificaciones:
        libro = c.libro
        generos = [g.nombre for g in libro.generos.all()]
        data.append({
            'Libro': libro.titulo,
            'Autor': str(libro.autor),
            'Géneros': ', '.join(generos),
            'Puntaje': c.puntaje
        })

    df = pd.DataFrame(data)

    # Guardar CSV
    csv_path = 'media/exports/calificaciones.csv'
    df.to_csv(csv_path, index=False)

    # Explosión por género
    df_exploded = df.copy()
    df_exploded['Géneros'] = df_exploded['Géneros'].str.split(', ')
    df_exploded = df_exploded.explode('Géneros')

    promedio_generos = df_exploded.groupby('Géneros')['Puntaje'].mean().sort_values(ascending=False)
    recomendados = df_exploded[df_exploded['Puntaje'] >= 4.5].groupby('Géneros')['Libro'].unique()

    # 📊 Gráfico de promedio por género
    plt.figure(figsize=(10, 5))
    promedio_generos.plot(kind='bar', color='skyblue')
    plt.title('Promedio de Puntaje por Género')
    plt.ylabel('Puntaje Promedio')
    plt.xlabel('Género')
    plt.tight_layout()
    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    grafico_genero_base64 = base64.b64encode(buffer1.read()).decode('utf-8')
    plt.close()

    # 📊 Gráfico de promedio por autor
    promedio_autores = df.groupby('Autor')['Puntaje'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    promedio_autores.plot(kind='bar', color='orange')
    plt.title('Promedio de Puntaje por Autor')
    plt.ylabel('Puntaje Promedio')
    plt.xlabel('Autor')
    plt.xticks(rotation=90)
    plt.tight_layout()
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    grafico_autor_base64 = base64.b64encode(buffer2.read()).decode('utf-8')
    plt.close()

    return JsonResponse({
        'total_calificaciones': len(df),
        'promedio_por_genero': promedio_generos.to_dict(),
        'promedio_por_autor': promedio_autores.to_dict(),
        'recomendados_por_genero': {k: list(v) for k, v in recomendados.to_dict().items()},
        'grafico_genero_base64': grafico_genero_base64,
        'grafico_autor_base64': grafico_autor_base64,
        'csv_path': csv_path
    })