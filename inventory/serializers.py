from rest_framework import serializers
from .models import Part, ImportTask


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "created_at",
            "updated_at",
        ]


class ImportTaskSerializer(serializers.ModelSerializer):
    executed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ImportTask
        fields = [
            "id",
            "file_path",
            "status",
            "total_imported",
            "executed_by",
            "created_at",
            "finished_at",
        ]
        read_only_fields = ["status", "total_imported", "created_at", "finished_at"]
