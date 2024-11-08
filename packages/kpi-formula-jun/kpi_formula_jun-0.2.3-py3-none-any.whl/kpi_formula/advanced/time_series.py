from typing import List, Dict, Optional
import statistics
from ..core.operations import Operations

class TimeSeriesAnalyzer:
    @staticmethod
    def seasonality(data: List[float], period: int = 12) -> Dict[str, List[float]]:
        if len(data) < period * 2:
            raise ValueError(f"Need at least {period * 2} data points")
        
        trend = []
        for i in range(len(data) - period + 1):
            trend.append(sum(data[i:i+period]) / period)
        
        seasonal = []
        for i in range(period):
            season_values = []
            for j in range(i, len(data), period):
                if j < len(data):
                    season_values.append(data[j])
            seasonal.append(statistics.mean(season_values))
            
        return {
            "seasonal": seasonal,
            "trend": trend
        }

    @staticmethod
    def forecast_simple(data: List[float], periods: int = 1) -> List[float]:
        """简单预测"""
        if not data:
            return []
            
        avg = sum(data[-3:]) / 3 if len(data) >= 3 else sum(data) / len(data)
        return [avg] * periods

    @staticmethod
    def detect_trend(data: List[float]) -> str:
        """检测趋势方向"""
        if len(data) < 2:
            return "neutral"
            
        mid_point = len(data) // 2
        first_half = sum(data[:mid_point]) / mid_point
        second_half = sum(data[mid_point:]) / (len(data) - mid_point)
        
        if second_half > first_half * 1.05:
            return "upward"
        elif second_half < first_half * 0.95:
            return "downward"
        return "neutral"
