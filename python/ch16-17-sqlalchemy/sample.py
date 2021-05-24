def test_sqlite3():
    # https://docs.python.org/3/library/sqlite3.html
    import sqlite3
    # con = sqlite3.connect('example.db')
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE stocks
                   (date text, trans text, symbol text, qty real, price real)''')
    # Insert a row of data
    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Save (commit) the changes
    con.commit()
    # Do this instead
    t = ('RHAT',)
    cur.execute('SELECT * FROM stocks WHERE symbol=?', t)
    result = cur.fetchone()
    # <class 'tuple'> ('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)
    print(type(result), result)
    # We can also close the connection if we are done with it.
    # Just be sure any chang
    con.close()


def test_create_engine():
    #
    from sqlalchemy import create_engine
    eng = create_engine("sqlite:///:memory:", echo=True)
    conn = eng.connect()
    conn.execute("create table x (a integer, b integer)")
    conn.execute("insert into x (a, b) values (1, 1)")
    conn.execute("insert into x (a, b) values (2, 2)")
    result = conn.execute("select x.a, x.b from x")
    # <class 'sqlalchemy.engine.result.ResultProxy'> <sqlalchemy.engine.result.ResultProxy object at 0x7f99b0247b50>
    print(type(result), result)
    assert result.keys() == ["a", "b"]
    result = conn.execute('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    # <class 'sqlalchemy.engine.result.ResultProxy'> <sqlalchemy.engine.result.ResultProxy object at 0x7fc1c00bfaf0>
    print(type(result), result)
    assert result.keys() == ["a", "b"]


def test_sql():
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy import select

    engine = create_engine('sqlite:///:memory:', echo=True)

    metadata = MetaData()
    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('fullname', String),
                  )
    print("=" * 10)
    metadata.create_all(engine)
    print("=" * 10)
    ins = users.insert().values(name='jack', fullname='Jack Jones')
    print(ins)
    result = engine.execute(ins)
    print(result, result.inserted_primary_key)
    s = select([users])
    result = engine.execute(s)
    for row in result:
        print(row)
    result = engine.execute("select * from users")
    for row in result:
        print(row)


def test_orm():
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:', echo=True)
    Model = declarative_base()

    class User(Model):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        nickname = Column(String)

        def __repr__(self):
            return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                self.name, self.fullname, self.nickname)

    Model.metadata.create_all(engine)
    print("=" * 10)
    Session = sessionmaker(bind=engine)
    session = Session()
    ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    session.add(ed_user)
    session.commit()
    print(ed_user.id)
    result = engine.execute("select * from users")
    for row in result:
        print(row)


def test_model():
    class DummyModel(object):
        name = ["dummy_model"]  # 引用类型

    a = DummyModel()
    b = DummyModel()
    assert id(a.name) == id(b.name) == id(DummyModel.name)
    a.name.append("a")
    assert id(a.name) == id(b.name) == id(DummyModel.name)

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String, Integer

    Model = declarative_base()

    class UserModel(Model):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    c = UserModel()
    c.name = "c"
    d = UserModel()
    d.name = "d"
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    # 注意并不是Column
    assert isinstance(UserModel.name, InstrumentedAttribute)
    assert isinstance(c.name, str)
    assert d.name == "d"
    assert id(c.name) != id(d.name) != id(UserModel.name)


def test_dynamic_class():
    class DeclarativeMeta(type):
        def __init__(cls, klass_name, bases, dict_):
            print("class_init", klass_name, bases, dict_)
            type.__init__(cls, klass_name, bases, dict_)

    def get_attr(self, key):
        print("getattr", self, key)
        return self.__dict__[key]

    def constructor(self, *args, **kwargs):
        print("constructor", self, args, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dynamic_class(name):
        class_dict = {
            "__init__": constructor,
            "__getattr__": get_attr
        }

        return DeclarativeMeta(name, (object,), class_dict)

    DummyModel = dynamic_class("Dummy")
    dummy = DummyModel(1, name="hello", age=18)
    print(dummy, type(dummy), dummy.name, dummy.age)


if __name__ == "__main__":
    pass
