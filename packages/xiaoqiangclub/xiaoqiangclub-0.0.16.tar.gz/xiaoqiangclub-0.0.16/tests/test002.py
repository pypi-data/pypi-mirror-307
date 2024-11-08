# 使用 with 语句管理数据库连接
from xiaoqiangclub import TinyDBManager

with TinyDBManager('my_db.json') as db:
    # 在 with 语句块中可以正常执行数据库操作
    data_to_insert = {'name': 'Alice', 'age': 30}
    db.insert_data(data_to_insert)

    # 查询数据
    result = db.query({'name': 'Alice'})
    print(result)
