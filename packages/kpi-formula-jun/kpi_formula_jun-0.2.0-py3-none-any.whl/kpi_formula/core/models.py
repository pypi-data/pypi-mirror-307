from typing import Union, List, Dict, Any

# 定义数值类型
NumericType = Union[int, float]

class Expression:
    """表达式类"""
    def __init__(self, value: Any):
        self.value = value

    def evaluate(self) -> NumericType:
        return float(self.value)

class HistoryItem:
    """历史记录项"""
    def __init__(self, operation: str, inputs: List[Any], result: Any):
        self.operation = operation
        self.inputs = inputs
        self.result = result

    def to_dict(self) -> Dict[str, Any]:
        return {
            'operation': self.operation,
            'inputs': self.inputs,
            'result': self.result
        }

class JoinConfig:
    """连接配置类"""
    def __init__(self, 
                 left_table: str, 
                 right_table: str, 
                 left_key: str, 
                 right_key: str,
                 join_type: str = 'inner'):
        self.left_table = left_table
        self.right_table = right_table
        self.left_key = left_key
        self.right_key = right_key
        self.join_type = join_type

    def to_dict(self) -> Dict[str, str]:
        return {
            'left_table': self.left_table,
            'right_table': self.right_table,
            'left_key': self.left_key,
            'right_key': self.right_key,
            'join_type': self.join_type
        }
