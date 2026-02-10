import pandas as pd
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import HttpResponse
from .pdf_utils import generate_pdf_report
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer, CSVUploadSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
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

    # ✅ Equipment type distribution (Phase 6A)
    equipment_type_distribution = (
        df["Type"]
        .value_counts()
        .to_dict()
    )

    dataset = EquipmentDataset.objects.create(
        total_equipment=total_equipment,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature,
        equipment_type_distribution=equipment_type_distribution
    )

    # Keep only last 5 datasets
    if EquipmentDataset.objects.count() > 5:
        EquipmentDataset.objects.order_by('uploaded_at').first().delete()

    return Response({
        "id": dataset.id,
        "uploaded_at": dataset.uploaded_at,
        "total_equipment": total_equipment,
        "avg_flowrate": avg_flowrate,
        "avg_pressure": avg_pressure,
        "avg_temperature": avg_temperature,
        "equipment_type_distribution": equipment_type_distribution
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def latest_summary(request):
    dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return Response({"message": "No data available"})

    return Response({
        "id": dataset.id,
        "uploaded_at": dataset.uploaded_at,
        "total_equipment": dataset.total_equipment,
        "avg_flowrate": dataset.avg_flowrate,
        "avg_pressure": dataset.avg_pressure,
        "avg_temperature": dataset.avg_temperature,
        "equipment_type_distribution": dataset.equipment_type_distribution
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_history(request):
    datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def download_report(request):
    dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return Response({"error": "No data available"}, status=400)

    pdf_buffer = generate_pdf_report(dataset)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'
    return response
