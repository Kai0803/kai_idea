from django.db import models
#API設置
"""
Get:
curl http://localhost:8000/api/strategy-info/
--------------------------------
Post:
curl -X POST http://localhost:8000/api/strategy-info/ \
     -H "Content-Type: application/json" \
     -d '{"strategy_name": "Test Strategy", "current_position": 100.0, "profit_loss": 50.0}'
--------------------------------
"""
class StrategyInfo(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    strategy_name = models.CharField(max_length=100)
    current_position = models.FloatField()
    profit_loss = models.FloatField()
    def __str__(self):
           return f"{self.strategy_name} - {self.timestamp}"