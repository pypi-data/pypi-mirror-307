from typing import List
import requests
from baserowsdk.models.field import Field
from baserowsdk.models.row import RowList


class Client:
    def __init__(self, token: str, base_url: str = "https://baserow.io"):
        """BaseRow SDK的初始化类
        
        Args:
            token (str): BaseRow的认证Token
            base_url (str): BaseRow服务器地址
        """
        self.token = token
        self.base_url = base_url.rstrip('/')  # 移除末尾的斜杠
        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
    
    def _get_full_url(self, endpoint: str) -> str:
        """构建完整的API URL
        
        Args:
            endpoint (str): API端点路径
            
        Returns:
            str: 完整的API URL
        """
        return f"{self.base_url}/{endpoint.lstrip('/')}"


    def fields(self, table_id: int) -> List[Field]:
        """获取指定表的所有字段信息
        
        Args:
            table_id (int): 表的ID
            
        Returns:
            List[Field]: 表字段信息列表，每个元素都是Field对象，包含字段的完整信息
            
        Raises:
            requests.exceptions.RequestException: 当API请求失败时抛出异常
        """
        endpoint = f"api/database/fields/table/{table_id}/"
        url = self._get_full_url(endpoint)
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()        
        return [Field(**field) for field in response.json()]

    def row(self, table_id: int, row_id: int, user_field_names: bool = False) -> dict:
        """获取指定表中的单行数据
        
        Args:
            table_id (int): 表的ID
            row_id (int): 行的ID
            user_field_names (bool): 是否使用用户定义的字段名
                                   True: 使用实际的字段名
                                   False: 使用 "field_id" 格式的字段名
            
        Returns:
            dict: 行数据，包含所有字段值
            
        Raises:
            requests.exceptions.RequestException: 当API请求失败时抛出异常
        """
        endpoint = f"api/database/rows/table/{table_id}/{row_id}/"
        url = self._get_full_url(endpoint)
        
        params = {}
        if user_field_names:
            params['user_field_names'] = 'true'
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def rows(
        self, 
        table_id: int,
        page: int = 1,
        size: int = 100,
        user_field_names: bool = True,
        search: str = None,
        order_by: str = None,
        filters: dict = None,
        filter_type: str = 'AND',
        include: str = None,
        exclude: str = None,
        view_id: int = None,
        **kwargs
    ) -> dict:
        """获取表格中的多行数据，支持分页、排序、过滤等功能
        
        Args:
            table_id (int): 表的ID
            page (int, optional): 页码，默认为1
            size (int, optional): 每页数据量，默认为100
            user_field_names (bool, optional): 是否使用用户定义的字段名，默认为False
            search (str, optional): 搜索关键词
            order_by (str, optional): 排序字段，例如：'field_1,-field_2' 或 'Name,-Age'
            filters (dict, optional): 过滤条件，JSON格式
            filter_type (str, optional): 过滤类型，'AND' 或 'OR'，默认为'AND'
            include (str, optional): 需要包含的字段，逗号分隔
            exclude (str, optional): 需要排除的字段，逗号分隔
            view_id (int, optional): 视图ID
            **kwargs: 其他过滤条件，格式为 filter__field__type=value
            
        Returns:
            dict: {
                'count': 总记录数,
                'next': 下一页URL,
                'previous': 上一页URL,
                'results': [行数据列表]
            }
            
        Raises:
            requests.exceptions.RequestException: 当API请求失败时抛出异常
        """
        endpoint = f"api/database/rows/table/{table_id}/"
        url = self._get_full_url(endpoint)
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size
        }
        
        if user_field_names:
            params['user_field_names'] = 'true'
        
        if search:
            params['search'] = search
            
        if order_by:
            params['order_by'] = order_by
            
        if filters:
            params['filters'] = filters
            
        if filter_type and filter_type.upper() in ['AND', 'OR']:
            params['filter_type'] = filter_type.upper()
            
        if include:
            params['include'] = include
            
        if exclude:
            params['exclude'] = exclude
            
        if view_id:
            params['view_id'] = view_id
            
        # 添加自定义过滤条件
        params.update({
            k: v for k, v in kwargs.items() 
            if k.startswith('filter__')
        })
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return RowList(response.json()) 

if __name__ == "__main__":
    client = Client(token="xxxx", base_url="http://192.168.40.220")
    # fields
    # fields = client.fields(182)
    # print(fields)

    # row = client.row(table_id=182, row_id=1)
    # print(row)

    rows = client.rows(table_id=182)
    print(rows)