from rest_framework.viewsets import ModelViewSet
from .models import Internship
from .serializers import InternshipSerializer

class InternshipViewSet(ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
