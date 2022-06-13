from rest_framework.serializers import ModelSerializer
from .models import Core, Boost

class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['weight', 'power', 'level','is_weight_prev_for_next_level', 'is_levelup', 'image_number', 'current_size']
class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'