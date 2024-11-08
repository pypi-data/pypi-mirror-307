from typing import List, Dict, Optional
import statistics
from ..core.operations import Operations

class TimeSeriesAnalyzer:
    @staticmethod
    def seasonality(data: List[float], period: int = 12) -> Dict[str, List[float]]:
        """分析季节性模式"""
        if len(data) < period * 2:
            raise ValueError(f"Need at least {period * 2} data points")
        
        # 计算移动平均作为趋势
        trend = []
        for i in range(len(data) - period + 1):
            trend.append(sum(data[i:i+period]) / period)
        
        # 计算季节性因子
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
            
        # 使用简单移动平均进行预测
        avg = sum(data[-3:]) / 3 if len(data) >= 3 else sum(data) / len(data)
        return [avg] * periods

    @staticmethod
    def detect_trend(data: List[float]) -> str:
        """检测趋势方向"""
        if len(data) < 2:
            return "neutral"
            
        first_half = sum(data[:len(data)//2]) / (len(data)//2)
        
        if second_half > first_half * 1.05:
            return "upward"
        elif second_half < first_half * 0.95:
            return "downward"
        return "neutral"  # 默认返回 "neutral" 而不是 None
