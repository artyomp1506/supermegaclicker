from rest_framework.serializers import ModelSerializer
from .models import Core

class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['weight', 'power', 'level','is_weight_prev_for_next_level', 'is_levelup']
