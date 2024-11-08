from typing import List, Optional
import statistics

class DataProcessor:
    @staticmethod
    def moving_average(data: List[float], window: int = 3) -> List[float]:
        """计算移动平均"""
        if window <= 0:
            raise ValueError("Window size must be positive")
        results = []
        for i in range(len(data) - window + 1):
            window_average = sum(data[i:i+window]) / window
            results.append(window_average)
        return results

    @staticmethod
    def year_over_year_growth(data: List[float]) -> List[float]:
        """计算同比增长率"""
        growth_rates = []
        for i in range(12, len(data)):
            growth_rate = (data[i] - data[i-12]) / data[i-12] * 100
            growth_rates.append(growth_rate)
        return growth_rates
    
    @staticmethod
    def calculate_percentile(data: List[float], percentile: float) -> float:
        """计算百分位数"""
        return statistics.quantiles(sorted(data), n=100)[int(percentile)-1]
