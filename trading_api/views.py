from django.shortcuts import render
from rest_framework import viewsets
from .models import StrategyInfo
from .serializers import StrategyInfoSerializer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class StrategyInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # queryset = StrategyInfo.objects.all().order_by('-timestamp')
    queryset = StrategyInfo.objects.all().order_by('-id')  # 根據id排序 -為降冪
    serializer_class = StrategyInfoSerializer
    