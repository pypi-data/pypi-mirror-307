import uuid
from datetime import datetime
from typing import List, Optional
import pandas as pd
from pathlib import Path
from .models import HistoryItem

class DataManager:
    """数据管理器核心类"""
    
    def __init__(self):
        self.history: List[HistoryItem] = []
        self.current_data: Optional[HistoryItem] = None

    def import_csv(self, file_path: str) -> HistoryItem:
        """从CSV文件导入数据"""
        try:
            df = pd.read_csv(file_path)
            file_name = Path(file_path).stem
            
            item = HistoryItem(
                id=str(uuid.uuid4()),
                name=f"{file_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                type='csv',
                headers=df.columns.tolist(),
                data=df.values.tolist()
            )
            
            self.history.insert(0, item)
            self.current_data = item
            return item
            
        except Exception as e:
            raise ImportError(f"Failed to import CSV file: {str(e)}")

    def export_csv(self, item: HistoryItem, file_path: str) -> None:
        """导出数据到CSV文件"""
        try:
            df = pd.DataFrame(item.data, columns=item.headers)
            df.to_csv(file_path, index=False)
        except Exception as e:
            raise ExportError(f"Failed to export CSV file: {str(e)}")

    def update_cell(self, row_index: int, col_index: int, value: str) -> None:
        """更新单元格数据"""
        if not self.current_data:
            raise ValueError("No current data selected")

        try:
            new_data = [row.copy() for row in self.current_data.data]
            new_data[row_index][col_index] = value
            
            updated_item = HistoryItem(
                id=self.current_data.id,
                name=f"{self.current_data.name}_updated",
                timestamp=datetime.now(),
                type=self.current_data.type,
                headers=self.current_data.headers,
                data=new_data,
                source=self.current_data.source
            )
            
            # 更新历史记录
            self.history = [
                updated_item if item.id == self.current_data.id else item
                for item in self.history
            ]
            self.current_data = updated_item
            
        except Exception as e:
            raise UpdateError(f"Failed to update cell: {str(e)}")

    def get_item_by_id(self, item_id: str) -> Optional[HistoryItem]:
        """通过ID获取历史记录项"""
        return next((item for item in self.history if item.id == item_id), None)

    def clear_history(self) -> None:
        """清空历史记录"""
        self.history.clear()
        self.current_data = None

class ImportError(Exception):
    """导入错误"""
    pass

class ExportError(Exception):
    """导出错误"""
    pass

class UpdateError(Exception):
    """更新错误"""
    pass
