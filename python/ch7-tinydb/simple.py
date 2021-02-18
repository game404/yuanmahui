
def test_0():
    from tinydb import TinyDB
    db = TinyDB('simple_db.json')
    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 2, 'char': 'b'})
    db.close()


def test_1():
    from tinydb import TinyDB
    from tinydb import Query
    from tinydb import JSONStorage
    from tinydb.middlewares import CachingMiddleware
    db = TinyDB('cache_db.json', storage=CachingMiddleware(JSONStorage))
    db.purge_tables()  # 重置数据
    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 2, 'char': 'b'})
    table = db.table('user')
    table.insert({'name': "shawn", "age": 18})
    table.insert({'name': "shelton", "age": 28})
    print(table.all())  # [{'name': 'shawn', 'age': 18}, {'name': 'shelton', 'age': 28}]
    User = Query()
    table.update({'name': 'shawn', 'age': 19}, User.name == 'shawn')
    print(table.search(User.name == 'shawn'))  # [{'name': 'shawn', 'age': 19}]
    table.remove(User.name == 'shawn')
    db.close()


if __name__ == "__main__":
    test_1()
