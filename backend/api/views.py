import pandas as pd
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer, CSVUploadSerializer


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    serializer = CSVUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    file = serializer.validated_data['file']

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    total_equipment = len(df)

    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()

    dataset = EquipmentDataset.objects.create(
        total_equipment=total_equipment,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature
    )

    # Keep only last 5 datasets
    if EquipmentDataset.objects.count() > 5:
        EquipmentDataset.objects.order_by('uploaded_at').first().delete()

    return Response(EquipmentDatasetSerializer(dataset).data)

@api_view(['GET'])
def latest_summary(request):
    dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return Response({"message": "No data available"})

    serializer = EquipmentDatasetSerializer(dataset)
    return Response(serializer.data)


@api_view(['GET'])
def upload_history(request):
    datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)


# Create your views here.
