from typing import List, Optional, Dict, Any

class Row:
    """表示单行数据的类"""
    def __init__(self, **data):
        self.id: int = data.get('id')
        self.order: str = data.get('order')
        # 动态添加其他字段
        for key, value in data.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        fields = [f"{key}={repr(value)}" for key, value in self.__dict__.items()]
        return f"Row({', '.join(fields)})"

class RowList:
    """表示行数据列表的类"""
    def __init__(self, data: Dict[str, Any]):
        self.count: int = data.get('count', 0)
        self.next: Optional[str] = data.get('next')
        self.previous: Optional[str] = data.get('previous')
        self.results: List[Row] = [Row(**row) for row in data.get('results', [])]

    def __len__(self):
        return len(self.results)

    def __getitem__(self, index):
        return self.results[index]

    def __iter__(self):
        return iter(self.results)

    def __repr__(self):
        return f"RowList(count={self.count}, results={self.results})" 