from rest_framework import serializers
from .models import EquipmentDataset

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDataset
        fields = '__all__'
