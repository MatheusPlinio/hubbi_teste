from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Part, ImportTask
from .serializers import PartSerializer, ImportTaskSerializer
from .tasks import import_csv_task 

class PartListView(generics.ListAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAuthenticated]


class PartDetailView(generics.RetrieveAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAuthenticated]


class PartCreateView(generics.CreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAdminUser]


class PartUpdateView(generics.UpdateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAdminUser]


class PartDeleteView(generics.DestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAdminUser]

class ImportCSVView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        file_path = request.data.get("file_path")
        if not file_path:
            return Response({"error": "O campo file_path é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        task = ImportTask.objects.create(
            file_path=file_path,
            executed_by=request.user,
            status="pending"
        )

        import_csv_task.delay(task.id)

        serializer = ImportTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImportTaskListView(generics.ListAPIView):
    queryset = ImportTask.objects.all()
    serializer_class = ImportTaskSerializer
    permission_classes = [permissions.IsAdminUser]
