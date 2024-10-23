from django.shortcuts import render
from rest_framework import viewsets
from .models import StrategyInfo
from .serializers import StrategyInfoSerializer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse
from bybit_test2 import get_real_time_position
def real_time_position(request):
       position = get_real_time_position()
       if position:
           return JsonResponse(position)
       else:
           return JsonResponse({'error': '無法獲取倉位信息'}, status=400)
def trading_dashboard(request):
    return render(request, 'trading_api/trading_dashboard.html')
class StrategyInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # queryset = StrategyInfo.objects.all().order_by('-timestamp')
    queryset = StrategyInfo.objects.all().order_by('-id')  # 根據id排序 -為降冪
    serializer_class = StrategyInfoSerializer
    