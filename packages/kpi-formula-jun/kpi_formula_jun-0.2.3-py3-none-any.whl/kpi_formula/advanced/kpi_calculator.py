from typing import List, Dict, Optional

class KPICalculator:
    @staticmethod
    def roi(revenue: float, investment: float) -> float:
        """计算投资回报率 (ROI)"""
        if investment == 0:
            raise ValueError("Investment cannot be zero")
        return (revenue - investment) / investment * 100

    @staticmethod
    def conversion_rate(conversions: int, visitors: int) -> float:
        """计算转化率"""
        if visitors <= 0:
            raise ValueError("Number of visitors must be positive")
        return (conversions / visitors) * 100

    @staticmethod
    def customer_lifetime_value(
        avg_purchase_value: float,
        avg_purchase_frequency: float,
        customer_lifespan: float
    ) -> float:
        """计算客户终身价值 (CLV)"""
        return avg_purchase_value * avg_purchase_frequency * customer_lifespan

    @staticmethod
    def gross_margin(revenue: float, cost: float) -> float:
        """计算毛利率"""
        if revenue == 0:
            raise ValueError("Revenue cannot be zero")
        return ((revenue - cost) / revenue) * 100
