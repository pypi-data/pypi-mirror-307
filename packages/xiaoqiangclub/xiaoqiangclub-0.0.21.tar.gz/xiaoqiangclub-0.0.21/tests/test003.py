from tinydb import TinyDB, Query

# 创建数据库
db = TinyDB('example_database.json')

# 插入一些示例数据
db.insert({'name': 'Alice', 'age': 25, 'email': 'alice@example.com'})
db.insert({'name': 'Bob', 'age': 30, 'email': 'bob@example.com'})

# 定义查询对象
User = Query()

# 查找要删除字段的目标数据
target_user = db.search(User.name == 'Alice')[0]

def remove_field(doc, field_name):
    new_doc = dict(doc)
    if field_name in new_doc:
        del new_doc[field_name]
    return new_doc

updated_user = remove_field(target_user, 'email')

# 更新数据库中的数据
db.update(updated_user, User.name == 'Alice')

# 输出更新后的数据库内容
for item in db.all():
    print(item)