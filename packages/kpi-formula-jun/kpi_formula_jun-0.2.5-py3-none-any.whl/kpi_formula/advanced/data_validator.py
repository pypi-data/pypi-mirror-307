from typing import List, Tuple, Any, Dict
import re

class DataValidator:
    @staticmethod
    def validate_numeric(data: List[Any]) -> Tuple[List[float], List[str]]:
        cleaned_data = []
        errors = []
        for i, value in enumerate(data):
            try:
                cleaned_data.append(float(value))
            except (ValueError, TypeError):
                errors.append(f"Invalid value at index {i}: {value}")
        return cleaned_data, errors

    @staticmethod
    def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
        pattern = {
            "%Y-%m-%d": r'^\d{4}-\d{2}-\d{2}$',
            "%Y/%m/%d": r'^\d{4}/\d{2}/\d{2}$',
            "%d-%m-%Y": r'^\d{2}-\d{2}-\d{4}$'
        }
        return bool(re.match(pattern.get(format, r'^\d{4}-\d{2}-\d{2}$'), date_str))

    @staticmethod
    def remove_outliers(data: List[float], threshold: float = 2.0) -> List[float]:
        mean = sum(data) / len(data)
        std = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        return [x for x in data if abs(x - mean) <= threshold * std]
