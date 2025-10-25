from rest_framework import serializers
from .models import Peça

class PeçaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peça
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'categoria']