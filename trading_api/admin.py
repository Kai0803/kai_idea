from django.contrib import admin
from .models import StrategyInfo

@admin.register(StrategyInfo)
class StrategyInfoAdmin(admin.ModelAdmin):
    list_display = ['strategy_name', 'current_position', 'profit_loss', 'timestamp']
    search_fields = ['strategy_name']
    list_filter = ['timestamp']