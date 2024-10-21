from rest_framework import serializers
from .models import StrategyInfo

class StrategyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyInfo
        fields = '__all__'