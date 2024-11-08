from typing import List, Dict, Callable, Optional, Union
import operator
import numpy as np
from .models import Expression, HistoryItem, NumericType

class ExpressionManager:
    """表达式管理器"""
    
    def __init__(self):
        self.operations: Dict[str, Callable[[NumericType, NumericType], NumericType]] = {
            'add': operator.add,
            'subtract': operator.sub,
            'multiply': operator.mul,
            'divide': operator.truediv,
            'concat': lambda x, y: str(x) + str(y)
        }

    def apply_expression(self, 
                        expression: Expression,
                        history: List[HistoryItem]) -> Optional[HistoryItem]:
        """应用表达式运算"""
        try:
            # 获取源表和目标表
            source_table = next((item for item in history if item.id == expression.source_table), None)
            target_table = next((item for item in history if item.id == expression.target_table), None)

            if not source_table or not target_table:
                raise ValueError("Source or target table not found")

            # 获取列索引
            source_col_index = source_table.headers.index(expression.source_column)
            target_col_index = target_table.headers.index(expression.target_column)

            # 获取操作函数
            operation = self.operations.get(expression.operation)
            if not operation and expression.operation != 'custom':
                raise ValueError(f"Unsupported operation: {expression.operation}")

            # 处理数据
            new_data = []
            for row_index, source_row in enumerate(source_table.data):
                if row_index >= len(target_table.data):
                    break

                try:
                    source_value = float(source_row[source_col_index])
                    target_value = float(target_table.data[row_index][target_col_index])
                    
                    if expression.operation == 'custom':
                        # 处理自定义表达式
                        result = eval(
                            expression.expression,
                            {"__builtins__": {}},
                            {"x": source_value, "y": target_value, "np": np}
                        )
                    else:
                        result = operation(source_value, target_value)
                    
                    new_row = source_row.copy()
                    new_row.append(str(result))
                    new_data.append(new_row)
                    
                except (ValueError, ZeroDivisionError) as e:
                    print(f"Warning: Calculation error in row {row_index}: {str(e)}")
                    new_row = source_row.copy()
                    new_row.append("")
                    new_data.append(new_row)

            return HistoryItem(
                id=str(uuid.uuid4()),
                name=expression.name,
                timestamp=datetime.now(),
                type='csv',
                headers=[*source_table.headers, expression.name],
                data=new_data
            )

        except Exception as e:
            raise ExpressionError(f"Failed to apply expression: {str(e)}")

class ExpressionError(Exception):
    """表达式错误"""
    pass

class Operations:
    @staticmethod
    def sum(numbers: List[NumericType]) -> NumericType:
        """计算总和"""
        return sum(numbers)

    @staticmethod
    def subtract(a: NumericType, b: NumericType) -> NumericType:
        """计算差值"""
        return a - b

    @staticmethod
    def multiply(a: NumericType, b: NumericType) -> NumericType:
        """计算乘积"""
        return a * b

    @staticmethod
    def divide(a: NumericType, b: NumericType) -> NumericType:
        """计算除法"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
