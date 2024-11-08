from typing import List, Dict, Optional
from .models import JoinConfig, HistoryItem
import uuid
from datetime import datetime

class JoinManager:
    """表连接管理器"""
    
    def perform_join(self, 
                    config: JoinConfig,
                    history: List[HistoryItem]) -> Optional[HistoryItem]:
        """执行表连接操作"""
        try:
            # 获取左表和右表
            left_table = next((item for item in history if item.id == config.left_table), None)
            right_table = next((item for item in history if item.id == config.right_table), None)

            if not left_table or not right_table:
                raise ValueError("Left or right table not found")

            # 获取连接列索引
            left_col_index = left_table.headers.index(config.left_column)
            right_col_index = right_table.headers.index(config.right_column)

            # 创建右表的查找映射（排除连接列）
            right_headers = [h for i, h in enumerate(right_table.headers) if i != right_col_index]
            right_map = {
                row[right_col_index]: [v for i, v in enumerate(row) if i != right_col_index]
                for row in right_table.data
            }

            joined_data = []
            
            # 根据连接类型执行操作
            if config.type in ['inner', 'left']:
                for left_row in left_table.data:
                    key = left_row[left_col_index]
                    right_values = right_map.get(key)
                    if right_values:
                        joined_data.append([*left_row, *right_values])
                    elif config.type == 'left':
                        joined_data.append([*left_row, *[''] * len(right_headers)])

            if config.type in ['right', 'full']:
                # 创建左表的查找映射
                left_map = {row[left_col_index]: row for row in left_table.data}
                
                for right_row in right_table.data:
                    key = right_row[right_col_index]
                    if key not in left_map:
                        filtered_right = [v for i, v in enumerate(right_row) if i != right_col_index]
                        joined_data.append([*[''] * len(left_table.headers), *filtered_right])

            return HistoryItem(
                id=str(uuid.uuid4()),
                name=f"Joined {left_table.name} & {right_table.name}",
                timestamp=datetime.now(),
                type='csv',
                headers=[*left_table.headers, *right_headers],
                data=joined_data
            )

        except Exception as e:
            raise JoinError(f"Failed to perform join: {str(e)}")

class JoinError(Exception):
    """连接错误"""
    pass
