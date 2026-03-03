import logging
from sqlalchemy import create_engine
from sqlalchemy import inspect

log = logging.getLogger(__name__)

class MySQLDatabaseManger:
    """MySQL数据库管理类, 用于连接和操作MySQL数据库.
    

    """
    def __init__(self,connection_string:str):
        """初始化MySQL数据库管理类.
        
        Args:
            connection_string (str): MySQL数据库连接字符串.
        """
        self.engine = create_engine(connection_string,pool_size = 5,pool_recycle = 3600)

    def get_table_names(self) -> list[str]:
        """获取数据库中所有表的名称.
        
        Returns:
            List[str]: 数据库中所有表的名称列表.
        """
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            log.exception(f"获取数据库中所有表的名称失败: {e}")
            raise ValueError(f"获取数据库中所有表的名称失败: {e}")

if __name__ == '__main__':
    username = 'root'
    password = 'zjs20060618'
    host = 'localhost'
    port = '3306'
    database = 'zhaojianshuo'
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    manager = MySQLDatabaseManger(connection_string)
    print(manager.get_table_names())
