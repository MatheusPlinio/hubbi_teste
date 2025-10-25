from rest_framework import generics
from .models import Peça
from .serializers import PeçaSerializer

class PeçaList(generics.ListAPIView):
    queryset = Peça.objects.all()
    serializer_class = PeçaSerializer

class PeçaDetail(generics.RetrieveAPIView):
    queryset = Peça.objects.all()
    serializer_class = PeçaSerializer

class PeçaCreate(generics.CreateAPIView):
    queryset = Peça.objects.all()
    serializer_class = PeçaSerializer

class PeçaUpdate(generics.UpdateAPIView):
    queryset = Peça.objects.all()
    serializer_class = PeçaSerializer

class PeçaDelete(generics.DestroyAPIView):
    queryset = Peça.objects.all()
    serializer_class = PeçaSerializer
