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
    engine = create_engine('sqlite:///:memory:', echo=True)
    from sqlalchemy import MetaData
    metadata = MetaData()
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String
    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('fullname', String),
                  )
    metadata.create_all(engine)
    ins = users.insert()
    print(ins)


if __name__ == "__main__":
    pass
