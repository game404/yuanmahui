"""
```
                  _         
  _ __ ___   __ _| | _____  
 | '_ ` _ \ / _` | |/ / _ \ 
 | | | | | | (_| |   < (_) |
 |_| |_| |_|\__,_|_|\_\___/ 
                            
```
"""
from typing import Type
from mako.template import Template


def test_tmp():
    mytemplate = Template("hello, ${name}!")
    print(mytemplate._code)
    print(mytemplate.module)
    print(mytemplate.callable_)
    print(mytemplate.render(name="shawn"))


def test_compile():
    expr = """x,y =1,2\nprint(x+y)"""
    code = compile(expr, "<unknown>", "exec")
    print(code, type(code))
    exec(code)


def test_ast():
    import ast
    from mako._ast_util import SourceGenerator
    expr = """x,y =1,2\nprint(x+y)"""
    ast_tree = ast.parse(expr)
    print(type(ast_tree))
    print(ast.dump(ast_tree))
    code = compile(ast_tree, filename="", mode="exec")
    print(type(code))
    exec(code)
    nt = SourceGenerator(" ")
    nt.visit(ast_tree)
    print(nt.result, len(nt.result))
    print("".join(nt.result))


def test_lexer():
    from mako.lexer import Lexer
    from mako import codegen
    lexer = Lexer("hello, ${name}!")
    node = lexer.parse()
    print(lexer.template)
    source = codegen.compile(node, "a", default_filters=[])
    print(source)


def test_compile_exec():
    import types
    source = """def add(x,y):\n    return x+y"""
    mod = types.ModuleType("test")
    print(mod, type(mod))
    code = compile(source, "test", "exec")
    print(code, type(code))
    exec(code, mod.__dict__, mod.__dict__)
    result = mod.add(1, 2)
    print(result, type(result))


def test_ast_0():
    import ast
    expr = """hello, """
    ast_tree = ast.parse(expr)
    print(type(ast_tree))
    print(ast.dump(ast_tree))


if __name__ == "__main__":
    test_tmp()
