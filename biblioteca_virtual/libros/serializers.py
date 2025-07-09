from rest_framework import serializers
from .models import Autor, Libro, Genero, Calificación, Reseña
from django.contrib.auth.models import User


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    usuario_subio = serializers.HiddenField(default=serializers.CurrentUserDefault())

    autor = AutorSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), source='autor', write_only=True)
    generos = GeneroSerializer(many=True, read_only=True)
    generos_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Genero.objects.all(), source='generos', write_only=True)

    class Meta:
        model = Libro
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificación
        fields = '__all__'

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseña
        fields = '__all__'

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
