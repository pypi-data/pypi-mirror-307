from typing import List, Optional
import statistics

class DataProcessor:
    @staticmethod
    def moving_average(data: List[float], window: int = 3) -> List[float]:
        if window <= 0:
            raise ValueError("Window size must be positive")
        results = []
        for i in range(len(data) - window + 1):
            window_average = sum(data[i:i+window]) / window
            results.append(window_average)
        return results

    @staticmethod
    def year_over_year_growth(data: List[float]) -> List[float]:
        growth_rates = []
        for i in range(12, len(data)):
            growth_rate = (data[i] - data[i-12]) / data[i-12] * 100
            growth_rates.append(growth_rate)
        return growth_rates
    
    @staticmethod
    def calculate_percentile(data: List[float], percentile: float) -> float:
        return statistics.quantiles(sorted(data), n=100)[int(percentile)-1]
