from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Literal

@dataclass
class DatabaseSource:
    """数据库源的配置信息"""
    type: Literal['database']
    connection: str
    query: str

@dataclass
class HistoryItem:
    """历史记录项"""
    id: str
    name: str
    timestamp: datetime
    type: Literal['csv', 'database']
    headers: List[str]
    data: List[List[str]]
    source: Optional[DatabaseSource] = None
