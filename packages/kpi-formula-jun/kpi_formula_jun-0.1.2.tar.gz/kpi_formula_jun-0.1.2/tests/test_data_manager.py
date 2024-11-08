import pytest
import pandas as pd
from pathlib import Path
from kpi_formula.core.data_manager import DataManager

@pytest.fixture
def sample_csv(tmp_path):
    """创建测试用的CSV文件"""
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_data_manager_creation():
    """测试DataManager实例化"""
    manager = DataManager()
    assert manager.history == []
    assert manager.current_data is None

def test_import_csv(sample_csv):
    """测试CSV导入功能"""
    manager = DataManager()
    item = manager.import_csv(sample_csv)
    
    assert item is not None
    assert item.headers == ['A', 'B']
    assert len(item.data) == 3
    assert item.type == 'csv'
